
##########################
## Initialize
###########################
split_arguments = [];
classification_arguments = [];


###########################
## Add split arguments - the splits will be generated and all will be used for each classification_argument set
############################
split_arguments.append({
    "sampling" : ["random"],
})
split_arguments.append({
    "sampling" : ["SMOTE"],
    "SM" : [3, 5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["over"],
    "SM" : [3, 5, 8, 10, 15],
})
split_arguments.append({
    "sampling" : ["under"],
    "SM" : [0.9, 0.7, 0.5],
})


#############################
## Add classification arguments
############################# 

## ['name', 'source_mod', 'njobs', 'rtrue', 'dev_mode', 'kernel', 'gamma', 'degree', 'verbose', 'classifier_choice'];
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["linear"],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["poly"],
    "degree" : [2, 3, 4, 5, 6],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["RBF"],
})
classification_arguments.append({
    "classifier_choice" : ["svm"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
    "kernel" : ["sigmoid"],
})

classification_arguments.append({
    "classifier_choice" : ["rf"],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
})
classification_arguments.append({
    "classifier_choice" : ["nn"],
    "epochs" : [400],
    "learning_rate" : [0.1, 0.05, 0.025],
    "n_hidden_1" : [40, 30, 20, 10, 5, 2],
    "n_hidden_2" : [40, 30, 20, 10, 5, 2],
    "rtrue" : [1, 5, 10, 20, 30, 40, 50],
})
