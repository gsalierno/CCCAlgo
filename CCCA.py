#!/usr/bin/env python3
import numpy as np
import math

class CCCA:

    def __init__(self, num_left, num_right,adj_M, b_right):
        self.num_left = num_left
        self.num_right = num_right
        self.adj_M = adj_M
        self.b_right = b_right
        self.boundArr = np.zeros(num_right)
        self.selected_edges = list()

    def match(self):
        while np.sum(self.boundArr) < self.num_left:
            
            for i in range(0,self.num_right):
                
                if(self.boundArr[i] == self.b_right): #if the right node has reached the degree constraint
                    continue   

                min_index_row = list(np.unravel_index(np.argmin(self.adj_M[i], axis=None), self.adj_M.shape)) # select min indices along for i raw w(0) ... w(n)
                min_index_row[0] = i #correction to the diverse matrix reference M[i] not adj_M
                min_index_col = list(np.unravel_index(np.argmin(self.adj_M[:,min_index_row[1]], axis=None), self.adj_M[:,min_index_row[1]].shape))  #retrieve minimum column indices
                min_index_col[1] = min_index_row[1]
                #print(min_index_row,min_index_col)
                #print(self.adj_M)
                #print(self.boundArr)

                if self.adj_M[min_index_row[0],min_index_row[1]] <= self.adj_M[min_index_col[0],min_index_col[1]] or self.boundArr[min_index_col[0]] == self.b_right:#right node which have min value has reached the degree constraint
                    self.selected_edges.append((min_index_row[0],min_index_row[1]))
                    self.boundArr[i] = self.boundArr[i] + 1 #augment the degree constraint
                    self.adj_M[:,min_index_row[1]] = math.inf
                else:
                    continue #it means that other node has to make a choice before you can

        return self.selected_edges
