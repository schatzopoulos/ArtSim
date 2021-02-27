import sys
import pprint
import statistics
pp = pprint.PrettyPrinter(indent=4)

class ArtSim:
    _paper_ids = {}
    _papers = {}
    _venue_scores = {}

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

                    if self._papers[src_id]['cold-start'] == True:
                        self._papers[src_id][sim_name]['score'] += float(self._papers[dest_id]['score'])
                        self._papers[src_id][sim_name]['count'] += 1

                    if self._papers[dest_id]['cold-start'] == True:
                        self._papers[dest_id][sim_name]['score'] += float(self._papers[src_id]['score'])
                        self._papers[dest_id][sim_name]['count'] += 1

                line = fp.readline()


        # calculate average similarity scores for each paper in cold start
        for (paper_id, paper_details) in self._papers.items():

            if paper_details['cold-start'] == True:

                if paper_details[sim_name]['score'] > 0:
                    paper_details[sim_name]['score'] /= paper_details[sim_name]['count']

    def read_connections(self, con_file, sim_name):
        with open(con_file) as fp:
            line = fp.readline()
            while line:
                line = line.rstrip()
                parts = line.split("\t")

                paper_id = int(parts[0])
                venue_id = int(parts[1])

                # keep similarities for those papers inside the training set
                if paper_id in self._papers:

                    if venue_id not in self._venue_scores:
                        self._venue_scores[venue_id] = { 'score': 0.0, 'count': 0 }

                    self._venue_scores[venue_id]['score'] += self._papers[paper_id]['score']
                    self._venue_scores[venue_id]['count'] += 1
                    self._papers[paper_id]['venue'] = venue_id

                line = fp.readline()

        # calculate average score for each paper in venue
        for (venue_id, venue_details) in self._venue_scores.items():
            #print("Venue: " +  str(venue_id) + "\t" + str(venue_details['score']))
            if venue_details['score'] > 0:
                venue_details['score'] /= venue_details['count']

        # calculate average similarity scores for each paper in cold start
        for (paper_id, paper_details) in self._papers.items():

            if paper_details['cold-start'] == True:

                if paper_details['venue'] in self._venue_scores:
                    paper_details[sim_name]['score'] = float(self._venue_scores[paper_details['venue']]['score'])
                else:
                    paper_details[sim_name]['score'] = 0.0

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
                    'venue': -1,
                    'PA': { 'score': 0.0, 'count': 0 },
                    'PT': { 'score': 0.0, 'count': 0 },
                    'PV': { 'score': 0.0 }
                }

                line = fp.readline()

    def run(self, alpha, beta, gamma, delta, output_file):
        #print (str(alpha) + "\t" + str(beta) + "\t" + str(gamma))

        results = []

        for (paper_id, paper_details) in self._papers.items():
            score = 0.0

            if paper_details['cold-start'] == False:
                score = paper_details['score']
            else:
                score = alpha * paper_details['PA']['score'] + beta * paper_details['PT']['score'] + gamma * paper_details['PV']['score'] + delta * paper_details['score']

            results.append((paper_details['code'], float(score)))

        return results
