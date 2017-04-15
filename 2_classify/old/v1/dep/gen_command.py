import sys;


string = "";
for i in range(len(sys.argv)):
    if(i == 0):
        continue;
    this_argv = sys.argv[i];
    
    parts = this_argv.split(":");
    if(parts[0] == "name" or parts[0] == "n"):
        n = parts[1];
    elif(parts[0] == "rtrue"):
        rtrue = float(parts[1]);
    elif(parts[0] == "min_freq"):
        min_freq = int(parts[1]);
    elif(parts[0] == "batch_size"):
        batch_size = int(parts[1]);
    elif(parts[0] == "learning_rate"):
        learning_rate = float(parts[1]);
    elif(parts[0] == 'n_hidden_1'):
        n_hidden_1 = int(parts[1]);
    elif(parts[0] == 'n_hidden_2'):
        n_hidden_2 = int(parts[1]);
    elif(parts[0] == 'epochs'):
        epochs = int(parts[1]);
    elif(parts[0] == "runs"):
        runs = int(parts[1]);
    
if 'runs' not in locals():
    runs = 5;
    
args = "cd /var/www/git/Plants/NLP/word2vec/classify/v1/\n";
hyperparamlist = ['n',  'epochs',  'batch_size', 'learning_rate', 'n_hidden_1', 'n_hidden_2', 'min_freq', 'rtrue'];
for i in range(runs):
    args += "python3 classifier_rand.py";
    for param in hyperparamlist:
        if(param == 'n'):
            value = eval(param) + "_" + str(i);
        elif param in locals():
            value = eval(param);
        else:
            continue;
        args += " " + param + ":" + str(value);
    args += "; ";
            

print(args);