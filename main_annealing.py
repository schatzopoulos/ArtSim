import sys
import numpy as np
from ArtSim import ArtSim
from rank_distance import tau
from scipy import optimize
import time
import pandas as pd

dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent.txt"

if len(sys.argv) != 8:
    print("Usage: python main.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <con_file1> <cold_start_year> <output_file>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file_PA = sys.argv[3]
sim_file_PT = sys.argv[4]
con_file_PV = sys.argv[5]
cold_start_year = int(sys.argv[6])
output_file = sys.argv[7]

artsim = ArtSim()

artsim.read_paper_ids(paper_details)
artsim.read_paper_scores(scores_file)

artsim.mark_cold_start_papers(cold_start_year)

artsim.read_similarities(sim_file_PA, 'PA')
artsim.read_similarities(sim_file_PT, 'PT')
artsim.read_connections(con_file_PV, 'PV')
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
	results = artsim.run(alpha, beta, gamma, delta, output_file)
	call_artsim.artsim_time += (time.time() - start)

	start = time.time()
	result_df = pd.DataFrame(results, columns=['paper_id', 'pred_score'])
	kendall_tau = tau(ground_truth_df, result_df)
	call_artsim.tau_time += (time.time() - start)

	print (str(cold_start_year) + "\t" + str(call_artsim.count) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(delta) + "\t" + str(kendall_tau))

	return 1 - kendall_tau

bounds = [(0, 1.0), (0, 1.0), (0, 1.0)]

call_artsim.count = 0
call_artsim.artsim_time = 0
call_artsim.tau_time = 0
result = optimize.dual_annealing(call_artsim, bounds, maxiter=1000, no_local_search=True, initial_temp=5230)
print(">" + str(call_artsim.artsim_time) + "\t" + str(call_artsim.tau_time))
#print(result)

#print("Function calls: ", result['nfev'])
#print("Best x: ", result['x'])
#print("Best y: ", 1 - result['fun'])
#print(call_artsim.count)
