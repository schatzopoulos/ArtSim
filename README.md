# ArtSim & ArtSim+

This repository contains the code for the article "ArtSim: Improved estimation of current impact for recent articles." published in AIMinScience workshop @ TPDL 2020 and its extension ArtSim+.



## Installation
TODO

## Execution

ArtSim and ArtSim+ can be executed with the scripts `artsim.py` and `artsim_plus.py` respectively as follows:

```
python3 artsim.py <paper_file> <scores_file> <pap_similarities_file> <ptp_similarities_file> <pv_connections_file> <cold_start_year> <evaluation_method> <ndcg:k>
```

where 

  * `paper_file` is a tsv file for mapping internal numeric ids to actual paper ids
  * `scores_file` contains paper ids and their popularity scores computed by a popularity method
  * `pap_similarities_file` and `ptp_similarities_file` are files containing similarities based on authors and topics respectively; they contain tuples of numeric paper ids with their respecitive similarity score. `pv_connections_file` contains the paper to venue relationships. The files we used for our experiments with the DBLP dataset can be found at (Zenodo)[https://zenodo.org/record/4567527]
  * `cold_start_year` is the year after which we consider articles being in their cold start period.
  * `evaluation_method` can be one of 'tau' or 'ndcg'
  * in case of selecting 'ndcg' as an evaluation method in the previous parameter, we should also provide the `k` parameter of ndcg as an extra parameter



Please cite:

```
@inproceedings{chatzopoulos2020artsim,
  title={Artsim: improved estimation of current impact for recent articles},
  author={Chatzopoulos, Serafeim and Vergoulis, Thanasis and Kanellos, Ilias and Dalamagas, Theodore and Tryfonopoulos, Christos},
  booktitle={ADBIS, TPDL and EDA 2020 Common Workshops and Doctoral Consortium},
  pages={323--334},
  year={2020},
  organization={Springer}
}
```
