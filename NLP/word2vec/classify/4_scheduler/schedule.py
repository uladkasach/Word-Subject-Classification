import subprocess;
import dynamic;
import sys;

import multiprocessing as mp
import time




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

def return_classification_command(base, split_data_source, name, arguments):
    this_classify_command 
    return this_classify_command;
    
def generate_command_chains(enumerations, classify_base, split_data_source, analyze_base, repeats_per_set, split_command = "", set_title = None, limit = -1):
    if(split_data_source == None):
        print("Split data source can not be empty for classification. Error");
        exit();
    ###########################
    ## For each enumeration, build chain of commands required. (classify, analyze)
    ###########################
    index = -1;
    command_chains = [];
    for enum in enumerations:
        index+=1;
        for repeat_index in range(dynamic.repeats_per_set):
            this_name = "enum_"+str(index) + "_r" + str(repeat_index); 
            if(set_title is not None):
                this_name = set_title + "_" + this_name;
            this_split_command = split_command;
            this_classify_command = classify_base + " source_mod:" + split_data_source + " name:" + this_name + " " + enum + "; ";
            this_analyze_command = analyze_base + "name:"+this_name + "; ";
            this_command_full = this_split_command + this_classify_command + this_analyze_command;
            command_chains.append(this_command_full);
        if(index == limit -1):
            break;
    return command_chains;

        
if __name__ == '__main__':
    PARALLEL_PROCESSES = int(sys.argv[1]);
    
    #########################################################
    ## Read Arguments
    #########################################################
    if(sys.argv[1] == "-h"):
        print ("delta_mod classifier_dir_mod data_source_type");
        exit();
    arguments = dict();
    acceptable_arguments = ['set_title', 'classifier_choice', 'repeats_per_set', 'seconds_per_chain'];
    for i in range(len(sys.argv)):
        if(i == 0):
            continue;
        this_argv = sys.argv[i];
        parts = this_argv.split(":");
        this_name = parts[0];
        this_value = parts[1];
        if(this_name not in acceptable_arguments):
            print(this_name, " is not an acceptable argument. Error.");
            exit();
        arguments[this_name] = this_value;
        
    ########################################################
    ## Set Defaults
    ########################################################
    set_title = None;
    seconds_per_chain = None;
    
        
    #########################################################
    ## Update data to arguments
    #########################################################
    if('classifier_choice' in arguments):
        classifier_choice = arguments['classifier_choice'];
    else:
        print("classifier_choice is required. Error.");
        exit();    
    if('set_title' in arguments): set_title = arguments['set_title'];
    if('repeats_per_set' in arguments): repeats_per_set = int(arguments['repeats_per_set']);
    if('seconds_per_chain' in arguments): seconds_per_chain = int(arguments['seconds_per_chain']);
    
    
    
    keys = list(dynamic.classification_arguments.keys());
    keys = sorted(keys);
    classification_enumerations = recursive_list_enumerator(keys, dynamic.classification_arguments, "");
    
    
    if(dynamic.classifier_choice == "nn"):
        split_data_source = "f10_t30_ran";
        classify_base = "cd /var/www/git/Plants/NLP/word2vec/classify/2_train_and_classify/nn/; python3 classifier.py "; 
        analyze_base = "cd /var/www/git/Plants/NLP/word2vec/classify/3_analyze_classification/; python3 analyze.py classifier_dir_mod:nn ";
        command_chains = generate_command_chains(classification_enumerations, classify_base, split_data_source, analyze_base, repeats_per_set, set_title = set_title, limit = 1);
        
    if(dynamic.classifier_choice == "random_forest"):
        split_data_filebase = "f10_t30_ran";
        classify_base = "cd /var/www/git/Plants/NLP/word2vec/classify/2_train_and_classify/random_forest/; python3 classifier.py source_mod:" + split_data_filebase + " "; 
        analyze_base = "cd /var/www/git/Plants/NLP/word2vec/classify/3_analyze_classification/; python3 analyze.py classifier_dir_mod:random_forest ";
    

    if(dynamic.seconds_per_chain is not None):
        seconds = dynamic.seconds_per_chain * len(command_chains);
        print(len(command_chains), " total command chains, \nat ", dynamic.seconds_per_chain, " sec per => total of ", seconds, "seconds = ", seconds/60, "minutes = ", seconds/3600, " hours"); 
        print(" With parallelism, at ", PARALLEL_PROCESSES, ", this reduces to ", seconds/3600/PARALLEL_PROCESSES, " hours");
    
    print(command_chains);
    
    if(False):
        parallel_queue.begin_parallel_commands(command_chains, PARALLEL_PROCESSES);