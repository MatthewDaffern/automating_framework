import datetime
import json
import paramiko
import subprocess
from Crypto.Cipher import AES
from hashlib import sha3_256

# The goal of this script is to configure a site all at the exact same time. The actual logic is handled by the scripts.


# ================================================================================================================
# Workflow functions
# PASS
def main_menu():
    """main menu"""
    print('welcome to the automation script\n\n'
          'please let me know whether you wish to configure one device or all of them\n'
          'if you have a new config, please type in new.')
    result = input()
    if result == 'one':
        return result
    if result == 'all':
        return result
    if result == 'new':
        return result
    else:
        return main_menu()


# Pass
def one_device(device_list):
    """logic for configuring only one device. Returns one environment config."""
    list_of_device_names = list(device_list['site'].keys())
    qty = range(0, len(list_of_device_names))
    for i in qty:
        print(str.join('', (str(i), ': ', list_of_device_names[i])))
    choice = input('\n\nOf the above devices which do you want to configure? Please type in the number.\n\n')
    if choice not in list(map(lambda x: str(x), list(qty))):
        return one_device(device_list)
    else:
        return list_of_device_names[int(choice)]


# pass
def all_devices(device_list):
    """just for printing."""
    list_of_device_names = list(device_list['site'].keys())
    qty = range(0, len(list_of_device_names))
    for i in qty:
        print(str.join('', (str(i), ': ', list_of_device_names[i])))
    print('\n\nFor your information, you will be configuring every single device in the configuration file. '
          '(helpfully put in a list for you above.)'
          '\nIf you do not wish to configure the whole "site", press ctrl+c, otherwise press enter to acknowledge')
    input()
    return list_of_device_names


# Pass
def one_or_all_or_new(choice_input, environment_config):
    """Just logic."""
    if choice_input == 'one':
        return one_device(environment_config)
    if choice_input == 'all':
        return all_devices(environment_config)
    if choice_input == 'new':
        return encrypt_config(environment_config)


# ================================================================================================================
# Backend Stuff
def encrypt_config(environment_config):
    """Says what it's intended for"""
    password = create_hash(input("\n\nPlease enter in the password."
                                 "If you forget this, you'll have to rewrite the config\n\n"))
    print('encrypting the config now. This will exit when successful')
    return encrypt(environment_config, password)


def local_script(device_name, environment_config):
    """If I want to automate a HPE Server configuration, I have to use their tool, so this needs to be run locally."""
    if environment_config['site'][device_name]['remote_or_local_script'] == 'local':
        result = list()
        for i in environment_config['site'][device_name]['temporary_write_config']:
            result.append(subprocess.run(i, capture_output=True))
        environment_config['site'][device_name]['config_result'] = result
        return result
    else:
        return environment_config


def apply_local_config(device_name, environment_config):
    """this is just logic for the local script function."""
    return local_script(device_name, environment_config)


def apply_config(device_name, username, password, config_lines, environment_config):
    """"apply's a remote config using password based authentication and paramiko"""
    if environment_config['site'][device_name]['remote_or_local_script'] == 'remote':
        client = paramiko.client.SSHClient()
        client.connect(environment_config['site'][device_name]['hostname'], username=username, password=password)
        result = list()
        for i in config_lines:
            stdin, stdout, stderr = client.exec_command(i)
            result.append(stdout)
        environment_config['site'][device_name]['config_result'] = result
        return environment_config
    else:
        return environment_config


def configure_action(device_name, environment_config):
    """ configures a single device"""
    return apply_config(device_name,
                        environment_config['site'][device_name]['username'],
                        environment_config['site'][device_name]['password'],
                        environment_config['site'][device_name]['temporary_write_config'],
                        environment_config)


def read_action(device_name, environment_config):
    """ reads a single device"""
    return apply_config(device_name,
                        environment_config['site'][device_name]['username'],
                        environment_config['site'][device_name]['password'],
                        environment_config['site'][device_name]['read_config'],
                        environment_config)


