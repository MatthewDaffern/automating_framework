import json
from functools import partial
from nornir import InitNornir
from nornir.plugins.tasks import commands
from Crypto.Cipher import AES
from hashlib import sha3_256

# =====================================================================================================================
# Functions that pull the config
# All of these work as intended.
# The idea is to:
#     1. apply the reading config(read.json) and get the current state
#     2. difference the results between that and the last saved read config(read.json)
#     3. for those that are different, apply the constituent elements of the write config(write.json)
#     4. after that, save your state in read.json
#
# Now, you may ask. Why don't you just write some quick Napalm code and be done? Well, I don't work in an environment
# That has compatible napalm drivers for much of my stuff, and I want to be able to write 'configs'
# For any type of device that has the ability to connect via SSH. Many of the computers in my environment don't support
# WinRM because it's been removed, and I certainly won't be able to install Ansible.
# This is my work around for all of that.

def elements_to_first_level(dict_input, key_value):
    return dict_input[key_value]


def get_list_of_elements(dict_input, key_value):
    return list(dict_input[key_value].keys())


def unapplied_parameters(old_dict, new_dict):
    """the goal is to be able to parse any config so to speak, and apply the uncommitted changes
           regardless of platform or architecture.
           The goal is to be able to only write commands that haven't been configured yet."""
    key_value_string = 'config'
    old_dict_converted = elements_to_first_level(old_dict, key_value_string)
    new_dict_converted = elements_to_first_level(new_dict, key_value_string)
    list_of_elements = old_dict_converted.keys()
    difference_dict = dict()
    for i in list_of_elements:
        if not old_dict_converted[i]['result'] == new_dict_converted[i]['result']:
            difference_dict[i] = new_dict_converted[i]
    return {'config': difference_dict}


# =============================================================
# So I use nornir to get my stuff done.


# Pass
def get_command_list(config_object):
    list_of_commands = config_object['config'].keys()
    command_list = list()
    for i in list_of_commands:
        command_list.append(config_object['config'][i]['command'])
    return command_list


def config_action(nornir_object, list_of_commands):
    """This will allow you to get or apply the list of commands.
    All you need is for it to be a list of commands and a single host"""
    print(list_of_commands)
    results = dict()
    for i in list_of_commands:
        results[i] = nornir_object.run(task=commands.remote_command, command=i)
    return results


def save_the_output(results, config):
    """overwrites the results"""
    config_elements = elements_to_first_level(config, 'config')
    for i in config_elements.keys():
        config_elements[i]['result'] = results[i]
    return {'config': config_elements}


def write_to_config(config, file_name):
    with open(file_name, 'w+') as config_file:
        json.dump(config_file, config)
    return str.join('', (file_name, ' ', 'has been saved'))


# PASS
def init_nornir(config_file_name):
    return InitNornir(config_file=config_file_name)


# passed
def truth_test(value_input, value_test):
    return value_input == value_test


# passed
def filter_by_platform(nornir_object, filter_name):
    """I only really care about name or platform, this filters by platform"""
    platform = partial(truth_test, value_test=filter_name)
    return nornir_object.filter(filter_func=lambda h: platform(h.platform)).inventory.hosts


# Passed
def filter_by_name(nornir_object, filter_name):
    """This filters nornir by name"""
    name = partial(truth_test, value_test=filter_name)
    return nornir_object.filter(filter_func=lambda h: name(h.name)).inventory.hosts


# passed
def load_config(json_file):
    config = open(json_file, 'r+')
    return json.load(config)


def create_hash(passphrase):
    hash_object = sha3_256(str.encode(passphrase))
    return hash_object.digest()


# the goal is to grab the actual password and encrypt each one on the nornir config.
def encrypt_password(config, passphrase):
    password = config['config']['actual_password']
    cipher = AES.new(create_hash(passphrase), AES.MODE_EAX)
    encrypted_password = cipher.encrypt_and_digest(password)
    config['config']['actual_password'] = [encrypted_password, cipher.nonce]
    return config


def decrypt_password(config, passphrase):
    password = config['config']['actual_password']
    cipher = AES.new(create_hash(passphrase), AES.MODE_EAX, password[1])
    decrypted_password = cipher.decrypt(password)
    return decrypted_password


# passed
def mask_password(config_object):
    """removes my password when I save the config"""
    config_object['password']['command'] = 'lol'
    config_object['password']['result'] = 'lol'
    return config_object


# passed
def save_the_state(applied_config, original_config):
    key_value_string = 'config'
    applied_config_converted = elements_to_first_level(applied_config, key_value_string)
    original_config_converted = elements_to_first_level(original_config, key_value_string)
    list_of_elements = original_config.keys()
    for i in list_of_elements:
        if i in applied_config_converted:
            original_config_converted[i] = applied_config_converted[i]
    return {'config': original_config_converted}


# =========================================================================

def send_commands_and_recieve_standardized_output(nornir_object, device_name, config, file_path):
    single_device = filter_by_name(nornir_object, device_name)
    processed_config = save_the_output(config_action(single_device, get_command_list(config)), config)
    config_path = str.join('', (file_path, '\\', 'read.json'))
    write_to_config(processed_config, config_path)
    return processed_config


# Generic code basically does the following:
# load starting config
# Grabs the 'state' of the device. It should be generic.
# Overwrite the password
# if there's no state, create the old state
# write the 'config'
# read the 'state'
# save the 'state'
# second run
# compare the old with the new
# difference the two
# write the 'config'
