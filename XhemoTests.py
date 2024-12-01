# ich versuche hier bisschen "ETMM.ipynb" nachzubauen

import construction as cs
from ETN import *
from ETMM import *

# %load_ext autoreload
# %autoreload 2


# Parameters
k = 3    # number of static snapshot used for the constructions of ETN
gap = 299   # temporal gap
label = False # if true, the loaded dataset is labeled
file_name = "InVS13" # name of the file


# Load the temporal graph as a sequence of static NetworkX graphs
data = cs.load_data("Datasets/"+file_name+".dat")
# print(data)
# nodes = cs.individuals(data)
# print(nodes)
if label:
    meta_data = cs.load_metadata("Datasets/metadata/metadata_"+file_name+".dat")
else:
    meta_data = None
    
if label:
    graphs = cs.build_graphs(data,gap=gap,with_labels=label,meta_path="Datasets/metadata/metadata_"+file_name+".dat")
else:
    graphs = cs.build_graphs(data,gap=gap,with_labels=label)
    

# Count ETN or LETN and store the result
S = count_ETN(graphs,k,meta=meta_data)
S = {k: v for k, v in sorted(S.items(), key=lambda item: item[1], reverse=1)}

store_etns(S,file_name,gap,k,label=label)

print(S)                                                                                     # diesen abschnitt mit dem Signature S muss ich mir nochmal genauer anschauen


# load etns 
SS = load_etns(file_name,gap,k,label=label)
assert(SS == S)


S_array = list(S.keys())
#print(S_array[10])
#print(from_ETNS_to_ETN(S_array[10],k=3,meta=None))
draw_ETN(from_ETNS_to_ETN(S_array[10],k=3,meta=None),multiple=False)            #hier verstehe ich noch nicht so ganz, warum der Graph so gezeichnet wird und why S_array[10] benutzt wird, allgemein nochmal anschauen


# plot 6 most frequent ETN
fig_per_row = 6
S_array = list(S.keys())
for i in range(0,6,fig_per_row):
    plt.figure(figsize=(12,3))
    for j in range(fig_per_row):
        plt.subplot(1,fig_per_row,j+1)
        print("count \t = \t",S[S_array[i+j]])
        draw_ETN(from_ETNS_to_ETN(S_array[i+j],k,meta_data),multiple=True)
    plt.show()