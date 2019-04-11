#!/usr/bin/env python3

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import math
import csv

from CWMA import CWMA
# left nodes
num_left = 1000
# right nodes
num_right = 1000
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
	#plot_network(BG.edges)

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
	#print(adj_M)

	return adj_M


def adjust_network(selected_edges):
	global BG
	#normalize edges
	selected_edges = [(t[1],t[0]+num_left) for t in selected_edges]
	#print("Selected Edges: "+str(selected_edges))
	#print(BG.edges())	
	#plot_network(selected_edges,isMin=True) # selected edges based on matching of the algorithm

	return selected_edges



def computeScoreCCCA(selected_edges):
	score = 0
	adj_M = nx.to_numpy_matrix(BG)

	for e in selected_edges:
		score += adj_M[e]

	print("Score overall QoS with CC:"+str(score))
	return score 

#simply take the minimum of column for each task
def computeScoreNORM(adjM):
	score = sum(np.apply_along_axis(sumScore, axis=1, arr=adjM))
	print("Score NORM: ", score)
	return score


def sumScore(row):
	print(row)
	return np.min(row)



def writeCSV(score1,score2):
	with open('result.csv','a', newline='') as csvfile:
		out = csv.writer(csvfile,delimiter =',')
		out.writerow([score1,score2])


if __name__ == '__main__':

	for i in range(0,99):
		build_network()
		adj_M = prepare_data()
		score1 = computeScoreNORM(adj_M)
		sel_edges_raw = CWMA(num_left,num_right,adj_M,b_right).match()
		sel_edges_norm = adjust_network(sel_edges_raw)
		score2 = computeScoreCCCA(sel_edges_norm)
		writeCSV(score1,score2)

