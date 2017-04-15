%%http://stackoverflow.com/questions/2856417/reading-a-text-file-in-matlab-line-by-line
%%[numData,textData,rawData] = xlsread(');
clear

file_source = '/var/www/git/Plants/NLP/word2vec/features/embed/results/embeddings_5.6m_basic.csv';
save_dest = '/var/www/git/Plants/NLP/word2vec/features/embed_analysis/mat/embeddings_5.6m_basic.mat';


keys = {};

file = fopen(file_source,'r'); %# open csv file for reading
counter = -1;
while ~feof(file)
    counter = counter + 1;
    line = fgets(file); %# read line by line
    parts = strsplit(line, ' ');
    this_row = zeros(1, 300);
    for i = 1:size(parts, 2)
        this_part = parts(i);
        if(i == 1)
            keys{end+1} = this_part;
            %this_part
        else 
            this_part = str2double(parts(i));
            this_row(i-1) = this_part;
        end
    end
    if exist('embeddings')
        embeddings = [embeddings; this_row];
    else 
        embeddings = [this_row];
    end
    if(mod(counter, 500) == 0)
        counter
    end;
end


if true
    size(keys)
    size(embeddings)
    error('here i am');
end

save(save_dest, 'keys', 'embeddings');