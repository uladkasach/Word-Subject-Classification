import subprocess;
import dynamic;
import sys;

import multiprocessing as mp
import time
import parallel_queue



############################
## Enumerate every set of the argument options
############################
def recursive_list_enumerator(data, string_so_far = None, name_string_so_far = None, key_list = None):
    if(key_list is None):
        key_list = list(data.keys());
        key_list = sorted(key_list);
         
    if(string_so_far is None):
        string_so_far = "";
    if(name_string_so_far is None):
        name_string_so_far = "";
    
    #logic, run this function for every value of each key in data. Reduce list that is passed by the key just 'evaluated'
    if(len(key_list) == 0):  return [string_so_far], [name_string_so_far];
    this_key = key_list[0];
    new_key_list = key_list[1:]
    
    these_strings = [];
    these_name_strings = [];
    for this_value in data[this_key]:
        new_string_part = str(this_key) + ":" + str(this_value) + " ";
        new_name_string_part = "";
        if(name_string_so_far != ""):
            new_name_string_part += "-";
        new_name_string_part += str(this_key) + str(this_value);
        
        new_result, new_name_result = recursive_list_enumerator(data, string_so_far + new_string_part, name_string_so_far + new_name_string_part, key_list = new_key_list)
        these_strings.extend(new_result);
        these_name_strings.extend(new_name_result);
        
    return these_strings, these_name_strings;

    
def generate_classify_and_analyze_command_chains(enumerations, classify_base,  analyze_base, repeats_per_set, set_title = None, limit = -1):
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
            this_classify_command = classify_base + " name:" + this_name + " " + enum + "&& ";
            this_analyze_command = analyze_base + " name:"+this_name + "; ";
            this_command_full = this_classify_command + this_analyze_command;
            command_chains.append(this_command_full);
        if(index == limit -1):
            break;
    return command_chains;

def generate_split_data_command_chains(split_enumerations, split_names, split_base, repeats_per_set, set_title = None, limit = -1):
    ###########################, 
    ## For each split enumeration, generate all the command chains for that split
    ###########################
    command_chains = [];
    split_source_names = [];
    for index in range(len(split_enumerations)):
        enum = split_enumerations[index];
        for repeat_index in range(repeats_per_set):
            this_name = split_names[index];
            this_name = this_name + "_r" + str(repeat_index); 
            if(set_title is not None):
                this_name = set_title + "_" + this_name;
                
            this_split_command = split_base + " name:" + this_name + " " + enum + "; ";
            command_chains.append(this_split_command);
            split_source_names.append(this_name);
        if(index == limit -1):
            break;
    return command_chains, split_source_names;
        
