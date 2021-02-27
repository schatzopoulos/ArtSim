import sys
import numpy as np
from ArtSim import ArtSim
from rank_distance import tau, ndcg
import pandas as pd
import time

dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent_WITH_ZEROS.txt"
#dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent.txt"

if len(sys.argv) != 9:
    print("Usage: python main.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <cold_start_year> <aggr: median|mean> <output_file>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file_PA = sys.argv[3]
sim_file_PT = sys.argv[4]
con_file_PV = sys.argv[5]
cold_start_year = int(sys.argv[6])
output_file = sys.argv[7]
k = int(sys.argv[8])

artsim = ArtSim()

artsim.read_paper_ids(paper_details)
artsim.read_paper_scores(scores_file)

artsim.mark_cold_start_papers(cold_start_year)
artsim.read_similarities(sim_file_PA, 'PA')
artsim.read_similarities(sim_file_PT, 'PT')
artsim.read_connections(con_file_PV, 'PV')
ground_truth_df = pd.read_csv(dblp_fcc, sep='\t', header=None, names=['paper_id',  'truth_score'])

for precision in [1]:
    splits = pow(10, precision) + 1

    artsim_time = 0
    tau_time = 0

    for alpha in np.linspace(0, 1, splits):
        for beta in np.linspace(0, 1, splits):
                for delta in np.linspace(0, 1, splits):
                    alpha = round(alpha, precision)
                    beta = round(beta, precision)
                    gamma = 0
                    delta = round(delta, precision)
                    sum = alpha + beta + gamma + delta

                    if (round(sum, precision) != 1.0):
                        continue

                    start = time.time()
                    results = artsim.run(alpha, beta, gamma, delta, output_file)
                    artsim_time += (time.time() - start)

                    start = time.time()
                    result_df = pd.DataFrame(results, columns=['paper_id', 'pred_score'])
                    #kendall_tau = tau(ground_truth_df, result_df)
                    ndcg_score = ndcg(ground_truth_df, result_df, k)
                    tau_time += (time.time() - start)

                    print (str(precision) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(delta) + "\t" + str(ndcg_score))

    print(">" + str(artsim_time) + "\t" + str(tau_time))
