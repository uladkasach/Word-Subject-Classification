import sys


def save_classification(results_data_frame,delta_mod = None):
    
    filename = delta_mod;

    file_name = "results/"+filename + '_neg.csv';
    results_data_frame.sort_values(['pred_0'], ascending=[False], inplace=False).to_csv(file_name, index=False);
    print('done!');

    file_name = "results/"+filename + '_pos.csv';
    results_data_frame.sort_values(['pred_1'], ascending=[False], inplace=False).to_csv(file_name, index=False);
    print('done!');
