import sys;
import numpy as np;
import os;

'''
acceptable_arguments = ['name', 'classifier_dir_mod', 'data_source_type'];
cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/; python3 analyze.py name:Ar1_enum_12_r2 classifier_dir_mod:nn
'''


def main(delta_mod, classifier_dir_mod = 'nn', data_source_type = 'test'):
    HYPERPARAM_SOURCE =  '../2_train_and_classify/'+classifier_dir_mod+'/results/'+delta_mod+'_z_hyperparams.txt';
    RESULTS_POS_SOURCE = '../2_train_and_classify/'+classifier_dir_mod+'/results/'+delta_mod+'_'+data_source_type+'_pos.csv';
    RESULTS_NEG_SOURCE = '../2_train_and_classify/'+classifier_dir_mod+'/results/'+delta_mod+'_'+data_source_type+'_neg.csv';

    #FREQUENCIES_SOURCE = "../0_data_source/5.6m_basic_freq_table.csv";
    FREQUENCIES_SOURCE = None;
    if(FREQUENCIES_SOURCE is not None):
        print('Using Frequency Source ', FREQUENCIES_SOURCE);

    #######################################
    ## Load Frequent Words
    #######################################
    if(FREQUENCIES_SOURCE is not None):
        frequency_dict = dict();
        f = open(FREQUENCIES_SOURCE, 'r');
        for line in f.readlines():
            parts = line.rstrip().split(",");
            #print(parts);
            word = parts[0];
            freq = int(parts[1]);
            frequency_dict[word] = freq;
        f.close();

    def parse_results_from(results_source):
        TP = [];
        TN = [];
        FP = [];
        FN = [];
        f = open(results_source, 'r');
        i = -1;
        for line in f.readlines():
            i += 1;
            if(i == 0):
                continue;
            parts = line.rstrip().split(" ");
            #print(parts);
            true_y = int(parts[0]);
            pred_y = int(parts[1]);
            word = parts[2];
            if(pred_y == 0):
                confidence = parts[3];
            else:
                confidence = parts[4];
            confidence = float(confidence);
            if(FREQUENCIES_SOURCE is not None):
                freq = frequency_dict[word];
            else:
                freq = -1;
            data = [true_y, pred_y, word, freq, confidence];
            #print(data);

            #if(i == 200):
            #    exit();

            if(true_y == pred_y):
                if(true_y == 1):
                    TP.append(data);
                else:
                    TN.append(data);
            else:
                if(true_y == 1):
                    FN.append(data);
                else:
                    FP.append(data);
        f.close();
        return TP, TN, FP, FN;

    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    print("Reading Hyperparameters...");
    #######################################
    ## Read hyperparam data
    #######################################
    hyperparameter_data = file_get_contents(HYPERPARAM_SOURCE);
    data_string = hyperparameter_data + "\n";

    print("Parsing Results...");
    #######################################
    ## Parse General Results
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_POS_SOURCE);
    print("Writing Stats...");
    data_string += ("TP:" + str(len(TP)) + "\nTN:" +  str(len(TN)) + "\nFP:" + str(len(FP)) + "\nFN:" + str(len(FN)) + "\n");
    data_string += ("%FP:" + str(len(FP)/(len(TN)+len(FP))) + "\n%TP:" +  str(len(TP)/(len(TP)+len(FN))) + "\n");
    #%F P = F P/(T N +F P )
    #%T P = T P/(T P +F N )
    
    
    #######################################
    ## Write FP Results, In order of decreasing Positive Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_POS_SOURCE);
    print ("Writing FP");
    data_string += "\n---- FP ----\n";
    for data in FP:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";


    #######################################
    ## Write FP Results, In order of decreasing Negative Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_NEG_SOURCE);
    print ("Writing FN");
    data_string += "\n---- FN ----\n";
    for data in FN:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";


    #######################################
    ## Write TP Results, In order of decreasing Positive Confidence
    #######################################
    TP, TN, FP, FN = parse_results_from(RESULTS_POS_SOURCE);
    print ("Writing TP");
    data_string += "\n---- TP ----\n";
    for data in TP:
        data_string += str(data[0]) + "," + str(data[1]) + "," + data[2] + "," + str(data[3]) + "," + str(data[4]) + "\n";


    # Ensure directory exists
    directory = "results";
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = "results/" + data_source_type;
    if not os.path.exists(directory):
        os.makedirs(directory)
    # write results
    myfile = open("results/"+data_source_type+"/"+delta_mod+"_result.csv", "w+");
    myfile.write(data_string);
    myfile.close();


    
if __name__ == "__main__":
    #########################################################
    ## Read Arguments
    #########################################################
    if(sys.argv[1] == "-h"):
        print ("name classifier_dir_mod data_source_type");
        exit();
    arguments = dict();
    acceptable_arguments = ['name', 'classifier_dir_mod', 'data_source_type'];
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
                  
    #########################################################
    ## Set Defaults
    #########################################################
    data_source_type = "test";

    #########################################################
    ## Update data to arguments
    #########################################################
    if('name' in arguments):
        delta_mod = arguments['name'];
    else:
        print("name is required. Error.");
        exit();
    if('classifier_dir_mod' in arguments):
        classifier_dir_mod = arguments['classifier_dir_mod'];
    else:
        print("source_mod is required. Error.");
        exit();    
    if('data_source_type' in arguments): data_source_type = (arguments['data_source_type']);
        
        
    main(delta_mod, classifier_dir_mod, data_source_type);