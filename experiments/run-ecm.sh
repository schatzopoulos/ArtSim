#!/bin/bash

years=( "2007" )

for year in "${years[@]}"
do
	python3 ../src/main.py ../data/P.csv ../data/rival_scores/timeawarerank_results_file_dblp_full_graph_oldest_50percent.txt_a0.2_c0.4_year2010_mECM.txt ../data/similarities/PAP_similarities.csv  ../data/similarities/PTP_similarities.csv $year mean tmp-results.csv
	break
done
