#!/bin/bash
# sed -e 's/([^()]*)//g' author_ids.csv
input_folder="../sigmod_per_year/all/APV-topk"
authors_file="$input_folder/author_ids.csv"
hin_inputs=("PA" "PT")
ids_input="../data/ids.csv"

for hin_input in "${hin_inputs[@]}"
do
	config="$author_id"_config.csv
	in="$hin_input".csv
	out="$hin_input"_sim.csv
	# echo $author_id
	echo "{
	    \"indir\": \"/dataX/SciNeM-data/DBLP/nodes/\",
	    \"irdir\": \"/dataX/SciNeM-data/DBLP/relations/\",
	    \"algorithm\": \"DynP\",
	    \"hin_out\": \"../data/$in\",
	    \"analysis_out\": \"../data/$out\",
	    \"final_out\": \"./data/out/FINAL_OUT.csv\",
	    \"ids_input\": \"$ids_input\",
	    \"k\": 500,
	    \"t\": 1,
	    \"w\": 5,
	    \"min_values\": 1,
	    \"operation\": \"search\",
	    \"query\": {
	        \"metapath\": \"APV\",
	        \"constraints\": {
	        }
	    }
	    
	}" > $config
	echo $1

	java -jar ../EntitySimilarity-1.0-SNAPSHOT.jar -c $config > $hin_input"_join.csv"
	rm $config
done