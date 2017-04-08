words = [];

f = open('several_input.txt');
for line in f.readlines():
    line = line.rstrip();
    words.append(line);
    print(line);
    
string = "";
for word in words:
    string += ('cd /var/www/git/Plants/NLP/word2vec/features/embed_analysis/KNN; python3 KNN.py ../GoogleNews-vectors-negative300.txt 250 ' + word + ' google;');
    
print (string);


##cd /var/www/git/Plants/NLP/word2vec/features/embed_analysis/KNN