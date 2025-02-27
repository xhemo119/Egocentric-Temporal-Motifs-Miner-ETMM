from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
import json
import os

def store_etns(S,file_name,gap,k,label):

    if label:
        name="gap_"+str(gap)+"_k_"+str(k)+"_LABEL.json"
    else:
        name="gap_"+str(gap)+"_k_"+str(k)+".json"

    directory = "res/"+file_name+"/ETNS/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    

    a_file = open(directory+name, "w")
    json.dump(S, a_file,indent=1)
    a_file.close()

    print("file stored in: \t"+directory+name)


def load_etns(file_name,gap,k,label):
    directory = "res/"+file_name+"/ETNS/"
    if label:
        name="gap_"+str(gap)+"_k_"+str(k)+"_LABEL.json"
    else:
        name="gap_"+str(gap)+"_k_"+str(k)+".json"

    with open(directory+name) as json_file:
        S = json.load(json_file)       

    return S

def count_ETN(graphs,k,meta=None):
    S = dict()                                      # Es wird hier benutzt, um das dictionary zu kreieren! Das erschafft dieses Format: {blablabla: 21, blabla: 14, bla: 1} (Also so wird dann tatsächlich unser Signatur beschriftet, wenn wir in die aufrufende Funktion gehen)
    for i in range(len(graphs)-k + 1):
        for v in graphs[i].nodes():
            etn = build_ETN(graphs[i:i+k+1],v)      # hier wird ETN erstmal gebaut mit graphs, worin die static graphs drin sind (das sind einfach temporal graphic snapshots at time t) (aus vielen temporal graphic snapshots kann man ETN bauen)
            #print(etn)
            if not etn == None:
                etns = get_ETNS(etn,meta)
                #print(etns)
                if etns in S.keys():
                    S[etns] = S[etns] + 1           # hier wird hochgezählt, wie oft ein ETNS vorkommt
                else:
                    S[etns] = 1
                #print(S[etns])
    return(S)





def get_node_encoding_labeled(meta,node_encoding,ego):
    categories = np.sort(list(np.unique(list(meta.values())))+["0"])

    meta_binary = list(itertools.product([0, 1], repeat=round(len(categories)**(1/2)+0.5)))
    meta_dict = dict()
    for i in range(len(categories)):    
        meta_dict[categories[i]] = list(meta_binary[i])


    new_node_encoding = dict()
    for i in node_encoding:
        tmp = []
        for v in node_encoding[i]:
            if(v==0):
                tmp.extend(meta_dict["0"])
            else:
                tmp.extend(meta_dict[meta[int(i)]])

        new_node_encoding[i]=tmp

    ego_encoding = meta_dict[meta[ego]]

    return(new_node_encoding,ego_encoding)
        
    


def from_ETNS_to_ETN(s,k,meta=None):

    n = k + 1
    if not(meta==None):
        categories = np.sort(list(np.unique(list(meta.values())))+["0"])
        meta_binary = list(itertools.product([0, 1], repeat=round(len(categories)**(1/2)+0.5)))
        meta_dict = dict()
        for i in range(len(categories)):
            value = "".join(str(e) for e in meta_binary[i])
            meta_dict[value] = categories[i]

        s = s[2:] # update s
        ego_encoding = s[:len(meta_binary[0])]
        s = s[len(meta_binary[0]):] # update s 

        node_encoding = [s[i:i+len(meta_binary[0])] for i in range(0,len(s),len(meta_binary[0]))]


        new_node_encoding = []
        for i in node_encoding:
            tmp = []
            for j in range(0, len(i), len(meta_binary[0])):
                value = i[j:j+len(meta_binary[0])]
                tmp.append(meta_dict[value])

            new_node_encoding.append(tmp)
        node_encoding_labels = new_node_encoding
    else:
        node_encoding = [s[2:][i:i+1] for i in range(0, len(s[2:]))]

    egos = [("0*_"+str(i),"0*_"+str(i+1)) for i in range(n-1)]



    ETN = nx.Graph()
    ETN.add_edges_from(egos)
    # add ego labels 
    if not(meta == None):
        for nod in list(ETN.nodes()):
            ETN.nodes()[nod]["label"] = meta_dict[ego_encoding]


    new_node_encoding = []

    for j in node_encoding:
        if("1" in j):
            new_node_encoding.append(1)
        else:
            new_node_encoding.append(0)

    node_encoding = new_node_encoding

    for i in range(0,len(node_encoding),n):
        same_person = []
        for j in range(n):
            if not(node_encoding[i+j] == 0):
                ETN.add_edge("0*_"+(str(j)),str(i+1)+"_"+str(j))
                same_person.append(str(i+1)+"_"+str(j))
                if not (meta == None):
                    ETN.nodes()[str(i+1)+"_"+str(j)]["label"] = node_encoding_labels[i+j][0]

        if len(same_person) > 1:
            for k in range(len(same_person)-1):
                ETN.add_edge(same_person[k],same_person[k+1])



    return(ETN)

       
    
