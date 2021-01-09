import sys
import pprint
import statistics
from rank_distance import tau
pp = pprint.PrettyPrinter(indent=4)

if len(sys.argv) != 10:
    print("Usage: python sim.py <paper_details_file> <scores_file> <sim_file1> <sim_file2> <cold_start_year> <aggr: median|mean> <output_file> <alpha> <beta>")
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
dblp_fcc = "../data/evaluation/dblp_fcc_varying_future_period_30percent.txt"


class ArtSimCore:

# read similarities
def read_similarties(sim_file, sim_name):
    sim_count = 0
    with open(sim_file) as fp:
        line = fp.readline()
        while line:
            line = line.rstrip()
            parts = line.split("\t")
            
            src_id = int(parts[0])
            dest_id = int(parts[1])

            # keep similarities for those papers inside the training set
            if src_id in papers and dest_id in papers:

                # 'similar' field is present only for papers in cold start
                if 'similar' in papers[src_id]:
                    papers[src_id]['similar'][sim_name].append((dest_id, float(parts[2]), papers[dest_id]['score']))
                    sim_count += 1

                if 'similar' in papers[dest_id]:
                    papers[dest_id]['similar'][sim_name].append((src_id, float(parts[2]), papers[src_id]['score']))
                    sim_count += 1
            
            line = fp.readline()

# load paper code & ids

paper_ids = {}
with open(paper_details, encoding="utf8") as fp:
    line = fp.readline()
    while line:
        line = line.rstrip()
        parts = line.split("\t")
        paper_ids[parts[1]] = int(parts[0])   
        line = fp.readline()

# read paper scores and publication year
papers = {}
papers_num = 0
papers_in_cold_start_num = 0
with open(scores_file) as fp:
    line = fp.readline()
    while line:
        line = line.rstrip()
        parts = line.split("\t")
        pub_year = int(parts[2])

        paper_id = paper_ids[parts[0]]
        papers[paper_id] = {
            'code': parts[0],
            'score': float(parts[1]), 
            'year': pub_year
        }
        if pub_year >= cold_start_year:
            papers[paper_id]['similar'] = {}
            papers[paper_id]['similar']['PA'] = []
            papers[paper_id]['similar']['PT'] = []

            papers_in_cold_start_num += 1

        line = fp.readline()
        papers_num += 1


read_similarties(sim_file_PA, 'PA')
read_similarties(sim_file_PT, 'PT')

print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

fw = open(output_file, "w")

result = []
for key in papers:
    if 'similar' in papers[key]: 
        score = papers[key]['score']

        sim_score_PA = 0.0
        if len(papers[key]['similar']['PA']) > 0:

            # calculate score from PA similarities
            scores_PA = [item[2] for item in papers[key]['similar']['PA']]

            if aggr == 'median':
                sim_score_PA = statistics.median(scores_PA)
            else:
                sim_score_PA = statistics.mean(scores_PA)

        sim_score_PT = 0.0    
        if  len(papers[key]['similar']['PT']) > 0:

            # calculate score from PT similarities
            scores_PT = [item[2] for item in papers[key]['similar']['PT']]

            if aggr == 'median':
                sim_score_PT = statistics.median(scores_PT)
            else:
                sim_score_PT = statistics.mean(scores_PT)

        score = alpha * sim_score_PA + beta * sim_score_PT + gamma * score

        fw.write(papers[key]['code'] + "\t" + str(score) + "\t" + str(papers[key]['year']) + "\n")

    else:
        result.append((papers[key]['code'], papers[key]['score'], papers[key]['year']))
        fw.write(papers[key]['code'] + "\t" + str(papers[key]['score']) + "\t" + str(papers[key]['year']) + "\n")
fw.close()
kendall_tau = tau(dblp_fcc, output_file)
print(kendall_tau)
