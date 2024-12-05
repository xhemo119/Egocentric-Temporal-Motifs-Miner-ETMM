# ich versuche hier bisschen "ETMM.ipynb" nachzubauen

import construction as cs
from ETN import *
from ETMM import *

# %load_ext autoreload
# %autoreload 2


# Parameters
k = 2                                                               # number of static snapshot used for the constructions of ETN
gap = 300                                                           # temporal gap
label = False                                                       # if true, the loaded dataset is labeled
file_name = "Xhemo_Test_Dataset (email-Eu-core-temporal)"           # Wenn ich hier file_name änder, nicht vergessen unten bei data = cs.load_data(...) die Endung der Datei auch zu ändern falls nötig

'''
def individuals(data):
    """compute the number of individuals

    Parameters:
    data (np.array): loaded input data

    Returns:
    int: number of individuals in the network

    """
    return(np.unique(data[:,:1]))



def build_graphs(data,gap=19,with_labels=False,meta_path=None):

    graphs = []
    G=nx.Graph()
    nodes = individuals(data)
    G.add_nodes_from(nodes)
    if(with_labels):
        G = add_labels(G,meta_path)
    splitted_data = split_input_data(data,gap)
    
    for t in splitted_data:
        g = G.copy()
        for _,i,j in t:
            g.add_edge(i,j)
        graphs.append(g)  

    return(graphs)

def split_input_data(data, gap=19):
    """split the input data according to the temporal gap

    Parameters:
    data (np.array): loaded input data
    gap (int): [default = 19]

    Returns:
    np.array(): return an array of array, the inner array represent the interactions within the gap.

    """
    times = data[:,2]
    pos = times[0]
    chunks = []
    for i in range(len(times)):
        if not(times[i]<=(pos + gap)):
            chunks.append(i)
            pos = times[i]

    return(np.split(data,chunks))


def add_labels(G,meta_path):
    """Summary or Description of the Function

    Parameters:
    argument1 (int): Description of arg1

    Returns:
    int:Returning value

    """
    meta = load_metadata(meta_path) #dictionary
    
    for n in G.nodes():
        G.nodes()[n]["label"] = meta[n]
    
    return(G)

def load_metadata(path_meta):
    """load the metadata of the tmporal graph

    Parameters:
    path_meta (string): path of the meta data

    Returns:
    dict: a dictionary whit key = node and value = attributes

    """
    data = dict()
    with open(path_meta) as f:
        for line in f:
            tmp = line.split()[0:2]

            data[int(tmp[0])] = tmp[1]        

    return(data)
'''

def reorder_array(data):

    reordered_data = np.zeros_like(data)                            # Erstellt ein Array der gleichen Form wie data
    reordered_data[:, 0] = data[:, -1]                              # Verschiebt die letzte Spalte auf die erste
    reordered_data[:, 1] = data[:, 0]                               # Verschiebt die erste Spalte auf die zweite
    reordered_data[:, 2] = data[:, 1]                               # Verschiebt die zweite Spalte auf die dritte
    return reordered_data

# Load the temporal graph as a sequence of static NetworkX graphs
data = cs.load_data("Datasets/"+file_name+".txt")                   # hier nicht vergessen immer die Endungen (zB .txt) zu ändern, wenn oben file_name geändert wird

# Umordnen des Arrays
reordered_data = reorder_array(data)
#print(reordered_data)

# print(data)
# nodes = individuals(data)
# print(nodes)
if label:
    meta_data = cs.load_metadata("Datasets/metadata/metadata_"+file_name+".dat")
else:
    meta_data = None
    
if label:
    graphs = cs.build_graphs(reordered_data,gap=gap,with_labels=label,meta_path="Datasets/metadata/metadata_"+file_name+".dat")
else:
    graphs = cs.build_graphs(reordered_data,gap=gap,with_labels=label)

print(graphs)

# Count ETN or LETN and store the result
S = count_ETN(graphs,k,meta=meta_data)
S = {k: v for k, v in sorted(S.items(), key=lambda item: item[1], reverse=1)}

store_etns(S,file_name,gap,k,label=label)

print(S)                                                                                    # diesen abschnitt mit dem Signature S muss ich mir nochmal genauer anschauen


# load etns 
SS = load_etns(file_name,gap,k,label=label)
assert(SS == S)


S_array = list(S.keys())
#print(S_array[10])
#print(from_ETNS_to_ETN(S_array[10],k=3,meta=None))
draw_ETN(from_ETNS_to_ETN(S_array[10],k=2,meta=None),multiple=False)                        # hier verstehe ich noch nicht so ganz, warum der Graph so gezeichnet wird und why S_array[10] benutzt wird, allgemein nochmal anschauen


# plot 6 most frequent ETN
fig_per_row = 5
S_array = list(S.keys())
for i in range(0,5,fig_per_row):
    plt.figure(figsize=(12,3))
    for j in range(fig_per_row):
        plt.subplot(1,fig_per_row,j+1)
        print("count \t = \t",S[S_array[i+j]])
        draw_ETN(from_ETNS_to_ETN(S_array[i+j],k,meta_data),multiple=True)
    plt.show()


# BUILD NULL MODELS                                                                         # verstehe die theorie hinter den null models noch nicht so richtig
def buil_nm(graphs,n,file):
    t = 0
    to_save = []
    f = open("null_models/"+file+"/"+file+"_"+str(n)+".txt", "a")
    for g in graphs:
        for e in g.edges():
            s = str(t)+" "+str(e[0])+" "+str(e[1])+"\n"
            f.write(s)
        t = t + gap + 1
    f.close()

seed = 10
n = 5
null_models = shuffle_graphs(graphs,n,seed)
print(len(null_models))

# store null models
c = 0
for graphs in null_models:
    buil_nm(graphs,c,file_name)
    c = c + 1



# Egocentric temporal motifs miner ETMM

# load precoputed etns
S = load_etns(file_name,gap,k,label)


# count etn in null models and store the results

counts = counts_ETN_null_models(null_models,S,k,label,meta_data,verbose=True)
store_etm_counts(counts,file_name,gap,k,label)


tmp = load_etm_count(file_name,gap,k,label)
assert(tmp == counts)


print(counts)



# APPLY STATISTICAL TEST                                                                    # den bre muss ich mir auch nochmal genauer anschauen

alpha=0.01
beta=0.1
gamma=5

ETM = get_ETM(counts,alpha,beta,gamma)


fig_per_row = 5
for i in range(0,fig_per_row,fig_per_row):
    plt.figure(figsize=(12,3))
    for j in range(fig_per_row):
        plt.subplot(1,fig_per_row,j+1)
        print("count \t = \t",ETM[i+j][1])
        draw_ETN(from_ETNS_to_ETN(ETM[i+j][0],k,meta_data),multiple=True)
    plt.show()
