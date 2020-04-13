import sys
import pprint
import statistics

pp = pprint.PrettyPrinter(indent=4)

if len(sys.argv) != 7:
    print("Usage: python sim.py <paper_details_file> <scores_file> <sim_file> <cold_start_year> <aggr: median|mean> <alpha>")
    sys.exit(-1)


paper_details = sys.argv[1]
scores_file = sys.argv[2]
sim_file = sys.argv[3]
cold_start_year = int(sys.argv[4])
aggr = sys.argv[5]
alpha = float(sys.argv[6])

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
            papers[paper_id]['similar'] = []
            papers_in_cold_start_num += 1
        
        line = fp.readline()
        papers_num += 1

# print(papers)
# print("TOTAL PAPERS: " + str(papers_num))
# print("PAPERS IN COLD START: " + str(papers_in_cold_start_num))

# read similarities
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
                papers[src_id]['similar'].append((dest_id, float(parts[2]), papers[dest_id]['score']))
                sim_count += 1

            if 'similar' in papers[dest_id]:
                papers[dest_id]['similar'].append((src_id, float(parts[2]), papers[src_id]['score']))
                sim_count += 1
        
        line = fp.readline()

# print("SIMILARITIES COUNT: " + str(sim_count))
# pp.pprint(papers)
result = []
for key in papers:
    if 'similar' in papers[key]: 
        score = papers[key]['score']

        # if it has similar papers
        if len(papers[key]['similar']) > 0:
            
            # gather scores of similar papers
            scores = [item[2] for item in papers[key]['similar']]
            # scores.append(score)

            if aggr == 'median':
                sim_score = statistics.median(scores)
            else:
                sim_score = statistics.mean(scores)
            
            score = alpha * score + (1-alpha) * sim_score

        result.append((papers[key]['code'], score, papers[key]['year']))

    else:
        result.append((papers[key]['code'], papers[key]['score'], papers[key]['year']))

result.sort(key = lambda x: x[1], reverse=True)  
for res in result:
    print(res[0] + "\t" + str(res[1]) + "\t" + str(res[2]))
