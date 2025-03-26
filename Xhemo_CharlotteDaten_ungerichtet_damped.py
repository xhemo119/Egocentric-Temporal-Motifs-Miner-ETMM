# ich versuche hier bisschen "ETMM.ipynb" nachzubauen aber mit Charlottes Daten (hier nur mit ungerichtet/damped_01)

# Der "damped" Datensatz bilden die Entwicklung einer Zeitreihe x=sin(5t)*e^(-0.1t) ab.


import construction as cs
import os
import math
import numpy as np
from matplotlib import pyplot as plt
from ETN import *
from ETMM import *


#for baba_nummer in range (0, 1):

# Parameters
k = 4                                   # number of static snapshot used for the constructions of ETN
gap = 0.5                               # temporal gap
label = False                           # if true, the loaded dataset is labeled
file_name = "damped_01_graph_30" #+ str(baba_nummer)

#G = nx.read_edgelist("Datasets/"+file_name)





def load_data(path):                                                        # Ein spezielles load_data(), da die Daten von Charlotte so ausgelegt sind, dass {'weight': 1} als zwei array elemente gelten (wegen dem Leerzeichen)
                                                                            # und nicht mehr nur 3 array elemente berücksichtig werden müssen (wie es im originalen ist) sondern 4
    data = []
    with open(path) as f:
        for line in f:
            tmp = line.split()[0:4]
            tmp[2] = tmp[2]+tmp[3]                                          # Das hier wird gemacht, um "{'weight':" und "1}" als 1 Element zu haben
            tmp[2] = int(1)                                                 # Und das wird gemacht, um aus "{'weight':1}" den integer 1 zu machen (kp ob ich das so machen soll mit der 1, aber falls nicht, dann kann ich hier easy diese Zeile einfach rausnehmen 
            arr_tmp = [int(tmp[0]),int(tmp[1]),int(tmp[2])]                 # und "{'weight':1}" wird korrekt an der Stelle im array gespeichert)
        
            data.append(arr_tmp)
    data = np.array(data)
    return(data)



# Load the temporal graph as a sequence of static NetworkX graphs
data = load_data("Datasets/ungerichtet/damped_01/"+file_name)                   # hier nicht vergessen immer die Endungen (zB .txt) zu ändern, wenn oben file_name geändert wird

#print(data)

def reorder_array(data):
    
    reordered_data = np.zeros_like(data)                            # Erstellt ein Array der gleichen Form wie data
    
    reordered_data[:, 0] = data[:, -1]                              # Verschiebt die letzte Spalte auf die erste
    reordered_data[:, 1] = data[:, 0]                               # Verschiebt die erste Spalte auf die zweite
    reordered_data[:, 2] = data[:, 1]                               # Verschiebt die zweite Spalte auf die dritte
    
    return reordered_data


# Umordnen des Arrays
reordered_data = reorder_array(data)
#print(reordered_data)


def time_changed_data(reordered_data):                                              # da Charlottes Daten an der Stelle, wo eig die Zeit stehen muss, {'weight': 1} stehen haben und sie in der E-Mail meinte die Daten sind 
    new_data = np.zeros_like(reordered_data)                                        # in der richtigen Reihenfolge platziert alle 0.5 Sekunden, habe ich dann diese Funktion programmiert 
    new_data = new_data.astype(object)                                              # (Change to object type to allow mixed types)
    new_data[:, 0] = np.arange(0, len(reordered_data[:,0]) * 0.5, 0.5)              # die an der Stelle von 0 hochzählt und in jeder inkrementation (0.5, 1, 1.5, ...) reinschreibt
    new_data[:, 1] = reordered_data[:, 1]
    new_data[:, 2] = reordered_data[:, 2]
    return new_data


new_data = time_changed_data(reordered_data)

#print(new_data)
#print(data)
#nodes = cs.individuals(data)
#print(nodes)
if label:
    meta_data = cs.load_metadata("Datasets/metadata/metadata_"+file_name+".dat")
else:
    meta_data = None
    
if label:
    graphs = cs.build_graphs(new_data,gap=gap,with_labels=label,meta_path="Datasets/metadata/metadata_"+file_name+".dat")
else:
    graphs = cs.build_graphs(new_data,gap=gap,with_labels=label)                                # in "graphs" werden die static graphs gespeichert (das sind einfach temporal graphic snapshots at time t) (aus vielen temporal graphic snapshots kann man dann ETN bauen)
    
#print(graphs)


# Count ETN or LETN and store the result
S = count_ETN(graphs,k,meta=meta_data)
S = {k: v for k, v in sorted(S.items(), key=lambda item: item[1], reverse=1)}               # das hier sortiert einfach die liste, sodass das etns was am meisten vorkommt ganz oben ist und das am wenigsten ganz unten

