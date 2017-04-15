This is a classification pipeline


X amount of random data splits are generated from source data.

M Models with H_m sets of hyper parameters train on the data splits and test their results, 
outputting full data results in their respective folders and aggregated summaries on test results in a high level directory
E.G:
- model_name/results/summary -vs- model/results/aggregate






With one command, simulation scheduler will run X amount of simulations for one model for a defined set of hyper parameters
(each set of HP should be run 3-5 times).
s
