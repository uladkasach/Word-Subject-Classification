import subprocess;
import dynamic;
import sys;

import multiprocessing as mp
import time

#############################
## Run command chains, X at a time, in parallel
#############################
def change_after_second(this_item):
    #time.sleep(1);
    print (subprocess.Popen(this_item, shell=True, stdout=subprocess.PIPE).stdout.read());
def callback_for_async(result):
    global pool;
    global globals_running_list;
    print("callback running, list size now = ", len(globals_running_list));
    if(len(globals_running_list) == 0): return;
    this_item = globals_running_list[0];
    globals_running_list.remove(this_item);
    pool.apply_async(change_after_second, args = (this_item, ), callback = callback_for_async);
def begin_parallel_commands(command_chains, par_jobs):
    global globals_running_list;
    global pool;
    globals_running_list = command_chains;
    pool = mp.Pool()
    for i in range(par_jobs):
        callback_for_async(None);
    while True:
        print('checking again...');
        if(len(globals_running_list) == 0):
            pool.close();
            pool.join();
            return;
        time.sleep(60);
        
        