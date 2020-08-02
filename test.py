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

config['site']['server']['username'] = 'lol'
config['site']['server']['password'] = 'lol'
config['site']['server']['config_result'] = ['1',
                                               '2',
                                               '3']
config['site']['server']['read_config'] = ['1',
                                             '2',
                                             '3']
config['site']['server']['write_config'] = ['1',
                                              '2',
                                              '3']

config['site']['server']['temporary_write_config'] = ['1',
                                                        '2',
                                                        '3']
config['site']['server']['remote_or_local_script'] = 'remote'

config['site']['server']['hostname'] = '127.0.0.1'

config['site']['switch']['username'] = 'lol'
config['site']['switch']['password'] = 'lol'
config['site']['switch']['config_result'] = ['1',
                                               '2',
                                               '3']
config['site']['switch']['read_config'] = ['1',
                                             '2',
                                             '3']
config['site']['switch']['write_config'] = ['1',
                                              '2',
                                              '3']

config['site']['switch']['temporary_write_config'] = ['1',
                                                        '2',
                                                        '3']
config['site']['switch']['remote_or_local_script'] = 'remote'

config['site']['switch']['hostname'] = '127.0.0.1'





json.dump(config, file)
file.close()

import main as test

result = test.one_or_all_or_new(test.main_menu(), config)
print(result)