def get_ETNS(ETN,meta=None):
    nodes = list(ETN.nodes())

    nodes_no_ego = []
    ids_no_ego = []
    lenght_ETNS = 0
    for n in nodes:
        if not ("*" in n):
            nodes_no_ego.append(n)
            if not(n.split("_")[0] in ids_no_ego):
                ids_no_ego.append(n.split("_")[0])
        else:
            ego = int(n.split("*")[0])
            lenght_ETNS = lenght_ETNS + 1

    node_encoding = get_node_encoding(ids_no_ego,nodes_no_ego,lenght_ETNS)
    if not(meta == None):
        node_encoding,ego_encoding = get_node_encoding_labeled(meta,node_encoding,ego)
    
    for k in node_encoding.keys():
        node_encoding[k] = '0b'+''.join(str(e) for e in node_encoding[k])

    binary_node_encodings = list(node_encoding.values())
    binary_node_encodings.sort()
    
    ETNS = '0b'+''.join(e[2:] for e in binary_node_encodings)
    
    # add ego label encoding
    if not (meta == None):
        ETNS  = '0b'+''.join(str(e) for e in ego_encoding)+ETNS[2:]
    
    return(ETNS)



def get_node_encoding(ids_no_ego,nodes_no_ego,lenght_ETNS):

    node_encoding = dict()
    for n in ids_no_ego:
        enc = []
        for k in range(lenght_ETNS):
            if (str(n)+"_"+str(k) in nodes_no_ego):
                enc.append(1)
            else:
                enc.append(0)
        node_encoding[n]=enc
        
    return(node_encoding)




def get_egocentric_neighborhood(g,v):
    return([str(v)+"*"]+list(g.neighbors(v)))

def build_ETN(graphs,v):
    if len(list(graphs[0].neighbors(v))) > 0 :
        en_list = []
        en_ids = []
        for i in graphs:
            en_list.append(get_egocentric_neighborhood(i,v))
            en_ids.append(get_egocentric_neighborhood(i,v))

        # add temporal step to en_list
        for i in range(len(en_list)):
            for j in range(len(en_list[i])):
                en_list[i][j] = str(en_list[i][j])+"_"+str(i)


        #buld graphs en
        en_graph = []
        for en in en_list:
            g = nx.Graph()
            for i in range(len(en)-1):
                g.add_edge(en[0],en[i+1])
            en_graph.append(g)

        # compose an to get disconnected ETN 
        ETN = nx.Graph()
        for g in en_graph:
            ETN = nx.compose(ETN,g)


        # merge en
        en_list_long = []
        for en in en_list:
            en_list_long_tmp = []
            for n in en:
                en_list_long_tmp.append(n.split("_")[0])

            en_list_long.append(en_list_long_tmp)

        for k in range(len(en_list_long)-1):
            for n in en_list_long[k]:
                for en in range(len(en_list_long[k+1:])):
                    add = False
                    if (n in en_list_long[k+en+1]):
                        add = True 
                        t = k + 1 + en
                        break
                if (add == True):
                    u = str(n)+"_"+str(k)
                    v = str(n)+"_"+str(t)
                    ETN.add_edge(u,v)
        return(ETN)
    else:
        return(None)


def draw_barChart(S_keys, S_values, k):

    S_keys_length = np.arange(len(S_keys))
    plt.bar(S_keys_length, S_values, align = 'center', alpha = 0.5)
    filtered_S_keys = [filtered[2:] for filtered in S_keys]
    #adjusted_label = "\n".join(str([filtered_S_keys[i:i+k+1] for i in range(0, len(filtered_S_keys), k+1)]))                                   # ein Ansatz dafür, wenn ich das ohne rotation mache und mit alle k zeichen ein zeilenumbruch, aber irgendwie klappt das nicht so wie bei den normalen graphen
    plt.xticks(ticks = S_keys_length, labels = filtered_S_keys, rotation=45)                                                                    # hier war vorher "plt.xticks(S_keys_length, filtered_S_keys, rotation=45)", allerdings ging das mit rotation=45 nur, wenn k=2. bei zu großem k haben sich die label wieder überschnitten.
    #S_values_length = np.arange(len(S_keys))
    #plt.yticks(S_values, S_values_length)

    plt.show()


