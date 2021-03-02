import sys
import numpy as np
from ArtSimCore import ArtSimCore
from rank_distance import tau, ndcg
from scipy import optimize
import time
import pandas as pd

if len(sys.argv) != 8 and len(sys.argv) != 9:
    print("Usage: python3 artsim_plus.py <paper_details_file> <scores_file> <sim_file_PAP> <sim_file_PTP> <connections_file_PV>  <cold_start_year> <eval_method> <ndcg:k>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file_PA = sys.argv[3]
sim_file_PT = sys.argv[4]
con_file_PV = sys.argv[5]
cold_start_year = int(sys.argv[6])
eval_method = sys.argv[7]

k = -1
if eval_method == "ndcg":
    if len(sys.argv) != 9:
        print("Usage: python3 artsim_plus.py <paper_details_file> <scores_file> <sim_file_PAP> <sim_file_PTP> <connections_file_PV>  <cold_start_year> <eval_method> <ndcg:k>")
        sys.exit(-1)
    k = int(sys.argv[8])

artsim_core = ArtSimCore()

artsim_core.read_paper_ids(paper_details)
artsim_core.read_paper_scores(scores_file)

artsim_core.mark_cold_start_papers(cold_start_year)

artsim_core.read_similarities(sim_file_PA, 'PA')
artsim_core.read_similarities(sim_file_PT, 'PT')
artsim_core.read_connections(con_file_PV, 'PV')
ground_truth_df = pd.read_csv(dblp_fcc, sep='\t', header=None, names=['paper_id',  'truth_score'])

def call_artsim(x):
	if np.sum(x) > 1:
		return 1000

	alpha = x[0]
	beta = x[1]
	gamma = x[2]
	delta = 1 - alpha - beta - gamma
	call_artsim.count += 1

	start = time.time()
	results = artsim.run(alpha, beta, gamma, delta)
	call_artsim.artsim_time += (time.time() - start)

	start = time.time()
	result_df = pd.DataFrame(results, columns=['paper_id', 'pred_score'])

	eval_score = -1
	if eval_method == "tau":
		eval_score = tau(ground_truth_df, result_df)
	elif eval_method == "ndcg":
		eval_score = ndcg(ground_truth_df, result_df, k)
	else:
		print(eval_method + " is not recognised as a valid evaluation method; please choose one of { tau, ndcg }")
		sys.exit(-1)

	call_artsim.eval_time += (time.time() - start)

	print (str(cold_start_year) + "\t" + str(k) + "\t" + str(call_artsim.count) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(delta) + "\t" + str(eval_score))

	return 1 - eval_score

bounds = [(0, 1.0), (0, 1.0), (0, 1.0)]

call_artsim.count = 0
call_artsim.artsim_time = 0
call_artsim.eval_time = 0
result = optimize.dual_annealing(call_artsim, bounds, maxiter=1000, no_local_search=True, initial_temp=5230)
print(">" + str(call_artsim.artsim_time) + "\t" + str(call_artsim.eval_time))
#print(result)

#print("Function calls: ", result['nfev'])
#print("Best x: ", result['x'])
#print("Best y: ", 1 - result['fun'])
#print(call_artsim.count)
