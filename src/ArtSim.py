import sys
import pprint
import statistics
pp = pprint.PrettyPrinter(indent=4)

class ArtSim:
    _paper_ids = {}
    _papers = {}

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
                    
                    self.check_paper_in_similarities(src_id)
                    self.check_paper_in_similarities(dest_id)

                    self._papers[src_id][sim_name].append((dest_id, float(parts[2]), self._papers[dest_id]['score']))
                    self._papers[dest_id][sim_name].append((src_id, float(parts[2]), self._papers[src_id]['score']))
                    
                line = fp.readline()

    def check_paper_in_similarities(self, paper_id):
        if paper_id not in self._similarities:
            #self._similarities[paper_id] = {}
            self._papers[paper_id]['PA'] = []
            self._papers[paper_id]['PT'] = []

    # load paper code & ids
    def read_paper_ids(self, paper_details):
        with open(paper_details, encoding="utf8") as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")
                self._paper_ids[parts[1]] = int(parts[0])   
                line = fp.readline()

    def mark_cold_start_papers(self, cold_start_year):
        for key in self._papers:
            self._papers[key]['cold-start'] = self._papers[key]['year'] >= cold_start_year

    # read paper scores and publication year
    def read_paper_scores(self, scores_file):
        
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
                }

                line = fp.readline()
    
    def aggregate_score(self, sim_scores_array, aggr):
        scores_PA = [item[2] for item in sim_scores_array]

        if aggr == 'median':
            return statistics.median(scores_PA)
        else:
            return statistics.mean(scores_PA)


    def run(self, alpha, beta, gamma, aggr, output_file):
        print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

        fw = open(output_file, "w")

        for (paper_id, paper_details) in self._papers.items():
            
            if paper_details['cold-start'] == False:
                fw.write(paper_details['code'] + "\t" + str(paper_details['score']) + "\t" + str(paper_details['year']) + "\n")
                continue
             
            score = paper_details['score']

            # calculate score from PA similarities
            sim_score_PA = 0.0
            if len(paper_details['PA']) > 0:
                sim_score_PA = self.aggregate_score(paper_details['PA'], aggr)
                
            # calculate score from PT similarities
            sim_score_PT = 0.0    
            if len(paper_details['PT']) > 0:
                sim_score_PT = self.aggregate_score(paper_details['PT'], aggr)

            score = alpha * sim_score_PA + beta * sim_score_PT + gamma * score

            fw.write(paper_details['code'] + "\t" + str(score) + "\t" + str(paper_details['year']) + "\n")
                
        fw.close()
        
