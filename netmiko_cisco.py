from json import load
import netmiko


def import_connection_settings(file_name):
    with open(file_name, 'r+') as config:
        result = load(config)
    return result

#yada yada
def process_connection(config):
    config['connection'] = netmiko.ConnectHandler(**config['config'])
    return config


def process_commands(config_and_connection_object):
    config_and_connection_object['result'] = list()
    for i in config_and_connection_object['commands']:
        config_and_connection_object['result'].append(config_and_connection_object['connection'].send_config_set(i))
    return config_and_connection_object


def print_result(config_connection_and_result_object):
    file_name = 'result.txt'
    file = open(file_name, 'a+')
    for i in config_connection_and_result_object['result']:
        print(i)
        file.write(i)
    file.close()
    print('\n\n\n Your config result is in result.txt')
    return config_connection_and_result_object


def main():
    load_config = import_connection_settings('netmiko_cisco.json')
    processed_connection = process_connection(load_config)
    result = process_commands(processed_connection)
    print_output = print_result(result)
    return print_output


if __name__ == '__main__':
    main()
