import sys
import pprint
import statistics
pp = pprint.PrettyPrinter(indent=4)

class ArtSim:
    _paper_ids = {}
    _papers = {}

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
                if src_id in _papers and dest_id in _papers:

                    # 'similar' field is present only for papers in cold start
                    if 'similar' in _papers[src_id]:
                        _papers[src_id]['similar'][sim_name].append((dest_id, float(parts[2]), _papers[dest_id]['score']))
                        sim_count += 1

                    if 'similar' in papers[dest_id]:
                        _papers[dest_id]['similar'][sim_name].append((src_id, float(parts[2]), _papers[src_id]['score']))
                        sim_count += 1
                
                line = fp.readline()

    # load paper code & ids
    def read_paper_ids(paper_details):
        with open(paper_details, encoding="utf8") as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                _paper_ids[parts[1]] = int(parts[0])   
                line = fp.readline()

    # read paper scores and publication year
    def read_paper_scores(scores_file, cold_start_year):
        
        papers_num = 0
        papers_in_cold_start_num = 0

        with open(scores_file) as fp:

            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                pub_year = int(parts[2])

                paper_id = _paper_ids[parts[0]]
                _papers[paper_id] = {
                    'code': parts[0],
                    'score': float(parts[1]), 
                    'year': pub_year
                }

                # TODO: move to init function so as to reuse function
                if pub_year >= cold_start_year:
                    _papers[paper_id]['similar'] = {}
                    _papers[paper_id]['similar']['PA'] = []
                    _papers[paper_id]['similar']['PT'] = []

                    papers_in_cold_start_num += 1

                line = fp.readline()
                papers_num += 1
        return papers_num, papers_in_cold_start_num


    def run(alpha, beta, gamma, output_file):
        print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

        fw = open(output_file, "w")

        for key in _papers:
            if 'similar' in _papers[key]: 
                score = _papers[key]['score']

                sim_score_PA = 0.0
                if len(_papers[key]['similar']['PA']) > 0:

                    # calculate score from PA similarities
                    scores_PA = [item[2] for item in _papers[key]['similar']['PA']]

                    if aggr == 'median':
                        sim_score_PA = statistics.median(scores_PA)
                    else:
                        sim_score_PA = statistics.mean(scores_PA)

                sim_score_PT = 0.0    
                if  len(_papers[key]['similar']['PT']) > 0:

                    # calculate score from PT similarities
                    scores_PT = [item[2] for item in _papers[key]['similar']['PT']]

                    if aggr == 'median':
                        sim_score_PT = statistics.median(scores_PT)
                    else:
                        sim_score_PT = statistics.mean(scores_PT)

                score = alpha * sim_score_PA + beta * sim_score_PT + gamma * score

                fw.write(_papers[key]['code'] + "\t" + str(score) + "\t" + str(_papers[key]['year']) + "\n")

            else:
                fw.write(_papers[key]['code'] + "\t" + str(_papers[key]['score']) + "\t" + str(_papers[key]['year']) + "\n")
        fw.close()
        