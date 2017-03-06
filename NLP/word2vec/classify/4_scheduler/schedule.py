import subprocess;
import dynamic;
import sys;

import multiprocessing as mp
import time


PARALLEL_PROCESSES = int(sys.argv[1]);


############################
## Enumerate every set of the argument options
############################
def recursive_list_enumerator(key_list, data, string_so_far):
    #logic, run this function for every value of each key in data. Reduce list that is passed by the key just 'evaluated'
    if(len(key_list) == 0):  return [string_so_far];
    this_key = key_list[0];
    new_key_list = key_list[1:]
    
    these_strings = [];
    for this_value in data[this_key]:
        new_string_part = str(this_key) + ":" + str(this_value) + " ";
        
        new_result = recursive_list_enumerator(new_key_list, data, string_so_far + new_string_part)
        these_strings.extend(new_result);
        
    return these_strings;
    
keys = list(dynamic.arguments.keys());
keys = sorted(keys);
enumerations = recursive_list_enumerator(keys, dynamic.arguments, "");


###########################
## For each enumeration, build chain of commands required. (classify, analyze)
###########################
split_data_filebase = "f10_t30_ran";
classify_base = "cd /var/www/git/Plants/NLP/word2vec/classify/2_train_and_classify/nn/; python3 classifier.py source_mod:" + split_data_filebase + " "; 
analyze_base = "cd /var/www/git/Plants/NLP/word2vec/classify/3_analyze_classification/; python3 analyze.py ";
index = -1;
command_chains = [];
for enum in enumerations:
    index+=1;
    for repeat_index in range(dynamic.repeats_per_set):
        this_name = "enum_"+str(index) + "_r" + str(repeat_index); 
        this_classify_command = classify_base + "name:" + this_name + " " + enum + "; ";
        this_analyze_command = analyze_base + this_name + "; ";
        this_command_full = this_classify_command + this_analyze_command;
        command_chains.append(this_command_full);
seconds =  3 * len(command_chains);
print(len(command_chains), " total command chains, \nwhich at 3 sec per => total of ", seconds, "seconds = ", seconds/60, "minutes = ", seconds/3600, " hours"); 

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
if __name__ == '__main__':
    globals_running_list = command_chains;
    pool = mp.Pool()
    for i in range(PARALLEL_PROCESSES):
        callback_for_async(None);
    while True:
        print('checking again...');
        if(len(globals_running_list) == 0):
            pool.close();
            pool.join();
            exit();
        time.sleep(20);