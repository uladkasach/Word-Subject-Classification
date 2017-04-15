import sys
import os

def save_classification(results_data_frame,delta_mod = None):
    
    ## Ensure output directory exists
    directory = "results";
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = delta_mod;

    file_name = "results/"+filename + '_neg.csv';
    results_data_frame.sort_values(['pred_0'], ascending=[False], inplace=False).to_csv(file_name, index=False, sep=' ');
    print('done!');

    file_name = "results/"+filename + '_pos.csv';
    results_data_frame.sort_values(['pred_1'], ascending=[False], inplace=False).to_csv(file_name, index=False, sep=' ');
    print('done!');
