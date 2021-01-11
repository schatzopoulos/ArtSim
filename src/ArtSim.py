import sys
import pprint
import statistics
pp = pprint.PrettyPrinter(indent=4)

class ArtSim:
    _paper_ids = {}
    _papers = {}

    # read similarities
    def read_similarities(self, sim_file, sim_name, aggr):
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

                    if self._papers[src_id]['cold-start'] == True:
                        self._papers[src_id][sim_name].append((dest_id, float(parts[2]), self._papers[dest_id]['score']))

                    if self._papers[dest_id]['cold-start'] == True:
                        self._papers[dest_id][sim_name].append((src_id, float(parts[2]), self._papers[src_id]['score']))

                line = fp.readline()

        score_key = sim_name + "_score"

        # calculate average similarity scores for each paper in cold start
        for (paper_id, paper_details) in self._papers.items():

            if paper_details['cold-start'] == True:

                if len(paper_details[sim_name]) > 0:
                    paper_details[score_key] = self.aggregate_score(paper_details[sim_name], aggr)
                else:
                    paper_details[score_key] = 0.0

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
        for (paper_id, paper_details) in self._papers.items():
            paper_details['cold-start'] = paper_details['year'] >= cold_start_year


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
                    'PA': [],
                    'PT': []
                }

                line = fp.readline()

    def aggregate_score(self, sim_scores_array, aggr):
        scores = [item[2] for item in sim_scores_array]

        if aggr == 'median':
            return statistics.median(scores)
        else:
            return statistics.mean(scores)


    def run(self, alpha, beta, gamma, output_file):
        #print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

        fw = open(output_file, "w")

        for (paper_id, paper_details) in self._papers.items():

            if paper_details['cold-start'] == False:
                fw.write(paper_details['code'] + "\t" + str(paper_details['score']) + "\t" + str(paper_details['year']) + "\n")
                continue

            score = alpha * paper_details['PA_score'] + beta * paper_details['PT_score'] + gamma * paper_details['score']

            fw.write(paper_details['code'] + "\t" + str(score) + "\t" + str(paper_details['year']) + "\n")

        fw.close()
