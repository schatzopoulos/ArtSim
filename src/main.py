import sys
from ArtSim import ArtSim
from rank_distance import tau

if len(sys.argv) != 10:
    print("Usage: python main.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <cold_start_year> <aggr: median|mean> <output_file> <alpha> <beta>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file_PA = sys.argv[3]
sim_file_PT = sys.argv[4]
cold_start_year = int(sys.argv[5])
aggr = sys.argv[6]
output_file = sys.argv[7]
alpha = float(sys.argv[8])
beta = float(sys.argv[9])
gamma = 1 - alpha - beta

artsim = ArtSim()

artsim.read_paper_ids(paper_details)
total_papers, papers_in_cold_start = artsim.read_paper_scores(scores_file, cold_start_year)

print(total_papers)
print(papers_in_cold_start)

artsim.read_similarties(self.sim_file_PA, 'PA')
artsim.read_similarties(self.sim_file_PT, 'PT')

artsim.run(alpha, beta, gamma, output_file)

kendall_tau = tau(dblp_fcc, output_file)
print(kendall_tau)
