# Product Review Based Aspect Extraction

This repository contains some basic methods for Aspect Extraction, as denoted in `Step 1` of [this research statement](https://docs.google.com/document/d/1-VFgAocdmJcEejerQfkIt7-rvZtvd4RbJiCQA9kwT7k/edit#heading=h.73dv0fqsq2nq).

## Directory structure

```
.
├── README.md
├── config      # config files
├── data        # compressed and decompressed txt data
├── label       # manually attached labels to use as test set
├── output      # generated output with file extension `*.keywords`
└── src         # code
```

## Papers

### Phrase extraction

id | paper | code
--- | --- | ---
autophrase | Shang et al., [Automated Phrase Mining from Massive Text Corpora](https://arxiv.org/abs/1702.04457), accepted by IEEE Transactions on Knowledge and Data Engineering, Feb. 2018 | https://github.com/luozhouyang/AutoPhraseX
kea | Witten et al., [KEA: Practical Automatic Keyphrase Extraction](https://www.cs.waikato.ac.nz/ml/publications/2005/chap_Witten-et-al_Windows.pdf), 2005. | https://github.com/boudinfl/pke
kpminer | El-Beltagy and Rafea, [KP-Miner: Participation in SemEval-2](https://aclanthology.org/S10-1041.pdf), 2010. | https://github.com/boudinfl/pke
multipart | Boudin, [Unsupervised Keyphrase Extraction with Multipartite Graphs](https://arxiv.org/abs/1803.08721), NAACL 2018. | https://github.com/boudinfl/pke
positionrank | Florescu and Caragea, [PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents](https://aclanthology.org/P17-1102.pdf), ACL 2017. | https://github.com/boudinfl/pke
singlerank | Wan and Xiao, [CollabRank: Towards a Collaborative Approach to Single-Document Keyphrase Extraction](https://aclanthology.org/C08-1122.pdf), 2008. | https://github.com/boudinfl/pke
textrank | Mihalcea and Tarau, [TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252.pdf), 2004. | https://github.com/boudinfl/pke
tfidf | - | https://github.com/boudinfl/pke
topicalpagerank | Sterckx et al., [Topical Word Importance for Fast Keyphrase Extraction](http://users.intec.ugent.be/cdvelder/papers/2015/sterckx2015wwwb.pdf), 2015 | https://github.com/boudinfl/pke
topicrank | Bougouin et al., [TopicRank: Graph-Based Topic Ranking for Keyphrase Extraction](https://aclanthology.org/I13-1062.pdf), 2013 | https://github.com/boudinfl/pke
yake | Campos et al., [YAKE! Keyword extraction from single documents using multiple local features](https://www.sciencedirect.com/science/article/abs/pii/S0020025519308588?via%3Dihub), 2020 | https://github.com/boudinfl/pke


### Aspect extraction

id | paper | code |supervised| result
--- | --- | --- | --- | ---
mate | Angelidis and Lapata, [Summarizing Opinions: Aspect Extraction Meets Sentiment Prediction and They Are Both Weakly Supervised](https://aclanthology.org/D18-1403/), | https://github.com/stangelid/oposum | semi- | on keyboard dataset from electronic data [mate.jsonl](https://hkustconnect-my.sharepoint.com/:u:/g/personal/ywangnx_connect_ust_hk/EXuVPWubkiNAm976Y0ZTcNkBY8NkvdQVuWqF_wE1-Q0B6g?e=lPugcS)
acos | Cai et al., [Aspect-Category-Opinion-Sentiment Quadruple Extraction with Implicit Aspects and Opinions](https://aclanthology.org/2021.acl-long.29.pdf), ACL 2021 | https://github.com/NUSTM/ACOS | yes
cat |[Embarrassingly Simple Unsupervised Aspect Extraction](https://aclanthology.org/2020.acl-main.290.pdf), ACL 2020| https://github.com/clips/cat| no
AspMem | Chao Zhao and Snigdha Chaturvedi, [Weakly-Supervised Opinion Summarization by Leveraging External Information](https://ojs.aaai.org//index.php/AAAI/article/view/6512), AAAI 2020 | https://github.com/zhaochaocs/AspMem | no | on keyboard dataset from electronic data [aspmem.json](https://hkustconnect-my.sharepoint.com/:u:/g/personal/ywangnx_connect_ust_hk/Edd0twDBpxZHtG3fR_iEXB8BoPCOxXfl9jneCaMWTfsUdg?e=N5KD3y)

## Run

```
pip install -r requirements.txt
cd src
python main.py
```
