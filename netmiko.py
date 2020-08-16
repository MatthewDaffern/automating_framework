from json import load
import netmiko


def import_connection_settings(file_name):
    with open(file_name, 'r+') as config:
        result = load(config)
    return result


def process_connection(config):
    processed_config = dict()
    processed_config['commands'] = config['commands']
    processed_config['connection'] = netmiko.ConnectHandler(config['config'])
    return processed_config


def process_commands(config_and_connection_object):
    config_and_connection = config_and_connection_object
    config_and_connection['result'] = list()
    for i in config_and_connection['commands']:
        config_and_connection['result'].append(config_and_connection['connection'].send_config_set(i))
    return config_and_connection


def print_result(config_connection_and_result_object):
    file_name = 'result.txt'
    file = open(file_name, 'a+')
    for i in config_connection_and_result_object['result']:
        print(i)
        file.append(i)
    file.close()
    print('\n\n\n Your config result is in result.txt')
    return config_connection_and_result_object


def main():
    load_config = import_connection_settings('netmiko.json')
    processed_connection = process_connection(load_config)
    result = process_commands(processed_connection)
    print_output = print_result(result)
    return print_output


if __name__ == '__main__':
    main()
