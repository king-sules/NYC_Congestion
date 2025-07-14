# NYC Congestion Pricing Analysis

This project analyzes the impact of NYC's congestion pricing program using machine learning techniques and data visualization.

## Project Overview

New York City's congestion pricing program aims to reduce traffic congestion, improve air quality, and generate revenue for public transportation improvements. This project examines various metrics to understand the program's effectiveness.

## Key Metrics Analyzed

- **Emissions Data**: Air quality improvements and carbon footprint reduction
- **Foot Traffic**: Changes in pedestrian activity in affected zones
- **Subway Ridership**: Public transportation usage patterns
- **Traffic Volume**: Vehicle count changes in congestion zones
- **Economic Impact**: Business activity and revenue effects
- **Public Opinion**: Sentiment analysis of public response

## Project Structure

```
conjestion/
├── notebooks/           # Jupyter notebooks for analysis
├── data/               # Data files and datasets
├── src/                # Source code and utilities
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch Jupyter:
   ```bash
   jupyter lab
   ```

3. Start with `01_data_collection.ipynb` to gather and prepare data

## Notebooks

- `01_data_collection.ipynb` - Data gathering and preprocessing
- `02_emissions_analysis.ipynb` - Air quality and emissions analysis
- `03_traffic_patterns.ipynb` - Traffic volume and flow analysis
- `04_public_transport.ipynb` - Subway and bus ridership analysis
- `05_foot_traffic.ipynb` - Pedestrian activity analysis
- `06_economic_impact.ipynb` - Business and economic effects
- `07_sentiment_analysis.ipynb` - Public opinion analysis
- `08_comprehensive_analysis.ipynb` - Integrated findings and conclusions

## Data Sources

- NYC Open Data Portal
- MTA (Metropolitan Transportation Authority)
- EPA Air Quality Data
- NYC DOT Traffic Data
- Social Media APIs for sentiment analysis

## Technologies Used

- Python 3.8+
- Jupyter Notebooks
- Pandas, NumPy, Matplotlib, Seaborn
- Scikit-learn for ML models
- Plotly for interactive visualizations
- NLTK for text analysis 