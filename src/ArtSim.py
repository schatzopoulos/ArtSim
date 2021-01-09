import sys
import pprint
import statistics
pp = pprint.PrettyPrinter(indent=4)

class ArtSim:
    _paper_ids = {}
    _papers = {}
    _similarities = {}

    # read similarities
    def read_similarities(self, sim_file, sim_name):
        sim_count = 0
        with open(sim_file) as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                
                src_id = int(parts[0])
                dest_id = int(parts[1])

                # keep similarities for those papers inside the training set
                if src_id in self._papers and dest_id in self._papers:

                    self._similarities[src_id][sim_name].append((dest_id, float(parts[2]), self._papers[dest_id]['score']))
                    self._similarities[dest_id][sim_name].append((src_id, float(parts[2]), self._papers[src_id]['score']))
                
                line = fp.readline()

    # load paper code & ids
    def read_paper_ids(self, paper_details):
        with open(paper_details, encoding="utf8") as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                self._paper_ids[parts[1]] = int(parts[0])   
                line = fp.readline()

    # read paper scores and publication year
    def read_paper_scores(self, scores_file, cold_start_year):
        
        with open(scores_file) as fp:

            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                pub_year = int(parts[2])

                paper_id = self._paper_ids[parts[0]]
                self._papers[paper_id] = {
                    'code': parts[0],
                    'score': float(parts[1]), 
                    'year': pub_year,
                    'inColdStart': pub_year >= cold_start_year
                }

                # TODO: move to init function so as to reuse function
                # if pub_year >= cold_start_year:

                #     self._papers[paper_id] = {}
                #     self._papers[paper_id]['PA'] = []
                #     self._papers[paper_id]['PT'] = []

                #     papers_in_cold_start_num += 1

                line = fp.readline()
    
    def aggregate_score(self, paper_id, similarity_type, aggr):
        scores_PA = [item[2] for item in self._similarities[paper_id][similarity_type]]

        if aggr == 'median':
            return statistics.median(scores_PA)
        else:
            return statistics.mean(scores_PA)


    def run(self, alpha, beta, gamma, aggr, output_file):
        print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

        fw = open(output_file, "w")

        for key in self._papers:
            if self._papers[key]['inColdStart'] == True: 
                score = self._papers[key]['score']

                # calculate score from PA similarities
                sim_score_PA = 0.0
                if len(self._similarities[key]['PA']) > 0:
                    sim_score_PA = self.aggregate_score(key, 'PA', aggr)
                    

                sim_score_PT = 0.0    
                if len(self._similarities[key]['PT']) > 0:

                    # calculate score from PT similarities
                    scores_PT = self.aggregate_score(key, 'PT', aggr)

                score = alpha * sim_score_PA + beta * sim_score_PT + gamma * score

                fw.write(self._papers[key]['code'] + "\t" + str(score) + "\t" + str(self._papers[key]['year']) + "\n")

            else:
                fw.write(self._papers[key]['code'] + "\t" + str(self._papers[key]['score']) + "\t" + str(self._papers[key]['year']) + "\n")
        fw.close()
        