def draw_ETN(ETN,S,ax,multiple=False):
    ids,k = get_ids_and_k(ETN)
    pos = dict()
    id_ego = []
    z = 5                                                                                                               # die Knoten haben y-Werte, allerdings sind diese hier nicht wichtig. Die Grafen sahen aber immer sehr unübersichtlich aus, deshalb dieses z was dafür sorgt, dass die Graphen gleichmäßig aufsteigende Knoten haben
    for t in range(k+1):                                                                                                # neues Problem: wenn gleicher Knoten in zwei hintereinander folgenden k, dann wird das nicht erkannt
        minus_sign = False
        for i in ids:
            if "*" in i:
                id_ego.append(str(i)+"_"+str(t))
                pos[str(i)+"_"+str(t)] = [t,int(i[0])]
            else:
                if minus_sign == False:
                    pos[str(i)+"_"+str(t)] = [t,z]
                    minus_sign = True
                else:
                    pos[str(i)+"_"+str(t)] = [t,-z]
                    minus_sign = False
            
        z = z + 5
                
    node_label = dict() 
    nodes_data = dict(ETN.nodes(data=True))
    for i in list(ETN.nodes()):
        if not(nodes_data[i] == {}):
            node_label[i] = nodes_data[i]["label"]
            
    #print(pos)
    #print(ids)
            
    def y_value(k):                                                                                                  # since the limits on the y-axe are different for every k, this function regulates it
        
        if k == 2:
            return (20, 2.5)                                                                                         # Laptop: (20, 2.5), PC: (19, 1.8)
        elif k == 3:
            return (34, 3)                                                                                           # Laptop: (34, 3), PC: (34, 2.8)
        elif k == 4:
            return (52, 4)                                                                                           # Laptop: (52, 4), PC: (52, 3.8)
        else:   # k ==5
            return (76, 5)                                                                                           # Laptop: (76, 5), PC: (76, 4.8)
            
    if (node_label == {}):
        y_axe, num = y_value(k)                                                                                   # parameter der entscheidet, wo limit auf der y-achse des graphen ist
        plt.ylim(-y_axe, y_axe)                                                                                     # setzt die limits auf der y-achse bei den gezeichneten graphen, parameter y_axe erstellt zur einfachheit
        nx.draw(ETN, pos=pos, ax=ax ,node_size=100, alpha=0.9, with_labels=False)
        ax.arrow(0, -y_axe+1, k+0.05, 0, head_width=1, head_length=0.1, fc='k', ec='k')                             # der Pfeil ganz unten beim Graphen der den Zeitstrahl zeigen soll
        tick_positions = [i for i in range(0, k+1, 1)]                                                              # gehört
        for x, label in zip(tick_positions, tick_positions):                                                        # alles
            ax.plot(x, -y_axe+1, marker="|", color="k", markersize=8)  # Ticks                                      # zum 
            ax.text(x, -y_axe+num - 0.05, label, ha='center', va='top', fontsize=7)  # Labels                       # Zeitstrahl Pfeil

        limits=plt.axis('on')                                                                                       # turns on axis
        adjusted_label = "\n".join([S[i:i+k+1] for i in range(0, len(S), k+1)])                                     # die ETNS die zu lang sind, überschneiden sich. ich habe das erst mit rotation=45 gelöst (siehe eine Zeile weiter unten im Kommentar), allerdings ging das nur bei k = 2. für größere k haben sich die label wieder überschnitten
        ax.set_xlabel(adjusted_label)                                                                               # wenn k = 2, dann kann ich hier auch "ax.set_xlabel(S, rotation=45)" benutzen, dann überschneiden sich die label nicht, da sie etwas rotiert sind. bei größerem k überschneiden sie sich allerdings wieder                                                     
        nx.draw_networkx_nodes(ETN, pos, nodelist=id_ego, node_size=100, node_color='red', alpha=0.5)
    else:
        nx.draw(ETN,pos=pos,node_size=100,alpha=0.5)
        nx.draw_networkx_nodes(ETN, pos, nodelist=id_ego, node_size=300, node_color='red',alpha=0.5)
        nx.draw_networkx_labels(ETN, pos, labels=node_label, font_size=12)

    if not multiple:
        plt.show()

#tick_labels = ["t=0", "t=1", "t=2", "t=3", "t=4"]  # Labels der Ticks

#plt.show()




# get unique ids (no time consideration)
def get_ids_and_k(ETN):
    nodes = list(ETN.nodes())
    ids = []
    k = 0
    for n in nodes:
        id_n = (n.split("_")[0])
        k_tmp = (n.split("_")[1])
        if not (id_n in ids):
            ids.append(id_n)
        if int(k_tmp) > k:
            k = int(k_tmp)
    
    return(ids,k)


def draw_ETN_barchart(width, height):                                         #Komplett neue Funtion um die Ausgaben als Bar Charts darzustellen
    
    plt.bar(width,height)
    
    
    # Das ab hier ist von draw_ETN(...)
    '''
    ids,k = get_ids_and_k(ETN)
    pos = dict()
    id_ego = []
    for t in range(k+1):
        for i in ids:
            if "*" in i:
                id_ego.append(str(i)+"_"+str(t))
                pos[str(i)+"_"+str(t)] = [t,int(i[0])]
            else:
                pos[str(i)+"_"+str(t)] = [t,int(i)]
                
    node_label = dict() 
    nodes_data = dict(ETN.nodes(data=True))
    for i in list(ETN.nodes()):
        if not(nodes_data[i] == {}):
            node_label[i] = nodes_data[i]["label"]
            
            
    if (node_label == {}):
        nx.draw(ETN,pos=pos,node_size=100,alpha=0.9,with_labels=False)
        nx.draw_networkx_nodes(ETN, pos, nodelist=id_ego, node_size=300, node_color='red',alpha=0.5)
    else:
        nx.draw(ETN,pos=pos,node_size=100,alpha=0.5)
        nx.draw_networkx_nodes(ETN, pos, nodelist=id_ego, node_size=300, node_color='red',alpha=0.5)
        nx.draw_networkx_labels(ETN, pos, labels=node_label, font_size=12)

    if not multiple:
        plt.show()
    '''