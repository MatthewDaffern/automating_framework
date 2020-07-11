import datetime
import json
import paramiko
import subprocess
from Crypto.Cipher import AES
import pathlib
from functools import reduce

def main_menu():
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


def one_device(device_list):
    list_of_device_names = list(device_list.keys())
    qty = range(0, len(list_of_device_names))
    for i in qty:
        print(str.join('', (str(i), ': ', list_of_device_names[i])))
    choice = input('\n\nOf the above devices which do you want to configure? Please type in the number.')
    if choice not in list(map(lambda x: str(x), list(qty))):
        return one_device(device_list)
    else:
        return device_list[list_of_device_names[int(choice)]]


def all_devices(device_list):
    for i in device_list:
        print(i)
    print('\n\nFor your information, you will be configuring every single device in the configuration files. '
          'Those are above'
          '\nIf you do not wish to configure the whole "site", press ctrl+c, otherwise press enter to acknowledge')
    input()
    return device_list


def one_or_all_or_new(choice_input, device_list):
    if choice_input == 'one':
        return one_device(device_list)
    if choice_input == 'all':
        return all_devices(device_list)
    if choice_input == 'new':
        return encrypt_config()


def local_script(device_name, environment_config):
    if environment_config['site'][device_name]['remote_or_local_script'] == 'local':
        result = list()
        for i in environment_config['site'][device_name]['temporary_write_config']:
            result.append(subprocess.run(i, capture_output=True))
        environment_config['site'][device_name]['config_result'] = result
        return result
    else:
        return environment_config


def apply_local_config(device_name, environment_config):
    return local_script(device_name, environment_config)


def apply_config(device_name, username, password, config_lines, environment_config):
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
    return apply_config(device_name,
                        environment_config['site'][device_name]['username'],
                        environment_config['site'][device_name]['password'],
                        environment_config['site'][device_name]['temporary_write_config'],
                        environment_config)


def read_action(device_name, environment_config):
    return apply_config(device_name,
                        environment_config['site'][device_name]['username'],
                        environment_config['site'][device_name]['password'],
                        environment_config['site'][device_name]['read_config'],
                        environment_config)


def configure_device(device_list, environment_config):
    config_storage = environment_config
    for i in device_list:
        config_storage = configure_action(i, apply_local_config(i, config_storage))
    return config_storage


def final_analysis(environment_config, device_list, log_location):
    log = open(log_location, 'a+')
    log.write(str.join('', ('=====  ', str(datetime.date.today()), '  ', str('=' * 50), '\n')))
    for i in device_list:
        log.write(str.join('\n', environment_config['site'][i]['config_result']))
    log.close()
    print('logs can be found at the following place:\n\n')
    print(str(log_location))
    return environment_config


# Pass
def create_hash(pass_phrase_input):
    hash_object = sha3_256(str.encode(pass_phrase_input))
    return hash_object.digest()


# Pass
def encrypt_string(string_input, pass_phrase_input):
    cipher = AES.new(create_hash(pass_phrase_input), AES.MODE_EAX)
    encrypted_password = cipher.encrypt(str.encode(string_input))
    return encrypted_password, cipher.nonce


# Pass
def decrypt_string(encrypted_tuple, pass_phrase_input):
    cipher = AES.new(create_hash(pass_phrase_input), AES.MODE_EAX, encrypted_tuple[1])
    decrypted_password = bytes.decode(cipher.decrypt(encrypted_tuple[0]))
    return decrypted_password


def decrypt(environment_config, password):
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



def main(environment_config, log_location):
    password = create_hash(input('please input your password\n'))
    environment_config_decrypted = json.loads(dump(decrypt(environment_config, password)))
    return encrypt(final_analysis(configure_device(one_or_all_or_new(main_menu(),
                                                      list(environment_config_decrypted['site'].keys())),
                                           environment_config_decrypted),
                          list(environment_config_decrypted['site'].keys()),
                          log_location), password)


if __name__ == '__main__':
    main()
