"""
Utility functions for NYC Congestion Pricing Analysis

This module contains helper functions used across the analysis notebooks.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_sample_emissions_data(start_date='2023-01-01', end_date='2024-01-01'):
    """
    Create sample emissions data for NYC congestion pricing analysis.
    
    Parameters:
    -----------
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
        
    Returns:
    --------
    pd.DataFrame
        Sample emissions data
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    congestion_start = pd.Timestamp('2023-06-01')
    
    # Simulate congestion pricing effect (reduction after June 2023)
    emissions_data = pd.DataFrame({
        'date': dates,
        'pm25': np.where(dates >= congestion_start, 
                         np.random.normal(30, 8, len(dates)),  # Lower after congestion pricing
                         np.random.normal(40, 10, len(dates))), # Higher before
        'pm10': np.where(dates >= congestion_start,
                         np.random.normal(45, 12, len(dates)),
                         np.random.normal(55, 15, len(dates))),
        'o3': np.where(dates >= congestion_start,
                       np.random.normal(40, 15, len(dates)),
                       np.random.normal(50, 20, len(dates))),
        'no2': np.where(dates >= congestion_start,
                        np.random.normal(20, 6, len(dates)),
                        np.random.normal(30, 8, len(dates))),
        'co': np.where(dates >= congestion_start,
                       np.random.normal(0.6, 0.2, len(dates)),
                       np.random.normal(1.0, 0.3, len(dates)))
    })
    
    # Add congestion pricing period indicator
    emissions_data['congestion_pricing'] = emissions_data['date'] >= pd.Timestamp('2023-06-01')
    emissions_data['period'] = emissions_data['congestion_pricing'].map({True: 'After CP', False: 'Before CP'})
    
    return emissions_data

def create_sample_traffic_data(start_date='2023-01-01', end_date='2024-01-01'):
    """
    Create sample traffic data for NYC congestion pricing analysis.
    
    Parameters:
    -----------
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
        
    Returns:
    --------
    pd.DataFrame
        Sample traffic data
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    congestion_start = pd.Timestamp('2023-06-01')
    
    traffic_data = []
    
    for date in dates:
        # Base traffic volume with daily and weekly patterns
        hour = date.hour
        day_of_week = date.dayofweek
        
        # Peak hours (7-9 AM, 5-7 PM)
        if hour in [7, 8, 9] or hour in [17, 18, 19]:
            base_volume = 1200
        elif hour in [10, 11, 12, 13, 14, 15, 16]:
            base_volume = 800
        else:
            base_volume = 400
        
        # Weekend effect
        if day_of_week >= 5:  # Weekend
            base_volume *= 0.7
        
        # Congestion pricing effect
        if date >= congestion_start:
            # Reduce traffic by 15-25% depending on time
            reduction = 0.20 if hour in [7, 8, 9, 17, 18, 19] else 0.15
            base_volume *= (1 - reduction)
        
        # Add noise
        volume = max(0, np.random.normal(base_volume, base_volume * 0.1))
        
        # Travel time (inverse relationship with volume)
        travel_time = 20 + (volume / 100) * 2 + np.random.normal(0, 2)
        
        traffic_data.append({
            'timestamp': date,
            'volume': int(volume),
            'travel_time': max(5, travel_time),
            'speed': max(5, 30 - (volume / 100)),
            'congestion_level': 'High' if volume > 1000 else 'Medium' if volume > 600 else 'Low'
        })
    
    traffic_df = pd.DataFrame(traffic_data)
    
    # Add time-based features
    traffic_df['date'] = pd.to_datetime(traffic_df['timestamp'])
    traffic_df['hour'] = traffic_df['date'].dt.hour
    traffic_df['day_of_week'] = traffic_df['date'].dt.dayofweek
    traffic_df['day_name'] = traffic_df['date'].dt.day_name()
    traffic_df['month'] = traffic_df['date'].dt.month
    traffic_df['congestion_pricing'] = traffic_df['date'] >= pd.Timestamp('2023-06-01')
    traffic_df['period'] = traffic_df['congestion_pricing'].map({True: 'After CP', False: 'Before CP'})
    
    return traffic_df

def create_sample_mta_data(start_date='2023-01-01', end_date='2024-01-01'):
    """
    Create sample MTA ridership data for NYC congestion pricing analysis.
    
    Parameters:
    -----------
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
        
    Returns:
    --------
    pd.DataFrame
        Sample MTA data
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    congestion_start = pd.Timestamp('2023-06-01')
    
    mta_data = []
    
    for date in dates:
        day_of_week = date.dayofweek
        
        # Base ridership with weekly patterns
        if day_of_week < 5:  # Weekday
            base_subway = 5500000  # 5.5M daily riders
            base_bus = 2200000     # 2.2M daily riders
        else:  # Weekend
            base_subway = 3500000  # 3.5M daily riders
            base_bus = 1500000     # 1.5M daily riders
        
        # Congestion pricing effect (increase after June 2023)
        if date >= congestion_start:
            # Increase ridership by 8-12%
            subway_increase = 0.10
            bus_increase = 0.08
            base_subway *= (1 + subway_increase)
            base_bus *= (1 + bus_increase)
        
        # Add seasonal variation
        month = date.month
        if month in [12, 1, 2]:  # Winter
            seasonal_factor = 0.95
        elif month in [6, 7, 8]:  # Summer
            seasonal_factor = 0.90
        else:
            seasonal_factor = 1.0
        
        base_subway *= seasonal_factor
        base_bus *= seasonal_factor
        
        # Add noise
        subway_riders = max(0, np.random.normal(base_subway, base_subway * 0.05))
        bus_riders = max(0, np.random.normal(base_bus, base_bus * 0.05))
        
        mta_data.append({
            'date': date,
            'subway_riders': int(subway_riders),
            'bus_riders': int(bus_riders),
            'total_riders': int(subway_riders + bus_riders)
        })
    
    mta_df = pd.DataFrame(mta_data)
    
    # Add time-based features
    mta_df['date'] = pd.to_datetime(mta_df['date'])
    mta_df['day_of_week'] = mta_df['date'].dt.dayofweek
    mta_df['day_name'] = mta_df['date'].dt.day_name()
    mta_df['month'] = mta_df['date'].dt.month
    mta_df['congestion_pricing'] = mta_df['date'] >= pd.Timestamp('2023-06-01')
    mta_df['period'] = mta_df['congestion_pricing'].map({True: 'After CP', False: 'Before CP'})
    
    return mta_df

