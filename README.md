## Overview
The content of this repository was created for an independent study completed durring spring semester of 2017. A complete writeup of this project can be found in the paper written about it: [Semi-Supervised Labeling and Classification of Words by Semantic Subject](https://github.com/uladkasach/Word-Subject-Classification/blob/master/SemanticSubjectRecognition_FinalDraft.pdf)

## More details
Goal:

- (*deprecated*) Build WordVectors for Classification
    - Idea : wordvectors trained on subject related corpus will perform better
    - Implementation : the web application located under `source` performs web-scraping of websites, tokenization of scrapped data, recording into database, and exporting lists of tokenized words of any size (can choose 1M or 12M words for export) and any tokenization type (keep stop words, remove stop words, etc). 
    - Result : Either the idea was wrong, the corpus must be much larger, or better tokenization (bigram, numerics) should be employed. GoogleNews-wordvectors perform much better.
    - This goal has been deprecated: project has migrated to focus on the classification of 'good' word vectors.
    
- Classify words based on subject
    - Implementation : 
        - `features` directory contains all functionality relating to converting `source` exports to embeddings, analyzing embeddings, and labeling words - to create features that can be used in classification. 
        - `classify` contains a classification 'pipeline', including: 
            - splitting source data into test and train sets (with oversampling, undersampling, SMOTE, and more options),
            - several different classification algorithms (nn, rf, svm, knn), 
            - classification analysis scripts - one calculating statistics (TP, %TP, etc) for each classification and another summarizing the statistics of many different classifications in order to compare classifier performance (-vs- classifyer types and hyperparameters)
            - automatic classification scheduling - where its possible to schedule several combinations of data_splits to be created and several enumerations of hyperparameters for each classifier to train and test on those data splits, and then have their results by analyzed - all with one command. (Removes babysitting of hyperparameter tuning and classification comparisions).
                - Example:
                    - The following code will create 6 train/test splits of data and run 3 classifiers with, for the example of the neural net, 250 (1x2x5x5x5) hyperparameter sets on each train/test split data. 
                    - Note, this scheduler takes a 'parallel' argument which enables how ever many classifications as desired to run simultaniously untill completion
                    ```
                        ###########################
                        ## Add split arguments - the splits will be generated and all will be used for each classification_argument set
                        ###########################
                        split_arguments.append({
                            "sampling" : ["SMOTE"],
                            "SM" : [3, 8, 15],
                        })
                        split_arguments.append({
                            "sampling" : ["over"],
                            "SM" : [3, 8, 15],
                        })
                        #############################
                        ## Add classification arguments
                        ###########################
                        classification_arguments.append({
                            "classifier_choice" : ["rf"],
                            "rtrue" : [1, 5, 10, 20, 30, 40, 50 ],
                        })
                        classification_arguments.append({
                            "classifier_choice" : ["nn"],
                            "epochs" : [400],
                            "learning_rate" : [0.1, 0.025],
                            "n_hidden_1" : [40, 20, 10, 5, 2],
                            "n_hidden_2" : [40, 20, 10, 5, 2],
                            "rtrue" : [1, 10, 30, 50],
                        })
                        classification_arguments.append({
                            "classifier_choice" : ["svm"],
                            "kernel" : ["linear"],
                        })
                    ```
    
    - Starting with a subject of "plants" as in "houseplants", "gardening", etc.
    
    
    
    
    
