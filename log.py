import time
import datetime
import os
import sys

debug_level = 3   # 0:close  1:error  2:err + debug  3:error + debug + info
is_print_file = True
is_first_log = True
head_len = 33

def get_head_info():
    func_name = sys._getframe(2).f_code.co_name
    line_num = str(sys._getframe(2).f_lineno)
    file_name = sys._getframe(2).f_code.co_filename.split('/')[-1]
    space1 = ' '
    space2 = ':'

    head = file_name + space1 + func_name + space1 + line_num + space2
    return head
def log_write(str):
    global debug_level
    global is_print_file
    global is_first_log
    str = str + '\r'

    if not is_print_file:
        return
    if is_first_log:
        try:
            with open('log.txt', 'w') as fp:
                fp.write(str)
                is_first_log = False
        except:
            return
    else:
        try:
            size = os.path.getsize('log.txt')
            size = size / 1024
            #print('size: %.2f kb' %size)
            if size > 10240:
                return
            with open('log.txt', 'a+') as fp:
                fp.write(str)
        except:
            return

def log_add_time():
    space = ' '
    time = datetime.datetime.now()
    #time= time.strftime("%Y-%m-%d %H:%M:%S")
    time = time.strftime("%H:%M:%S")
    result = time + space
    return result

def loginf(arg):
    global head_len
    if debug_level > 2:
        if type(arg) == int:
            arg = str(arg)
        head_bef = 'INF ' + log_add_time() + get_head_info()
        if len(head_bef) < head_len:
            head_bef = head_bef + ' ' * (head_len-len(head_bef))
        arg = head_bef + arg
        print(arg)
        log_write(arg)

def logdbg(arg):
    global head_len
    if debug_level > 1:
        if type(arg) == int:
            arg = str(arg)
        head_bef = 'DBG ' + log_add_time() + get_head_info()
        if len(head_bef) < head_len:
            head_bef = head_bef + ' ' * (head_len - len(head_bef))
        arg = head_bef + arg
        print(arg)
        log_write(arg)

def logerr(arg):
    global head_len
    if debug_level > 0:
        if type(arg) == int:
            arg = str(arg)
        head_bef = 'ERR ' + log_add_time() + get_head_info()
        if len(head_bef) < head_len:
            head_bef = head_bef + ' ' * (head_len - len(head_bef))
        arg = head_bef + arg
        print(arg)
        log_write(arg)

if __name__ == '__main__':
   for  i in range(0, 1000):
       #logerr(i)
       #logerr('yes:%s%d' % ('oh', 10))
       loginf('你好')
       #loginf('hello')
       #logerr(2)
       #logdbg('你好')
       #loginf('yes: %d' % 4439)