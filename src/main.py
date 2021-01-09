import ArtSim
from rank_distance import tau

if len(sys.argv) != 10:
    print("Usage: python main.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <cold_start_year> <aggr: median|mean> <output_file> <alpha> <beta>")
    sys.exit(-1)


paper_details = args[1]
scores_file = args[2]
sim_file_PA = args[3]
sim_file_PT = args[4]
cold_start_year = int(args[5])
aggr = args[6]
output_file = args[7]
alpha = float(args[8])
beta = float(args[9])
gamma = 1 - alpha - beta

artsim = ArtSim()

artsim.read_paper_ids(paper_details)
total_papers, papers_in_cold_start = artsim.read_paper_scores(scores_file, cold_start_year)

artsim.read_similarties(self.sim_file_PA, 'PA')
artsim.read_similarties(self.sim_file_PT, 'PT')

artsim.run(alpha, beta, gamma, output_file)

kendall_tau = tau(dblp_fcc, output_file)
print(kendall_tau)
