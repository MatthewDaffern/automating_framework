import json
file = open('test.json', 'w+')

config = dict()

config['site'] = dict()
config['site']['firewall'] = dict()
config['site']['server'] = dict()
config['site']['switch'] = dict()
config['site']['firewall']['username'] = 'lol'
config['site']['firewall']['password'] = 'lol'
config['site']['firewall']['config_result'] = ['1',
                                               '2',
                                               '3']
config['site']['firewall']['read_config'] = ['1',
                                             '2',
                                             '3']
config['site']['firewall']['write_config'] = ['1',
                                              '2',
                                              '3']

config['site']['firewall']['temporary_write_config'] = ['1',
                                                        '2',
                                                        '3']
config['site']['firewall']['remote_or_local_script'] = 'remote'

config['site']['firewall']['hostname'] = '127.0.0.1'

print(config)

json.dump(config, file)
file.close()