store_etns(S,file_name,gap,k,label=label)

#print(S)                                                                                    # diesen abschnitt mit dem Signature S muss ich mir nochmal genauer anschauen

# load etns 
SS = load_etns(file_name,gap,k,label=label)
assert(SS == S)


#S_array = list(S.keys())
#print(list(S.values()))
#print(from_ETNS_to_ETN(S_array[10],k=3,meta=None))                                         # hier verstehe ich noch nicht so ganz, warum der Graph so gezeichnet wird und why S_array[10] benutzt wird, allgemein nochmal anschauen
#draw_ETN(from_ETNS_to_ETN(S_array[0],k=2,meta=None),S_array[0][2:], ax ,multiple=False)                        

#print(list(S.keys()))
#print(list(S.values()))
#draw_barChart(list(S.keys()), list(S.values()))


# plot 6 most frequent ETN
fig_per_row = 5
S_array = list(S.keys())
for i in range(0,5,fig_per_row):
    plt.figure(figsize=(12,3))
    for j in range(fig_per_row):
        plt.subplot(1,fig_per_row,j+1)
        ax = plt.subplot(1,fig_per_row,j+1)
        print("count \t = \t",S[S_array[i+j]])
        draw_ETN(from_ETNS_to_ETN(S_array[i+j],k,meta_data), S_array[i+j][2:], ax, multiple=True)

    plt.show()

#draw_barChart(S_array[:][:5], list(S.values())[:5], k)



# BUILD NULL MODELS                                                                         # verstehe die theorie hinter den null models noch nicht so richtig
def build_nm(graphs,n,file):
    t = 0
    to_save = []

    f = open("null_models/"+file+"/"+file+"_"+str(n)+".txt", "w")                           # vorher war "a" statt "w", aber das war nerbig weil die files dann immer länger wurden weil einfach alles hinten rangepackt wurde, auch wenn man gap verändert hat


    for g in graphs:
        for e in g.edges():
            s = str(t)+" "+str(e[0])+" "+str(e[1])+"\n"
            f.write(s)
        t = t + gap + 1                                                                     # kp why + 1, hab das mal mit 0.001 versucht aber dann kamen komplett crazy zahlen
    f.close()

seed = 10
n = 5
null_models = shuffle_graphs(graphs,n,seed)
#print(len(null_models))

# store null models
c = 0

# open directory for the null models
directory = "null_models/" + file_name
if not os.path.exists(directory):
    os.makedirs(directory)

for graphs in null_models:
    build_nm(graphs,c,file_name)
    c = c + 1



# Egocentric temporal motifs miner ETMM

# load precoputed etns
S = load_etns(file_name,gap,k,label)


# count etn in null models and store the results

counts = counts_ETN_null_models(null_models,S,k,label,meta_data,verbose=True)
store_etm_counts(counts,file_name,gap,k,label)


tmp = load_etm_count(file_name,gap,k,label)
assert(tmp == counts)


#print(counts)


'''
# APPLY STATISTICAL TEST                                                                    # den bre muss ich mir auch nochmal genauer anschauen

alpha=0.01
beta=0.1
gamma=5

ETM = get_ETM(counts,alpha,beta,gamma)


# APPLY TEST BY ME
'''
N_G = np.array(list(counts.values()))[:,0]                                                  # N_G is the number of occurrences of sub-graph M in G
N_G0 = np.array(list(counts.values()))[:,1:]                                                # N_G0 is the average number of occurrences of sub-graph M in the random graphs (G0)

z = 0                                                                                       # iterator to go through the N_G0 list
for i in N_G:
    print("The number of occurences of a sub-graph M in G is: " + str(i))
    print("The number of occurences of a sub-graph M in the random graphs is: " + str(N_G0[z]))
    avr_num = np.mean(N_G0[z])
    print("The average number of occurences of a sub-graph M in the random graphs is: " + str(avr_num))
    diff = abs(i - avr_num)
    print("The difference between them equals: " + str("{:.1f}".format(diff)))              # dieses "{:.1f}".format(diff) sorgt dafür, dass es nur 2 Nachkommastellen gibt
    print("The deviation equals: " + str((diff/i)*100))                                           
    print( )
    z = z + 1

#print(N_G)
#print(N_G0)

'''
fig_per_row = 5
for i in range(0,fig_per_row,fig_per_row):
    plt.figure(figsize=(12,3))
    for j in range(fig_per_row):
        plt.subplot(1,fig_per_row,j+1)
        print("count \t = \t",ETM[i+j][1])
        draw_ETN(from_ETNS_to_ETN(ETM[i+j][0],k,meta_data),multiple=True)
    plt.show()
'''