import subprocess;
import dynamic;
import sys;

import multiprocessing as mp
import time
import parallel_queue




############################
## Enumerate every set of the argument options
############################
def recursive_list_enumerator(data, string_so_far, key_list = None):
    if(key_list is None):
        key_list = list(data.keys());
        key_list = sorted(key_list);
    
    #logic, run this function for every value of each key in data. Reduce list that is passed by the key just 'evaluated'
    if(len(key_list) == 0):  return [string_so_far];
    this_key = key_list[0];
    new_key_list = key_list[1:]
    
    these_strings = [];
    for this_value in data[this_key]:
        new_string_part = str(this_key) + ":" + str(this_value) + " ";
        
        new_result = recursive_list_enumerator(data, string_so_far + new_string_part, key_list = new_key_list)
        these_strings.extend(new_result);
        
    return these_strings;

    
def generate_classify_and_analyze_command_chains(enumerations, classify_base,  analyze_base, repeats_per_set, split_command = "", split_data_source = None, set_title = None, limit = -1):
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
        for repeat_index in range(repeats_per_set):
            this_name = "enum_"+str(index) + "_r" + str(repeat_index); 
            if(set_title is not None):
                this_name = set_title + "_" + this_name;
            this_split_command = split_command;
            this_classify_command = classify_base + " source_mod:" + split_data_source + " name:" + this_name + " " + enum + "&& ";
            this_analyze_command = analyze_base + "name:"+this_name + "; ";
            this_command_full = this_split_command + this_classify_command + this_analyze_command;
            command_chains.append(this_command_full);
        if(index == limit -1):
            break;
    return command_chains;

def generate_chains_with_split(split_enumerations, classification_enumerations, split_base, classify_base, analyze_base, repeats_per_set, set_title = None, split_data_source = None, limit = -1):
    if(split_enumerations is None):
        command_chains = generate_classify_and_analyze_command_chains(classification_enumerations, classify_base, analyze_base, repeats_per_set, set_title = set_title, split_data_source = split_data_source, split_command = "", limit = limit);
        return command_chains;
        
    ###########################, 
    ## For each split enumeration, generate all the command chains for that split
    ###########################
    index = -1;
    command_chains = [];
    for enum in split_enumerations:
        index+=1;
        this_name = "sp"+str(index);
        if(set_title is not None):
            this_name = set_title + "_" + this_name;
            
        this_split_command = split_base + " name:" + this_name + " " + enum + "&& ";
        these_command_chains = generate_classify_and_analyze_command_chains(classification_enumerations, classify_base, analyze_base, repeats_per_set, set_title = this_name, split_data_source = this_name, split_command = this_split_command, limit = limit);
            
            
            
        command_chains.extend(these_command_chains);
        if(index == limit -1):
            break;
            
    return command_chains;
        
if __name__ == '__main__':
    
    #########################################################
    ## Read Arguments
    #########################################################
    if(sys.argv[1] == "-h"):
        print ("delta_mod classifier_dir_mod data_source_type");
        exit();
    arguments = dict();
    acceptable_arguments = ['set_title', 'classifier_choice', 'repeats_per_set', 'seconds_per_chain', 'parallel', 'dev_mode'];
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
    PARALLEL_PROCESSES = 1;
    repeats_per_set = 3;
    split_enumerations = None;
    classification_enumerations = None;
    dev_mode = 'false';
    
        
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
    if('parallel' in arguments): PARALLEL_PROCESSES = int(arguments['parallel']);
    if('dev_mode' in arguments): dev_mode = bool(arguments['dev_mode']);
    
    
    classification_enumerations = recursive_list_enumerator(dynamic.classification_arguments, "");
    
    split_data_source = None; #"f10_t30_ran"; #
    if(split_data_source is None): ## Split arguments dont need to be set if split_source is defined
        split_enumerations = recursive_list_enumerator(dynamic.split_arguments, "");
        
    split_base = "cd /var/www/git/Plants/NLP/word2vec/classify/1_split_data; python3 split_data.py "; 
    classify_base = "cd /var/www/git/Plants/NLP/word2vec/classify/2_train_and_classify/"+classifier_choice+"/; python3 classifier.py "; 
    analyze_base = "cd /var/www/git/Plants/NLP/word2vec/classify/3_analyze_classification/; python3 analyze.py classifier_dir_mod:"+classifier_choice+" ";
    command_chains = generate_chains_with_split(split_enumerations, classification_enumerations, split_base, classify_base, analyze_base, repeats_per_set, set_title = set_title, split_data_source = split_data_source, limit = -1);
    
    print(command_chains[1:3]);

    if(dynamic.seconds_per_chain is not None):
        seconds = dynamic.seconds_per_chain * len(command_chains);
        print(len(command_chains), " total command chains, \nat ", dynamic.seconds_per_chain, " sec per => total of ", seconds, "seconds = ", seconds/60, "minutes = ", seconds/3600, " hours"); 
        print(" With parallelism, at ", PARALLEL_PROCESSES, ", this reduces to ", seconds/3600/PARALLEL_PROCESSES, " hours");
    
    
    if(dev_mode == 'false'):
        parallel_queue.begin_parallel_commands(command_chains, PARALLEL_PROCESSES);