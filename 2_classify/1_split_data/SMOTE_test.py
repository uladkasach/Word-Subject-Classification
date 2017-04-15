import split_support;
import numpy;
import pandas;


from sklearn import datasets;
import matplotlib.pyplot as plt;
Xi, yi = datasets.make_blobs(500, random_state=1111);
print(yi[0:10]);
Xi = Xi.astype(numpy.float32)
the_data = Xi;
K = 3;
#print(the_data);

SMOTE = True;
if(SMOTE == True):
    df = pandas.DataFrame(the_data);
    #print(df.head());
    synth_data = split_support.generate_SMOTE_samples(df, 1, dev_test = True);
    #print(synth_data.head());
    
    K += 1;
    yi_synth = numpy.array([3] * synth_data.shape[0]);
    synth_data = synth_data.as_matrix();
    
    #print(yi_synth);
    #print(len(yi_synth));
    
    yi = numpy.concatenate((yi, yi_synth), axis=0);
    ##Xi.extend(synth_data);
    Xi = numpy.concatenate((Xi, synth_data), axis=0);
    #print(Xi);
    #print(Xi.shape);
    
    
    #print(yi);
    #print(len(yi));
        
plt.scatter(*Xi.T, c='k', lw=0);
plt.scatter(*Xi.T, c=yi, lw=0, vmax=K + 0.5, label='data');
plt.legend(scatterpoints=3);
plt.show()
