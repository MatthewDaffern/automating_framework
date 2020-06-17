import Libraries.configuration as functions

nornir_object = functions.init_nornir('config.yaml')

for i in nornir_object.inventory.hosts:
    print(i)


def expose_password_attribute(nornir_object, passphrase):
    list_of_hosts = list(nornir_object.inventory.hosts)




test = dict()
test['config'] = dict()
test['config']['actual_password'] = 'lol'

result = functions.encrypt_password(test, 'fudge')
result2 = functions.decrypt_password(result, 'fudge')

print(result2)




































filter_group = functions.filter_by_name(nornir_object, 'SG350')

old_dict = dict()

new_dict = dict()

old_dict['config'] = dict()
new_dict['config'] = dict()

old_dict['config']['test1'] = dict()
new_dict['config']['test1'] = dict()

old_dict['config']['test2'] = dict()
new_dict['config']['test2'] = dict()

old_dict['config']['test3'] = dict()
new_dict['config']['test3'] = dict()

old_dict['config']['test1']['command'] = 'checkdb'
new_dict['config']['test1']['command'] = 'checkdb'

old_dict['config']['test2']['command'] = 'show storage'
new_dict['config']['test2']['command'] = 'show storage'

old_dict['config']['test3']['command'] = 'get list'
new_dict['config']['test3']['command'] = 'get list'


old_dict['config']['test1']['result'] = 'sure'
new_dict['config']['test1']['result'] = 'sure'

old_dict['config']['test2']['result'] = '200'
new_dict['config']['test2']['result'] = '100'

old_dict['config']['test3']['result'] = '32'
new_dict['config']['test3']['result'] = 'get list'

'''
differenced_dict = functions.unapplied_parameters(old_dict, new_dict)


applied_dict = functions.save_the_state(differenced_dict, old_dict)

commands = functions.get_command_list(old_dict)


result = functions.config_action(nornir_object, commands)

print(result)

for i in result:
    print(i)
'''