import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="CORD-19 Dataset Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('cord19_metadata.csv')
        # Clean the data
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['publish_year'] = df['publish_time'].dt.year
        df['publish_month'] = df['publish_time'].dt.month
        df['abstract'] = df['abstract'].fillna('No abstract available')
        df['journal'] = df['journal'].fillna('Unknown Journal')
        df['doi'] = df['doi'].fillna('No DOI available')
        df['author_count'] = df['authors'].str.split(',').str.len()
        df['abstract_length'] = df['abstract'].str.len()
        return df
    except FileNotFoundError:
        st.error("Dataset file 'cord19_metadata.csv' not found. Please make sure the file exists.")
        return None

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 CORD-19 Dataset Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Analysis of COVID-19 Research Papers")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.title("📊 Analysis Options")
    
    # Filters
    st.sidebar.subheader("🔍 Filters")
    
    # Year filter
    available_years = sorted(df['publish_year'].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=available_years,
        default=available_years
    )
    
    # Journal filter
    top_journals = df['journal'].value_counts().head(20)
    selected_journals = st.sidebar.multiselect(
        "Select Journals",
        options=top_journals.index.tolist(),
        default=[]
    )
    
    # Source filter
    sources = df['source_x'].unique()
    selected_sources = st.sidebar.multiselect(
        "Select Sources",
        options=sources,
        default=sources
    )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_years:
        filtered_df = filtered_df[filtered_df['publish_year'].isin(selected_years)]
    if selected_journals:
        filtered_df = filtered_df[filtered_df['journal'].isin(selected_journals)]
    if selected_sources:
        filtered_df = filtered_df[filtered_df['source_x'].isin(selected_sources)]
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Trends", "📚 Publications", "🔍 Search"])
    
    with tab1:
        st.header("Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Papers",
                value=f"{len(filtered_df):,}",
                delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
            )
        
        with col2:
            st.metric(
                label="Unique Journals",
                value=f"{filtered_df['journal'].nunique():,}"
            )
        
        with col3:
            avg_authors = filtered_df['author_count'].mean()
            st.metric(
                label="Avg Authors/Paper",
                value=f"{avg_authors:.1f}"
            )
        
        with col4:
            full_text_pct = (filtered_df['has_full_text'].sum() / len(filtered_df)) * 100
            st.metric(
                label="Full Text Available",
                value=f"{full_text_pct:.1f}%"
            )
        
        # Quick insights
        st.subheader("🔍 Quick Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
                <h4>📈 Publication Patterns</h4>
                <ul>
                    <li>Most active year: <strong>{}</strong></li>
                    <li>Date range: <strong>{} to {}</strong></li>
                    <li>Average abstract length: <strong>{:.0f} characters</strong></li>
                </ul>
            </div>
            """.format(
                filtered_df['publish_year'].mode().iloc[0] if not filtered_df.empty else "N/A",
                filtered_df['publish_time'].min().strftime('%Y-%m-%d') if not filtered_df.empty else "N/A",
                filtered_df['publish_time'].max().strftime('%Y-%m-%d') if not filtered_df.empty else "N/A",
                filtered_df['abstract_length'].mean() if not filtered_df.empty else 0
            ), unsafe_allow_html=True)
        
        with col2:
            top_source = filtered_df['source_x'].mode().iloc[0] if not filtered_df.empty else "N/A"
            top_journal = filtered_df['journal'].mode().iloc[0] if not filtered_df.empty else "N/A"
            
            st.markdown("""
            <div class="insight-box">
                <h4>🏆 Top Contributors</h4>
                <ul>
                    <li>Most common source: <strong>{}</strong></li>
                    <li>Most active journal: <strong>{}</strong></li>
                    <li>Data quality: <strong>{:.1f}% complete</strong></li>
                </ul>
            </div>
            """.format(
                top_source,
                top_journal,
                ((filtered_df['abstract'] != 'No abstract available').sum() / len(filtered_df)) * 100 if not filtered_df.empty else 0
            ), unsafe_allow_html=True)
    
    with tab2:
        st.header("Publication Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Publications by year
            yearly_counts = filtered_df['publish_year'].value_counts().sort_index()
            
            fig_year = px.bar(
                x=yearly_counts.index,
                y=yearly_counts.values,
                title="Publications by Year",
                labels={'x': 'Year', 'y': 'Number of Publications'},
                color=yearly_counts.values,
                color_continuous_scale='Blues'
            )
            fig_year.update_layout(showlegend=False)
            st.plotly_chart(fig_year, use_container_width=True)
        
        with col2:
            # Monthly trends
            monthly_data = filtered_df.groupby(['publish_year', 'publish_month']).size().reset_index(name='count')
            monthly_data['date'] = pd.to_datetime(monthly_data[['publish_year', 'publish_month']].assign(day=1))
            
            fig_month = px.line(
                monthly_data,
                x='date',
                y='count',
                title="Monthly Publication Trends",
                labels={'x': 'Date', 'y': 'Number of Publications'}
            )
            fig_month.update_traces(line=dict(width=3))
            st.plotly_chart(fig_month, use_container_width=True)
        
        # Source distribution
        col1, col2 = st.columns(2)
        
        with col1:
            source_counts = filtered_df['source_x'].value_counts()
            fig_source = px.pie(
                values=source_counts.values,
                names=source_counts.index,
                title="Publications by Source"
            )
            st.plotly_chart(fig_source, use_container_width=True)
        
        with col2:
            # Author count distribution
            fig_author = px.histogram(
                filtered_df,
                x='author_count',
                nbins=20,
                title="Distribution of Authors per Paper",
                labels={'author_count': 'Number of Authors', 'count': 'Frequency'}
            )
            st.plotly_chart(fig_author, use_container_width=True)
    
    with tab3:
        st.header("Publication Details")
        
        # Top journals
        st.subheader("🏆 Top Publishing Journals")
        top_journals_filtered = filtered_df['journal'].value_counts().head(10)
        
        fig_journals = px.bar(
            x=top_journals_filtered.values,
            y=top_journals_filtered.index,
            orientation='h',
            title="Top 10 Journals by Publication Count",
            labels={'x': 'Number of Publications', 'y': 'Journal'}
        )
        fig_journals.update_layout(height=400)
        st.plotly_chart(fig_journals, use_container_width=True)
        
        # Abstract length analysis
        col1, col2 = st.columns(2)
        
        with col1:
            fig_abstract = px.histogram(
                filtered_df,
                x='abstract_length',
                nbins=30,
                title="Abstract Length Distribution",
                labels={'abstract_length': 'Abstract Length (characters)', 'count': 'Frequency'}
            )
            st.plotly_chart(fig_abstract, use_container_width=True)
        
        with col2:
            # Full text availability
            full_text_counts = filtered_df['has_full_text'].value_counts()
            fig_fulltext = px.pie(
                values=full_text_counts.values,
                names=['Available', 'Not Available'],
                title="Full Text Availability",
                color_discrete_map={'Available': '#2E8B57', 'Not Available': '#DC143C'}
            )
            st.plotly_chart(fig_fulltext, use_container_width=True)
    
    with tab4:
        st.header("Search and Explore")
        
        # Search functionality
        search_term = st.text_input("🔍 Search in titles and abstracts", placeholder="Enter keywords...")
        
        if search_term:
            # Filter papers containing search term
            mask = filtered_df['title'].str.contains(search_term, case=False, na=False) | \
                   filtered_df['abstract'].str.contains(search_term, case=False, na=False)
            search_results = filtered_df[mask]
            
            st.write(f"Found {len(search_results)} papers matching '{search_term}'")
            
            if len(search_results) > 0:
                # Display results
                for idx, paper in search_results.head(10).iterrows():
                    with st.expander(f"📄 {paper['title'][:100]}..."):
                        st.write(f"**Authors:** {paper['authors']}")
                        st.write(f"**Journal:** {paper['journal']}")
                        st.write(f"**Published:** {paper['publish_time'].strftime('%Y-%m-%d') if pd.notna(paper['publish_time']) else 'Unknown'}")
                        st.write(f"**Source:** {paper['source_x']}")
                        st.write(f"**Full Text Available:** {'Yes' if paper['has_full_text'] else 'No'}")
                        st.write(f"**Abstract:** {paper['abstract'][:500]}...")
                        
                        if paper['doi'] != 'No DOI available':
                            st.write(f"**DOI:** {paper['doi']}")
        else:
            # Show random sample of papers
            st.subheader("📚 Sample Papers")
            sample_papers = filtered_df.sample(min(5, len(filtered_df)))
            
            for idx, paper in sample_papers.iterrows():
                with st.expander(f"📄 {paper['title'][:100]}..."):
                    st.write(f"**Authors:** {paper['authors']}")
                    st.write(f"**Journal:** {paper['journal']}")
                    st.write(f"**Published:** {paper['publish_time'].strftime('%Y-%m-%d') if pd.notna(paper['publish_time']) else 'Unknown'}")
                    st.write(f"**Source:** {paper['source_x']}")
                    st.write(f"**Full Text Available:** {'Yes' if paper['has_full_text'] else 'No'}")
                    st.write(f"**Abstract:** {paper['abstract'][:500]}...")
                    
                    if paper['doi'] != 'No DOI available':
                        st.write(f"**DOI:** {paper['doi']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔬 CORD-19 Dataset Analysis Dashboard | Built with Streamlit</p>
        <p>This dashboard provides interactive analysis of COVID-19 research papers metadata</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
