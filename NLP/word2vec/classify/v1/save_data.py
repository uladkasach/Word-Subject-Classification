import sys


def offer(training_data_frame, results_data_frame, delta = None, delta_mod = None):
    
    #print('Type `save` to save data as csv.') 
    #result = sys.stdin.readline().rstrip();
    result = "";
    if (True or result == 'save'):
        
        
        #print ('Please type filename, data will be saved as {}.csv');
        #filename = sys.stdin.readline().rstrip();
        filename = delta_mod;
        
        if(delta != 'two'):


            file_name = "results/"+filename + '_trainprog.csv';
            training_data_frame.to_csv(file_name, index=False);


            file_name = "results/"+filename + '_results.csv';
            results_data_frame.to_csv(file_name, index=False);
            print('done!');


            file_name = "results/"+filename + '_results_diff.csv';
            grouped = results_data_frame.groupby(['same']);

            #keys = grouped.groups.keys();
            grouped.get_group(0).to_csv(file_name, index=False);
            print('done!');

        else:

            file_name = "results/"+filename + '_freq.csv';
            results_data_frame.to_csv(file_name, index=False);

            file_name = "results/"+filename + '_neg.csv';
            results_data_frame.sort_values(['pred_0'], ascending=[False], inplace=False).to_csv(file_name, index=False);
            print('done!');

            #keys = grouped.groups.keys();
            file_name = "results/"+filename + '_pos.csv';
            results_data_frame.sort_values(['pred_1'], ascending=[False], inplace=False).to_csv(file_name, index=False);
            print('done!');
            
            
        
    else:
        print('Ok. Data not saved.');