if __name__ == '__main__':
    
    
    '''
    cd /var/www/git/NLP/Word-Subject-Classification/2_classify/4_scheduler/; python3 schedule.py seconds_per_chain:180 parallel:2 dev_mode:true
    '''

    #########################################################
    ## Read Arguments
    #########################################################
    if(sys.argv[1] == "-h"):
        print ("delta_mod classifier_dir_mod data_source_type");
        exit();
    arguments = dict();
    acceptable_arguments = ['set_title',  'repeats_per_set', 'repeats_per_split_set', 'seconds_per_chain', 'parallel', 'split_parallel', 'dev_mode'];
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
    seconds_per_chain = 180;
    PARALLEL_PROCESSES = 1;
    repeats_per_set = 3;
    split_enumerations = None;
    classification_enumerations = None;
    dev_mode = 'false';
    repeats_per_split_set = 1;
    
        
    #########################################################
    ## Update data to arguments
    #########################################################
    if('set_title' in arguments): set_title = arguments['set_title'];
    if('repeats_per_set' in arguments): repeats_per_set = int(arguments['repeats_per_set']);
    if('repeats_per_split_set' in arguments): repeats_per_split_set = int(arguments['repeats_per_split_set']);
    if('seconds_per_chain' in arguments): seconds_per_chain = int(arguments['seconds_per_chain']);
    if('parallel' in arguments): PARALLEL_PROCESSES = int(arguments['parallel']);
    if('dev_mode' in arguments): dev_mode = bool(arguments['dev_mode']);
    if('split_parallel' in arguments): 
        SPLIT_PARALLEL_PROCESSES = int(arguments['split_parallel']);
    else:
        SPLIT_PARALLEL_PROCESSES = PARALLEL_PROCESSES;
        
    ###########################################################
    ## Ensure that dynamic arguments are properly initialized
    ###########################################################
    assert isinstance(dynamic.split_arguments, list);
    assert isinstance(dynamic.classification_arguments, list);
    for argument_set in dynamic.classification_arguments:
        assert 'classifier_choice' in argument_set;
        assert isinstance(argument_set['classifier_choice'], list);
        assert 'source_mod' not in argument_set; # ensures same source used for all classification
    
    
    ########################################
    ## Genereate split data command chains if required
    ########################################
    split_command_chains = [];
    if(not hasattr(dynamic, 'source_mod') or dynamic.source_mod is None): ## Split arguments dont need to be set if split_source is defined
        print("\n Source_mod not defined in split arguments, generating split data commaand chains...");
        split_base = "cd /var/www/git/NLP/Word-Subject-Classification/2_classify/1_split_data; python3 split_data.py "; 
        split_enumerations = [];
        split_names = [];
        for argument_set_index, argument_set in enumerate(dynamic.split_arguments):
            these_split_enumerations, these_split_names = recursive_list_enumerator(argument_set);
            split_enumerations.extend(these_split_enumerations);
            split_names.extend(these_split_names);
        split_command_chains, split_source_names = generate_split_data_command_chains(split_enumerations, split_names, split_base, repeats_per_split_set, set_title = set_title);
        print(split_command_chains[0:2]);
        print("Number of split command chains: ", len(split_command_chains));
        ### Modify Classification Arguments to use the split_source given
        dynamic.source_mod = split_source_names;
        #print(dynamic.classification_arguments);
        #exit();
        
    #########################################
    ## Generate Classification and Analysis Command Chains
    #########################################
    print('\n Generating classification and Analysis command chains...');
    cAndA_command_chains = [];
    for argument_set_index, argument_set in enumerate(dynamic.classification_arguments):
        ## Define argument_set_title to prevent overwriting
        argument_set_title = "Ar"+str(argument_set_index);
        if(set_title is not None):
            argument_set_title = set_title + "_" + argument_set_title;
        ## Define source_mod arguments
        argument_set["source_mod"] = dynamic.source_mod;
        ## Handle classifier_choice 
        classifier_choice = argument_set["classifier_choice"][0];
        this_classify_base = "cd /var/www/git/NLP/Word-Subject-Classification/2_classify/2_train_and_classify/"+classifier_choice+"/&& python3 classifier.py "; 
        this_analyze_base = "cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/&& python3 analyze.py classifier_dir_mod:"+classifier_choice+" ";
        these_classification_enumerations, _ = recursive_list_enumerator(argument_set);
        these_cAndA_command_chains = generate_classify_and_analyze_command_chains(these_classification_enumerations, this_classify_base, this_analyze_base, repeats_per_set, set_title = argument_set_title );
        cAndA_command_chains.extend(these_cAndA_command_chains);
    print(cAndA_command_chains[0:2]);
    print("Number of classification and analysis command chains: ", len(cAndA_command_chains));
    
    ##########################################
    ## Combine command chains
    ##########################################
    print('\n Combining all command chains...');
    command_chains = [];
    command_chains.extend(split_command_chains);
    command_chains.extend(cAndA_command_chains);
    #print(command_chains[0:2]);
    
    ###########################################
    ## Output stats if defined
    ###########################################
    if(seconds_per_chain is not None):
        print("\n Outputting stats...");
        seconds = seconds_per_chain * len(command_chains);
        print(len(command_chains), " total command chains, \nat ", seconds_per_chain, " sec per => total of ", seconds, "seconds = ", seconds/60, "minutes = ", seconds/3600, " hours"); 
        print(" With parallelism, at ", PARALLEL_PROCESSES, ", this reduces to ", seconds/3600/PARALLEL_PROCESSES, " hours");
    
    ############################################
    ## Run queue if not in dev mode
    ############################################
    f = open("dev_output.txt", 'w+')
    for command in command_chains:
        f.write(command+'\n');  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    if(dev_mode == 'false'):
        if(split_command_chains != []):
            print('Running split_command chains...');
            parallel_queue.begin_parallel_commands(split_command_chains, SPLIT_PARALLEL_PROCESSES);
        print('Running classification and analysis chains...');
        parallel_queue.begin_parallel_commands(cAndA_command_chains, PARALLEL_PROCESSES);
    
