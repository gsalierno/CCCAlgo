#!/usr/bin/env python3

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from CWMA import CWMA
from DMA import computeScoreNORM
# left nodes
num_left = 4
# right nodes
num_right = 5
#contstraint on right nodes
b_right = 1
#DATA
BG = None
adj_M = None

def build_network():
	global BG
	#create bipartite network
	BG = nx.complete_bipartite_graph(num_left, num_right)
	# add nodes
	left,right = nx.bipartite.sets(BG)
	# add edges
	BG.add_weighted_edges_from((u,v,random.randint(1, 10)) for u,v in BG.edges())
	plot_network(BG.edges)

def plot_network(edges,isMin=False):
	#layout
	global BG
	pos = nx.circular_layout(BG)  
	edge_labels = nx.get_edge_attributes(BG,'weight')
	nx.draw_networkx_nodes(BG, pos,node_size=600,node_color='blue')
	nx.draw_networkx_labels(BG, pos, font_size=15, font_family='sans-serif')
	nx.draw_networkx_edges(BG,pos, edgelist=edges, width=2, alpha=0.5, edge_color='grey')
	nx.draw_networkx_edge_labels(BG, pos, edge_labels=edge_labels, font_size=15, font_family='sans-serif')
	
	plt.axis('off')
	plt.show() 
	

#prepare data for matching
def prepare_data():
	global adj_M
	# adjacent matrix of each node of the bipartite graph
	adj_M = nx.to_numpy_matrix(BG)
	#optimize matrix by taking adj list of only the right side
	adj_M = adj_M[num_left:]
	#replace 0 of adj matrix with inf
	adj_M[adj_M == 0] = math.inf
	print(adj_M)

	return adj_M


def adjust_network(selected_edges):
	global BG
	#normalize edges
	selected_edges = [(t[1],t[0]+num_left) for t in selected_edges]
	print("Selected Edges: "+str(selected_edges))
	#print(BG.edges())	
	plot_network(selected_edges,isMin=True) # selected edges based on matching of the algorithm

	return selected_edges



def computeScore(selected_edges):
	cost = 0
	adj_M = nx.to_numpy_matrix(BG)

	for e in selected_edges:
		cost += adj_M[e]

	print("Score overall QoS with CC:"+str(cost))


if __name__ == '__main__':
	build_network()
	adj_M = prepare_data()
	computeScoreNORM(adj_M)
	sel_edges_raw = CWMA(num_left,num_right,adj_M,b_right).match()
	sel_edges_norm = adjust_network(sel_edges_raw)
	computeScore(sel_edges_norm)
	

