import time
import datetime

def print_to_log(log_file_name, string_list):
    log = open(log_file_name, 'a+')
    date_list = list(map(lambda  x: str(x), list(time.localtime(time.time()))))
    final_header = str.join('', ('=====================', 
                                 ' ', 
                                 date_list[1], 
                                 '-', 
                                 date_list[2], 
                                 '-', 
                                 date_list[0], 
                                 '   ', 
                                 date_list[3], 
                                 ':', 
                                 date_list[4], 
                                 ':', 
                                 date_list[5])
                            )
    log.write(final_header + '\n')
    log.write(string_list)
    log.close()
    return string_list

