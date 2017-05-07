##############################
## Pull label, %FP, and %TP from the files found in results
##      - For each, create row in dataframe label, %fp, %tn
## Plot the data on an ROC curve (save in summaries)
## List all of the data in order desc (TP + (1-FP)) (save in summaries)
##############################

'''
cd /var/www/git/NLP/Word-Subject-Classification/2_classify/3_analyze_classification/; python3 summarize.py round_four
'''

from os import listdir
from os.path import isfile, join
import numpy as np;
import pandas as pd;
import sys;
import matplotlib.pyplot as plt
from tabulate import tabulate

#######################################
## User Inputs
#######################################
RESULTS_ROOT = "results/test_1_all/";
SUMMARY_DELTA_MOD = sys.argv[1];
FORCE_SHOW_ALL_REPEATS = False;


print('Detecting all files....');
#######################################
## Detect all results in results directory
#######################################
results_root = RESULTS_ROOT;
result_files = [f for f in listdir(results_root) if isfile(join(results_root, f))]
#result_files.remove('.gitignore');
result_files_old = result_files;
result_files = [s for s in result_files_old if s.endswith(".csv")]
print("Found ", len(result_files), " files.");
#print(len(result_files));
#exit();


print('Loading all relevant results...');
#######################################
## Load All Results
#######################################
full_data = [];
wanted_traits = ["delta_mod", "TP", "FP", "TN", "FN", "KERNEL", "degree", "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "source_mod", "classifier_choice", "final_cost_found"]
convert_to_float = [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1]
repeat_considered = False; ## If repeats exist, we'll need to get the lowest cost repeat
for this_file in result_files:
    ####
    ## For each file, find delta_mod, %TP, and %FP
    ####
    parts_found = 0;
    data_row = dict();
    with open(RESULTS_ROOT + this_file, 'r') as fp:
        source_lines = fp.readlines();
        for line in source_lines:
            parts = line.rstrip().replace(" ", "").split(":");
            #print(parts);
            this_base = parts[0];
            if(this_base in wanted_traits):
                #print(this_base);
                this_value = parts[1];
                if(convert_to_float[wanted_traits.index(this_base)] == 1):
                    this_value = float(this_value);
                    
                if(this_base == "delta_mod"):
                    potential_repeat_base = this_value.split("_r");
                    #print(potential_repeat_index);
                    if(len(potential_repeat_base) > 1):
                        repeat_considered = True;
                        repeat_base = potential_repeat_base[0];
                        data_row["base"] = repeat_base;
                    
                data_row[this_base] = this_value;
                parts_found += 1;
            if(parts_found == len(wanted_traits)):
                break;
    #print(this_file);
    #print(data_row);
    
    #data_row['goodness'] = data_row['%TP'] - data_row['%FP'];
    data_row["%FP"] = data_row["FP"] / (data_row["TN"] + data_row["FP"]); #False Positive Rate, Percent of Negatives Labeled Positive: 1 - Negative_Recall.  
    data_row["%TP"] = data_row["TP"] / (data_row["TP"] + data_row["FN"]); #True Positive Rate, Percent of Positives Labeled Positive: Positive_Recall.
    data_row['precision'] = data_row['TP'] / (data_row['TP'] + data_row['FP'] + 1); # Positive Prediction Value; PPV
    data_row["F1"] = 2*data_row["TP"]/(2*data_row["TP"] + data_row["FP"] + data_row["FN"]); #1/(1/data_row["precision"] + 1/data_row["%TP"]);
    data_row['goodness'] = data_row["F1"];
    full_data.append(data_row);
if(FORCE_SHOW_ALL_REPEATS):
    repeat_considered = False;
'''
if(repeat_considered):
    the_columns = ['delta_mod', 'base', 'precision', '%TP', '%FP', "TP", "FP", 'goodness', "KERNEL", "degree", "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "source_mod", "classifier_choice", "final_cost_found"];
else:
    the_columns = ['delta_mod', 'precision', '%TP', '%FP', "TP", "FP", 'goodness', "KERNEL", "degree", "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "source_mod", "classifier_choice", "final_cost_found"];
'''
the_columns = ['delta_mod', 'precision', '%TP', '%FP', "TP", "FP", "TN", "FN", 'goodness', "source_mod", "classifier_choice", "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "source_mod"];

results = pd.DataFrame(full_data, columns = the_columns);
'''
repeat_considered = False;
if(repeat_considered):
    if( not (np.isnan(results['final_cost_found'].tolist()[0])) ): ## if final_cost exists (does not for rf)
        ## Group by base and only return min cost value one
        results = results.sort(['final_cost_found'], ascending=[0]);
        results = results.groupby('base').first();
    else: 
        results = results.drop('base', axis=1);
'''
results = results.sort(['goodness'], ascending=[0]);

results.index = range(1,len(results) + 1);
def write_to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)
print('Writing relevant results to csv file...');
write_to_fwf(results, "summaries/"+SUMMARY_DELTA_MOD+".csv");
#print(results);

print('Generating and saving plot...');
#######################################
## Plot the graph
#######################################
x_ROC = results["%FP"].tolist();
y_ROC = results["%TP"].tolist();
gradient_value = results["goodness"].tolist();
#print(x_ROC);
#plt.plot(x_ROC, y_ROC)
plt.scatter(x_ROC, y_ROC, c=gradient_value)
#plt.gray()
plt.plot(x_ROC[0], y_ROC[0], 'ro');
plt.ylabel('%TP')
plt.xlabel('%FP')
#plt.savefig("summaries/"+SUMMARY_DELTA_MOD+"_ROC.png")
#plt.show()

## Clear graph
plt.gcf().clear()
#######################################
## Plot the graph
#######################################
x_ROC = results["%TP"].tolist();
y_ROC = results["precision"].tolist();
gradient_value = results["goodness"].tolist();
#print(x_ROC);
#plt.plot(x_ROC, y_ROC)
plt.scatter(x_ROC, y_ROC, c=gradient_value)
#plt.gray()
plt.plot(x_ROC[0], y_ROC[0], 'ro');
plt.ylabel('Precision')
plt.xlabel('%TP - Recall')
plt.savefig("summaries/"+SUMMARY_DELTA_MOD+"_PR.png")
#plt.show()
