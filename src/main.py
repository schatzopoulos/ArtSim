import sys
import numpy as np
from ArtSim import ArtSim
from rank_distance import tau

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


for alpha in np.linspace(0, 0.6, 7):
        for beta in np.linspace(0, 0.6, 7):
                for gamma in np.linspace(0, 1, 11):
                        alpha = round(alpha, 1)
                        beta = round(beta, 1)
                        gamma = round(gamma, 1)
                        sum = alpha + beta + gamma
                        if (round(sum, 1) != 1.0):
                                continue

                        artsim.run(alpha, beta, gamma, output_file)
                        kendall_tau = tau(dblp_fcc, output_file)

                        print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(kendall_tau))



for alpha in np.linspace(0, 0.6, 61):
	for beta in np.linspace(0, 0.6, 61):
		for gamma in np.linspace(0, 1, 101):
			alpha = round(alpha, 2)
			beta = round(beta, 2)
			gamma = round(gamma, 2)
			sum = alpha + beta + gamma
			if (round(sum, 2) != 1.0):
				continue

			artsim.run(alpha, beta, gamma, output_file)
			kendall_tau = tau(dblp_fcc, output_file)

			print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(kendall_tau))
