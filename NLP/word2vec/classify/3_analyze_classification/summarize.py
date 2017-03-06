##############################
## Pull label, %FP, and %TP from the files found in results
##      - For each, create row in dataframe label, %fp, %tn
## Plot the data on an ROC curve (save in summaries)
## List all of the data in order desc (TP + (1-FP)) (save in summaries)
##############################

from os import listdir
from os.path import isfile, join
import pandas as pd;
import sys;
import matplotlib.pyplot as plt
from tabulate import tabulate

#######################################
## User Inputs
#######################################
RESULTS_ROOT = "results/";
SUMMARY_DELTA_MOD = sys.argv[1];


#######################################
## Detect all results in results directory
#######################################
results_root = RESULTS_ROOT;
result_files = [f for f in listdir(results_root) if isfile(join(results_root, f))]
#result_files.remove('.gitignore');
result_files_old = result_files;
result_files = [s for s in result_files_old if s.endswith(".csv")]

#print(len(result_files));
#exit();


#######################################
## Load All Results
#######################################
full_data = [];
wanted_traits = ["delta_mod", "%TP", "%FP", "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "final_cost_found"]
convert_to_float = [0, 1, 1, 1, 1, 1, 1, 1]
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
                if(this_base != "delta_mod"):
                    this_value = float(this_value);
                data_row[this_base] = this_value;
                parts_found += 1;
            if(parts_found == len(wanted_traits)):
                break;
    #print(this_file);
    #print(data_row);
    data_row['goodness'] = data_row['%TP'] - data_row['%FP'];
    full_data.append(data_row);
    
results = pd.DataFrame(full_data, columns = ['delta_mod', '%TP', '%FP', 'goodness',  "learning_rate", "n_hidden_1", "n_hidden_2", "rtrue", "final_cost_found"]).sort(['goodness'], ascending=[0]);
results.index = range(1,len(results) + 1);
#results.to_csv(path_or_buf="summaries/"+SUMMARY_DELTA_MOD+".csv", sep=',', index = False);
def write_to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)
write_to_fwf(results, "summaries/"+SUMMARY_DELTA_MOD+".csv");
#print(results);

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
plt.show()

