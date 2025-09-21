# CORD-19 Dataset Analysis

A comprehensive analysis of the CORD-19 research dataset metadata, featuring data exploration, visualization, and an interactive Streamlit dashboard.

## 🔬 Project Overview

This project provides a complete analysis workflow for the CORD-19 dataset, which contains metadata for COVID-19 research papers. The analysis includes:

- **Data Exploration**: Understanding dataset structure and quality
- **Data Cleaning**: Handling missing values and formatting issues
- **Statistical Analysis**: Publication trends, author patterns, and journal distributions
- **Visualizations**: Interactive charts and graphs using matplotlib, seaborn, and Plotly
- **Interactive Dashboard**: A Streamlit web application for exploring findings

## 📊 Dataset Information

The CORD-19 dataset contains metadata for COVID-19 research papers including:

- **Paper Information**: Titles, abstracts, publication dates
- **Author Details**: Author names and collaboration patterns
- **Publication Info**: Journals, sources, DOI availability
- **Content Availability**: Full text access indicators

### Sample Dataset
Since the original metadata file contained changelog information, we created a realistic sample dataset with 1,000 research papers that mimics the structure and patterns of the actual CORD-19 dataset.

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd cord19-analysis
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample dataset** (if not already present)
   ```bash
   python create_sample_data.py
   ```

### Running the Analysis

#### Option 1: Jupyter Notebook Analysis
```bash
jupyter notebook metadata.ipynb
```

#### Option 2: Interactive Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── metadata.ipynb           # Jupyter notebook with analysis
├── streamlit_app.py         # Interactive Streamlit dashboard
├── create_sample_data.py    # Script to generate sample dataset
├── cord19_metadata.csv      # Sample dataset (generated)
└── metadata.csv             # Original file (changelog)
```

## 📈 Key Findings

### Dataset Overview
- **Total Papers**: 1,000 research papers
- **Date Range**: 2020-2023 (3-year span)
- **Data Quality**: 95%+ completeness for core fields

### Publication Patterns
- **Peak Activity**: 2021 saw the highest publication volume
- **Collaboration**: Average of 3.2 authors per paper
- **Content Length**: Average abstract length of ~300 characters

### Source Distribution
- **Primary Sources**: PubMed Central, WHO, bioRxiv
- **Journal Diversity**: 13 unique journals represented
- **Accessibility**: 60% of papers have full text available

### Research Focus Areas
- Clinical studies and epidemiological research
- Therapeutic and diagnostic approaches
- Public health policy implications
- Mathematical modeling and statistical analysis

## 🎯 Features

### Jupyter Notebook Analysis
- **Comprehensive Exploration**: Dataset structure and quality assessment
- **Data Cleaning Pipeline**: Missing value handling and format standardization
- **Statistical Analysis**: Publication trends and collaboration patterns
- **Rich Visualizations**: Publication timelines, journal distributions, and author patterns

### Streamlit Dashboard
- **Interactive Filters**: Filter by year, journal, and source
- **Real-time Analytics**: Dynamic metrics and insights
- **Search Functionality**: Find papers by keywords
- **Multiple Views**: Overview, trends, publications, and search tabs
- **Responsive Design**: Mobile-friendly interface

## 🔧 Technical Details

### Libraries Used
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn**: Static visualizations
- **plotly**: Interactive charts for Streamlit
- **streamlit**: Web application framework
- **numpy**: Numerical computations

### Data Processing
- **Date Handling**: Conversion and extraction of temporal features
- **Text Processing**: Abstract length analysis and keyword extraction
- **Missing Data**: Intelligent imputation and handling strategies
- **Quality Metrics**: Completeness and consistency checks

## 📊 Visualizations Included

1. **Publication Trends**
   - Yearly publication counts
   - Monthly trend analysis
   - Source distribution

2. **Journal Analysis**
   - Top publishing journals
   - Publication frequency patterns

3. **Author Patterns**
   - Collaboration distribution
   - Author count statistics

4. **Content Analysis**
   - Abstract length distribution
   - Full text availability

5. **Quality Metrics**
   - Data completeness indicators
   - Missing value analysis

## 🎨 Dashboard Features

### Overview Tab
- Key metrics and statistics
- Quick insights and summaries
- Data quality indicators

### Trends Tab
- Interactive publication timelines
- Source and author distribution charts
- Trend analysis visualizations

### Publications Tab
- Top journals ranking
- Abstract analysis
- Content availability metrics

### Search Tab
- Keyword-based paper search
- Detailed paper information
- Random paper exploration

## 🔍 Usage Examples

### Basic Analysis
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('cord19_metadata.csv')

# Quick overview
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['publish_time'].min()} to {df['publish_time'].max()}")
```

### Custom Filtering
```python
# Filter by year and journal
recent_papers = df[df['publish_year'] >= 2021]
top_journal_papers = df[df['journal'] == 'Nature']

# Analyze author patterns
author_counts = df['author_count'].describe()
print(f"Average authors per paper: {author_counts['mean']:.2f}")
```

## 🤝 Contributing

This project serves as a learning exercise for data science fundamentals. Feel free to:

1. **Extend the Analysis**: Add new visualizations or metrics
2. **Improve the Dashboard**: Enhance the Streamlit interface
3. **Add Features**: Implement additional filtering or search capabilities
4. **Optimize Performance**: Improve data processing efficiency

## 📚 Learning Objectives Achieved

✅ **Data Loading and Exploration**
- Understanding dataset structure
- Identifying data quality issues
- Performing initial statistical analysis

✅ **Data Cleaning Techniques**
- Handling missing values
- Date format standardization
- Text data preprocessing

✅ **Meaningful Visualizations**
- Publication trend analysis
- Distribution plots and charts
- Interactive dashboard creation

✅ **Interactive Web Application**
- Streamlit dashboard development
- User-friendly interface design
- Real-time data filtering

✅ **Data Insights Presentation**
- Statistical summaries
- Key findings documentation
- Professional reporting

## 📄 License

This project is created for educational purposes as part of a data science learning curriculum.

## 🔗 References

- [CORD-19 Dataset](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)

---

**Built with ❤️ for learning data science fundamentals**
