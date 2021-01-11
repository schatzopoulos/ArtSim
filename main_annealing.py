import sys
import numpy as np
from ArtSim import ArtSim
from rank_distance import tau
from scipy import optimize

dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent.txt"

if len(sys.argv) != 8:
    print("Usage: python main.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <cold_start_year> <aggr: median|mean> <output_file>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file_PA = sys.argv[3]
sim_file_PT = sys.argv[4]
cold_start_year = int(sys.argv[5])
aggr = sys.argv[6]
output_file = sys.argv[7]

artsim = ArtSim()

artsim.read_paper_ids(paper_details)
artsim.read_paper_scores(scores_file)

artsim.mark_cold_start_papers(cold_start_year)

artsim.read_similarities(sim_file_PA, 'PA', aggr)
artsim.read_similarities(sim_file_PT, 'PT', aggr)


def call_artsim(x):

	if np.sum(x) > 1:
		return 1000

	alpha = x[0]
	beta = x[1]
	gamma = 1 - alpha - beta
	call_artsim.count += 1

	artsim.run(alpha, beta, gamma, output_file)
    kendall_tau = tau(dblp_fcc, output_file)

    print (str(artisim_count) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(kendall_tau))

    return 1 - kendall_tau

bounds = [(0, 0.6), (0, 0.6)]

call_artsim.count = 0
result = optimize.dual_annealing(call_artsim, bounds, maxiter=500)
print(result)

print("Function calls: ", result['nfev'])
print("Best x: ", result['x'])
print("Best y: ", 1 - result['fun'])
print(call_artsim.count)