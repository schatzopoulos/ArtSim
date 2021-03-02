import sys
import numpy as np
from ArtSimCore import ArtSimCore
from rank_distance import tau, ndcg
import pandas as pd
import time

dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent_WITH_ZEROS.txt"
#dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent.txt"

if len(sys.argv) != 8 and len(sys.argv) != 9:
    print("Usage: python3 artsim.py <paper_details_file> <scores_file> <sim_file_PAP> <sim_file_PTP> <connections_file_PV>  <cold_start_year> <eval_method> <ndcg:k>")
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
        print("Usage: python3 artsim.py <paper_details_file> <scores_file> <sim_file_PAP> <sim_file_PTP> <connections_file_PV>  <cold_start_year> <eval_method> <ndcg:k>")
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
                    results = None
                    results = artsim_core.run(alpha, beta, gamma, delta)
                    artsim_time += (time.time() - start)

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

                    eval_time += (time.time() - start)

                    print (str(precision) + "\t" + str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(delta) + "\t" + str(eval_score))

    print(">" + str(artsim_time) + "\t" + str(eval_time))
