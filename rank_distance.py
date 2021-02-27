#!/opt/anaconda/bin/python

# Program to calculate spearman's rho,
# using the Bio.Cluster module of python

# -------------------------------------------------------------------- #
# Imports
import sys
import os
import Bio.Cluster
import scipy
import scipy.stats
import subprocess
import pandas as pd
import math

# -------------------------------------------------------------------- #

# -------------------------------------------------------------------- #
# Function definitions

# Function that returns the rank scores of papers in a paper id sorted file
def read_file_ranks(file_name, pub_id_dict = None):
	# List containing ranks. To be returned
	rank_list = list()
	# Read file contents - assumes a file SORTED by PAPER ID
	contents = open(file_name, "r").readlines()
	contents = [line.strip() for line in contents]

	#counter = 0
	
	# Read ranks into list - optionally exclude some
	if(not pub_id_dict):
		for content in contents:
			# print "File1, adding: ", content.split()[1]
			rank_list.append(float(content.split()[1]))
			#if(counter < 10):
			#	print content.split()[0], content.split()[1]
			#counter+=1
	# Exclude those papers not found previously
	else:
		for content in contents:
			line_parts = content.split()
			pid = line_parts[0]
			score = line_parts[1]
			if(pid in pub_id_dict):
				# print "File2, adding: ", score
				rank_list.append(float(score))
				#if(counter < 10):
				#	print content.split()[0], content.split()[1]
				#counter+=1
			else:
				pass
		
	return rank_list
	
# Function to read valid Paper IDs (those in older file)
def get_valid_paper_ids(file_name):
	valid_papers = dict()
	#print(file_name)
	contents = open(file_name, "r").readlines()
	# print(contents)
	contents = [line.strip().split()[0] for line in contents]
	# print(contents)
	for content in contents:
		valid_papers[content] = 1
	
	return valid_papers

# -------------------------------------------------------------------- #

# -------------------------------------------------------------------- #
# Reading of arguments
# TODO: implement rho

def tau(ground_truth_df,  result_df):
	metric = "k"

	df = pd.merge(ground_truth_df, result_df, how='inner', on=['paper_id'])

	old_file_list = df['truth_score'].tolist()
	new_file_list = df['pred_score'].tolist()

	ret_val = 0.0
	if(metric == "s"):
		# Fees rank lists into Bio.Cluster method
		spearman_dist = Bio.Cluster.distancematrix((old_file_list,new_file_list), dist=metric)[1][0]
		# Output rho
		ret_val = (str(1-spearman_dist))

	elif(metric == "k"):
		scipy_kendall = scipy.stats.stats.kendalltau(old_file_list, new_file_list)[0]
		ret_val = scipy_kendall
	return ret_val

def ndcg(ground_truth_df, result_df, k):
        df = pd.merge(ground_truth_df, result_df, how='inner', on=['paper_id']) 
        ground_truth_addends = df['truth_score'].tolist() 
        df = df.sort_values(by=['pred_score'], ascending=False) 
        comparison_addends = df['truth_score'].tolist() 

        IDCG = DCG(k, ground_truth_addends[:k])
        DCG_comp = DCG(k, comparison_addends[:k])
        return float(DCG_comp)/float(IDCG)

def DCG(topk, score_list):
        DCG = 0
        for i in range(0, topk):
                DCG += float(score_list[i])/math.log((i+2), 2)
        return DCG
