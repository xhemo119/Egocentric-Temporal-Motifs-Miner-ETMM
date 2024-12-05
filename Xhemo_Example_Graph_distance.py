# ich versuche hier bisschen Graph distances.ipynb nachzubauen

import networkx as nx

import construction as cs
import distances as dis

# %load_ext autoreload
# %autoreload 2


dataset1 = "InVS13"
dataset2 = "LH10"
gap = 300                                       # temporal gap

structure_type = "ETM"                          # ETM or ETN
k = 3                                           # number of EN used for the creation of ETN


# statistical test parameters
alpha=0.01
beta=0.1
gamma=5
label=False                                     # labels on nodes or not

dist_etmm = dis.etmm_distance([dataset1,dataset2],structure_type,gap,k,label,alpha,beta,gamma)

print("Distance between \n\t%s and %s \t\t%0.3f" %(dataset1,dataset2,dist_etmm))