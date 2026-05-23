# Football Fan Community Analysis — r/soccer
### COSC 2671 / COSC 3047 — Social Media and Network Analysis
### Assignment 2 — Group Project

---

## Project Overview
This project analyses football fan communities on Reddit using data from r/soccer
during the 2022 FIFA World Cup (November–December 2022).

**Research Question:**
*Who are the most influential users in football discussions on Reddit, what topics
dominate fan discourse, and how does sentiment vary across user communities?*

---

## Folder Structure
```
SMAA-A2/
├── data/
│   ├── posts_soccer.json       # 25,779 posts from r/soccer
│   └── comments_soccer.json    # 50,000 comments from r/soccer
│
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory Data Analysis
│   ├── 02_sentiment.ipynb      # VADER Sentiment Analysis
│   ├── 03_topic_modelling.ipynb # LDA Topic Modelling
│   └── 04_network_analysis.ipynb # Network, Centrality, Community Detection
│
├── scripts/
│   └── download_reddit_data.py # Data collection script (Arctic Shift API)
│
├── figures/                    # All output figures saved here
│
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Create virtual environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Download NLTK data (first run only)
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### 4. Run notebooks in order
```
01_eda.ipynb              → Run first
02_sentiment.ipynb        → Run second
03_topic_modelling.ipynb  → Run third
04_network_analysis.ipynb → Run last
```

Each notebook loads the data independently — no need to pass state between them.

---

## Data
- **Source:** r/soccer subreddit via Arctic Shift (https://arctic-shift.photon-reddit.com)
- **Period:** 2022-11-01 to 2022-12-20 (FIFA World Cup 2022)
- **Posts:** 25,779 (title, author, score, flair, timestamp, upvote_ratio)
- **Comments:** 50,000 (body, author, parent_id, score, timestamp)
- **Collection method:** Arctic Shift public API — no Reddit API key required
- **No private data, no API keys included**

---

## Analysis Pipeline

| Notebook | Techniques | Key Outputs |
|---|---|---|
| 01_eda | Descriptive stats, time series | Activity plots, flair distribution |
| 02_sentiment | VADER, time-series sentiment | Sentiment distribution, trends, by flair |
| 03_topic_modelling | LDA (gensim), WordCloud | 8 topics, word cloud, topic distribution |
| 04_network_analysis | NetworkX, Louvain, PageRank, Betweenness | Network graph, centrality rankings, communities |

---

## Key Findings (to be updated after full run)
- Most influential users identified via PageRank
- Community structure detected via Louvain algorithm
- Sentiment trends correlate with match outcomes
- Dominant topics: transfers, match reactions, player performance

---

## Dependencies
See `requirements.txt`

## Academic Integrity
All code is original. External packages used are acknowledged above.
Data collected from a public platform under fair academic use.
No API keys, credentials, or private data are included in this submission.