def calculate_percentage_change(before_data, after_data):
    """
    Calculate percentage change between two datasets.
    
    Parameters:
    -----------
    before_data : pd.Series or array-like
        Data from before period
    after_data : pd.Series or array-like
        Data from after period
        
    Returns:
    --------
    float
        Percentage change
    """
    before_mean = np.mean(before_data)
    after_mean = np.mean(after_data)
    
    if before_mean == 0:
        return 0
    
    return ((after_mean - before_mean) / before_mean) * 100

def perform_statistical_test(before_data, after_data, alpha=0.05):
    """
    Perform t-test to compare before and after periods.
    
    Parameters:
    -----------
    before_data : pd.Series or array-like
        Data from before period
    after_data : pd.Series or array-like
        Data from after period
    alpha : float
        Significance level
        
    Returns:
    --------
    dict
        Dictionary containing test results
    """
    from scipy import stats
    
    # Perform t-test
    t_stat, p_value = stats.ttest_ind(before_data, after_data)
    
    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt(((len(before_data) - 1) * np.var(before_data) + 
                          (len(after_data) - 1) * np.var(after_data)) / 
                         (len(before_data) + len(after_data) - 2))
    cohens_d = (np.mean(after_data) - np.mean(before_data)) / pooled_std
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'significant': p_value < alpha,
        'before_mean': np.mean(before_data),
        'after_mean': np.mean(after_data),
        'percentage_change': calculate_percentage_change(before_data, after_data)
    }

def create_time_series_plot(df, date_col, value_col, period_col, title, figsize=(12, 6)):
    """
    Create a time series plot comparing before and after periods.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_col : str
        Name of date column
    value_col : str
        Name of value column to plot
    period_col : str
        Name of period column ('Before CP' or 'After CP')
    title : str
        Plot title
    figsize : tuple
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for period in ['Before CP', 'After CP']:
        period_data = df[df[period_col] == period]
        ax.plot(period_data[date_col], period_data[value_col], 
               label=period, alpha=0.7, linewidth=1)
    
    # Add congestion pricing start line
    ax.axvline(x=pd.Timestamp('2023-06-01'), color='red', linestyle='--', 
               alpha=0.8, label='Congestion Pricing Start')
    
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel(value_col.replace('_', ' ').title())
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

def save_analysis_results(summary_df, filename='analysis_summary.csv'):
    """
    Save analysis results to CSV file.
    
    Parameters:
    -----------
    summary_df : pd.DataFrame
        Summary dataframe to save
    filename : str
        Output filename
    """
    filepath = f"../data/{filename}"
    summary_df.to_csv(filepath, index=False)
    print(f"Analysis results saved to {filepath}")

def print_analysis_summary(summary_df):
    """
    Print a formatted summary of analysis results.
    
    Parameters:
    -----------
    summary_df : pd.DataFrame
        Summary dataframe
    """
    print("=" * 60)
    print("NYC CONGESTION PRICING ANALYSIS SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal metrics analyzed: {len(summary_df)}")
    print(f"Analysis period: {summary_df.get('date', 'N/A')}")
    
    # Calculate summary statistics
    if 'change_pct' in summary_df.columns:
        avg_change = summary_df['change_pct'].mean()
        positive_changes = summary_df[summary_df['change_pct'] > 0]
        negative_changes = summary_df[summary_df['change_pct'] < 0]
        
        print(f"\nAverage change: {avg_change:+.2f}%")
        print(f"Positive changes: {len(positive_changes)} metrics")
        print(f"Negative changes: {len(negative_changes)} metrics")
        
        if len(positive_changes) > 0:
            print(f"\nTop improvements:")
            for _, row in positive_changes.nlargest(3, 'change_pct').iterrows():
                print(f"  ✓ {row['metric']}: {row['change_pct']:+.2f}%")
        
        if len(negative_changes) > 0:
            print(f"\nAreas of concern:")
            for _, row in negative_changes.nsmallest(3, 'change_pct').iterrows():
                print(f"  ✗ {row['metric']}: {row['change_pct']:+.2f}%")
    
    print("\n" + "=" * 60) 