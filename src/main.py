import sys
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
print("Done read_paper_ids")
artsim.read_paper_scores(scores_file)
print("Done read_paper_scores")

artsim.mark_cold_start_papers(cold_start_year)
print("Done mark_cold_start_papers")

artsim.read_similarities(sim_file_PA, 'PA')
print("Done read_similarities PA")
artsim.read_similarities(sim_file_PT, 'PT')
print("Done read_similarities PT")

params = [(0,0.1), (0,0.2), (0,0.3), (0,0.4), (0,0.5), (0,0.6), (0,0.7), (0,0.8), (0,0.9), (0,1), (0.1,0), (0.1,0.1), (0.1,0.2), (0.1,0.3), (0.1,0.4), (0.1,0.5), (0.1,0.6), (0.1,0.7), (0.1,0.8), (0.1,0.9), (0.2,0), (0.2,0.1), (0.2,0.2), (0.2,0.3), (0.2,0.4), (0.2,0.5), (0.2,0.6), (0.2,0.7), (0.2,0.8), (0.3,0), (0.3,0.1), (0.3,0.2), (0.3,0.3), (0.3,0.4), (0.3,0.5), (0.3,0.6), (0.3,0.7), (0.4,0), (0.4,0.1), (0.4,0.2), (0.4,0.3), (0.4,0.4), (0.4,0.5), (0.4,0.6), (0.5,0), (0.5,0.1), (0.5,0.2), (0.5,0.3), (0.5,0.4), (0.5,0.5), (0.6,0), (0.6,0.1), (0.6,0.2), (0.6,0.3), (0.6,0.4), (0.7,0), (0.7,0.1), (0.7,0.2), (0.7,0.3), (0.8,0), (0.8,0.1), (0.8,0.2), (0.9,0), (0.9,0.1), (1,0)]
for alpha, beta in params:
	
	gamma = 1.0 - alpha - beta
	
	artsim.run(alpha, beta, gamma, aggr, output_file)
	kendall_tau = tau(dblp_fcc, output_file)

	print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma) + "\t" + str(kendall_tau))
	