def configure_device(device_list, environment_config):
    """configures all devices in device list, regardless of whether or not it's a single or multiple device count."""
    config_storage = environment_config
    for i in device_list:
        config_storage = configure_action(i, apply_local_config(i, config_storage))
        """this below statement should be it's own function. This is incredibly unclear"""
        config_storage['site'][i]['read_config'] = read_action(i, config_storage)
    return config_storage


def check_state(device_list, environment_config):
    device = read_action(device_list, environment_config)
    '''for i in thing that needs to be commented, and probably won't work until I clean this code up.' \
            'Basically just check the state of the read config and store it to a read_result. I kind messed it up.
            The goal is to clean the config up during testing and make it so that my config workflow is sensible,
            the steps for the config are:
            1. read
            2. reduce
            3. write'
    '''


def final_analysis(environment_config, device_list, log_location):
    """all this does is print output of everything configured to a single file"""
    log = open(log_location, 'a+')
    log.write(str.join('', ('=====  ', str(datetime.date.today()), '  ', str('=' * 50), '\n')))
    for i in device_list:
        log.write(str.join('\n', environment_config['site'][i]['config_result']))
    log.close()
    print('logs can be found at the following place:\n\n')
    print(str(log_location))
    return environment_config


# ================================================================================================================
# Encrypting strings
# Pass
def create_hash(pass_phrase_input):
    """AES requires a fixed byte length for any password input. I think this one is 32 bytes."""
    hash_object = sha3_256(str.encode(pass_phrase_input))
    return hash_object.digest()


# Pass
def encrypt_string(string_input, pass_phrase_input):
    """Since we don't actually want to do file operations(it's insecure), we'll be dumping the file into memory and encrypting/decrypting only the strings."""
    cipher = AES.new(create_hash(pass_phrase_input), AES.MODE_EAX)
    encrypted_password = cipher.encrypt(str.encode(string_input))
    return encrypted_password, cipher.nonce


# Pass
def decrypt_string(encrypted_tuple, pass_phrase_input):
    """Since we don't actually want to do file operations(it's insecure), we'll be dumping the file into memory and encrypting/decrypting only the strings."""
    cipher = AES.new(create_hash(pass_phrase_input), AES.MODE_EAX, encrypted_tuple[1])
    decrypted_password = bytes.decode(cipher.decrypt(encrypted_tuple[0]))
    return decrypted_password


# ================================================================================================================
# Encrypting/decrypting config.
def decrypt(environment_config, password):
    """wrapping the 'string' encryption and decryption so that the file is properly handled'"""
    device_list = environment_config['site'].keys()
    for i in device_list:
        environment_config['site'][i]['username'] = decrypt_string(environment_config['site'][i]['username'], password)
        environment_config['site'][i]['password'] = decrypt_string(environment_config['site'][i]['password'], password)
        environment_config['site'][i]['hostname'] = decrypt_string(environment_config['site'][i]['hostname'], password)
    return environment_config


def encrypt(environment_config, password):
    device_list = environment_config['site'].keys()
    for i in device_list:
        environment_config['site'][i]['username'] = encrypt_string(environment_config['site'][i]['username'], password)
        environment_config['site'][i]['password'] = encrypt_string(environment_config['site'][i]['password'], password)
        environment_config['site'][i]['hostname'] = encrypt_string(environment_config['site'][i]['hostname'], password)
    return environment_config
# ================================================================================================================


def main(environment_config, log_location):
    """messy messy logic."""
    choice = main_menu()
    if choice == 'new':
        one_or_all_or_new(choice, environment_config)
        return environment_config
    password = create_hash(input('please input your password\n'))
    environment_config_decrypted = json.loads(decrypt(environment_config, password))
    device_list = one_or_all_or_new(choice, environment_config_decrypted)
    result = final_analysis(configure_device(device_list, environment_config_decrypted),
                            list(environment_config_decrypted['site'].keys()),
                            log_location)
    return encrypt(result, password)


if __name__ == '__main__':
    main('config.json', 'result.log')
