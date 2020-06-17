def selection(command_list):
    for i in command_list:
        print(i)


def main_menu(command_list):
    print('Welcome to the tool \n\n\n'
          'please select from the following options \n\n\n')
    selection(command_list)
    choice = input()
    if choice not in command_list:
        selection(command_list)
    # I know this doesn't work.