# ArXiv Research Dashboard

Automated synchronization of ArXiv papers to Notion with relevance scoring.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This tool automatically fetches recent papers from ArXiv, scores them based on configurable keywords, and syncs them to a Notion database. Designed for researchers who want to stay updated with the latest publications in their field.

**Key Features:**
- Hourly automated sync via GitHub Actions
- Configurable keyword-based relevance scoring (1-5 stars)
- Highlights top 5 most relevant papers
- Supports multiple ArXiv categories
- Includes full metadata: abstract, authors, PDF links

## Installation

### Prerequisites
- Python 3.11+
- Notion account with API access
- GitHub account (for automation)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jperret21/notion_news_sync.git
cd notion_news_sync
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a Notion integration at [notion.so/my-integrations](https://www.notion.so/my-integrations) and save the token.

4. Create a Notion database with these properties:
   - Title (Title)
   - URL (URL)
   - Date (Date)
   - Source (Text)
   - PDF (URL)
   - Keywords (Text)
   - Authors (Text)
   - Relevance (Select)
   - Status (Select)

5. Share the database with your integration and copy the database ID.

## Configuration

Create a `config.yaml` file:

```yaml
keywords:
  high_priority:
    - gravitational wave
    - black hole
    - neutron star
  
  medium_priority:
    - cosmology
    - dark matter
    - relativity
  
  low_priority:
    - numerical
    - simulation

arxiv_categories:
  - gr-qc
  - astro-ph.CO

days_lookback: 7
max_articles: 20
top_n: 5
```

Adjust keywords to match your research interests.

## Usage

### Local Execution

```bash
export NOTION_TOKEN="your_notion_integration_token"
export DATABASE_ID="your_notion_database_id"
python notion_news.py
```

### GitHub Actions (Automated)

1. Add repository secrets:
   - `NOTION_TOKEN`
   - `DATABASE_ID`

2. The workflow runs automatically every hour or can be triggered manually.

## Scoring System

Papers are scored based on keyword matches:

- **5 stars**: High-priority keywords detected
- **3 stars**: Medium-priority keywords detected
- **1 star**: Low-priority or no keyword matches

Top 5 highest-scored papers are marked with 🏆 for quick identification.

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `days_lookback` | Days to search backward | 7 |
| `max_articles` | Maximum articles to retain | 20 |
| `top_n` | Number of top articles to highlight | 5 |
| `arxiv_categories` | ArXiv categories to monitor | `['gr-qc']` |

### Available ArXiv Categories

- `gr-qc` - General Relativity and Quantum Cosmology
- `astro-ph.CO` - Cosmology and Nongalactic Astrophysics
- `astro-ph.HE` - High Energy Astrophysical Phenomena
- `hep-th` - High Energy Physics - Theory
- `quant-ph` - Quantum Physics

## Project Structure

```
notion_news_sync/
├── notion_news.py          # Main synchronization script
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
└── .github/workflows/
    └── notion_sync.yml     # Automation workflow
```

## Troubleshooting

**No articles found:**
- ArXiv doesn't publish on weekends. Increase `days_lookback` to 14 during holidays.
- Verify keywords match paper abstracts and titles.

**Notion API errors:**
- Ensure all required properties exist in the database.
- Verify integration has access to the database.

**GitHub Actions failures:**
- Check that secrets are correctly configured.
- Review workflow logs in the Actions tab.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [ArXiv API](https://arxiv.org/help/api/) for open access to research papers
- [Notion API](https://developers.notion.com/) for the integration platform

---

Project maintained by [jperret21](https://github.com/jperret21)
