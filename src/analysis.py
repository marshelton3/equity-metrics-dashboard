"""
Isosalus Maternal Mortality Analysis Toolkit

This module provides reusable functions for analyzing maternal mortality
disparities using CDC WONDER data.

Author: Marshawn Shelton, MPH, PMP, CCMP
Institution: Isosalus
Date: November 2025
Project: Operational Equity Framework - Maternal Health Analysis

Functions:
    load_maternal_data: Load and clean CDC WONDER mortality data
    load_birth_data: Load and clean CDC WONDER natality data
    create_race_ethnicity: Standardize race/ethnicity categories
    calculate_mmr: Calculate maternal mortality rates
    create_disparity_ratios: Calculate disparity ratios vs baseline
    aggregate_by_geography: Aggregate data by state/region
    visualize_disparities: Create disparity visualizations
    visualize_temporal_trends: Create temporal trend visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set visualization defaults
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_maternal_data(
    filepath: str,
    na_values: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Load and clean CDC WONDER maternal mortality data.
    
    This function loads tab-separated CDC WONDER data files and handles
    CDC-specific data suppression codes (e.g., "Suppressed", "Unreliable").
    
    Parameters
    ----------
    filepath : str
        Path to the CDC WONDER maternal mortality data file (.txt or .tsv)
    na_values : list of str, optional
        Additional values to treat as NA. Default includes CDC suppression codes.
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with maternal mortality data
        
    Examples
    --------
    >>> mortality = load_maternal_data('data/raw/maternal_mortality_national.txt')
    >>> print(f"Loaded {len(mortality)} rows")
    
    Notes
    -----
    CDC WONDER suppresses counts <10 for privacy. These appear as "Suppressed" 
    or "Unreliable" in the data and are converted to NaN.
    """
    if na_values is None:
        na_values = ['Suppressed', 'Unreliable', 'Not Applicable', 'Missing']
    
    try:
        df = pd.read_csv(
            filepath,
            sep='\t',
            na_values=na_values,
            low_memory=False
        )
        
        # Convert numeric columns
        numeric_cols = ['Deaths', 'Population', 'Crude Rate']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert Year to numeric
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        
        print(f" Loaded {len(df):,} rows of maternal mortality data")
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error loading maternal mortality data: {str(e)}")
    
def load_birth_data(
    filepath: str,
    na_values: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Load and clean CDC WONDER natality (birth) data.
    
    Parameters
    ----------
    filepath : str
        Path to the CDC WONDER natality data file (.txt or .tsv)
    na_values : list of str, optional
        Additional values to treat as NA. Default includes CDC suppression codes.
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with birth data
        
    Examples
    --------
    >>> births = load_birth_data('data/raw/births_national.txt')
    >>> print(f"Loaded {births['Births'].sum():,.0f} total births")
    """
    if na_values is None:
        na_values = ['Suppressed', 'Unreliable', 'Not Applicable', 'Missing']
    
    try:
        df = pd.read_csv(
            filepath,
            sep='\t',
            na_values=na_values,
            low_memory=False
        )
        
        # Convert numeric columns
        if 'Births' in df.columns:
            df['Births'] = pd.to_numeric(df['Births'], errors='coerce')
        
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        
        print(f" Loaded {len(df):,} rows of birth data")
        print(f"   Total births: {df['Births'].sum():,.0f}")
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error loading birth data: {str(e)}")
    
def create_race_ethnicity(row: pd.Series) -> str:
    """
    Standardize race/ethnicity categories from CDC WONDER data.
    
    CDC WONDER uses separate "Hispanic Origin" and "Race" fields. This function
    combines them into standard categories following CDC/OMB guidelines:
    Hispanic ethnicity takes precedence over race.
    
    Parameters
    ----------
    row : pd.Series
        Row from CDC WONDER dataframe containing 'Hispanic Origin' and 'Race' columns
        
    Returns
    -------
    str
        Standardized race/ethnicity category:
        - 'Hispanic or Latino' (any race)
        - 'Black (NH)' (Non-Hispanic Black)
        - 'White (NH)' (Non-Hispanic White)
        - 'Asian/PI (NH)' (Non-Hispanic Asian or Pacific Islander)
        - 'AIAN (NH)' (Non-Hispanic American Indian/Alaska Native)
        - 'Multiracial (NH)' (Non-Hispanic, more than one race)
        - 'Other/Unknown'
        
    Examples
    --------
    >>> df['race_ethnicity'] = df.apply(create_race_ethnicity, axis=1)
    >>> print(df['race_ethnicity'].value_counts())
    
    Notes
    -----
    - NH = Non-Hispanic
    - Hispanic ethnicity takes precedence (regardless of race)
    - Combines Native Hawaiian/Pacific Islander with Asian per small sample sizes
    """
    hispanic = str(row.get('Hispanic Origin', ''))
    race = str(row.get('Race', ''))
    
    # Hispanic (any race) takes precedence
    if 'Hispanic' in hispanic and 'Not' not in hispanic:
        return 'Hispanic or Latino'
    
    # Non-Hispanic categories
    if 'Black' in race:
        return 'Black (NH)'
    elif 'White' in race:
        return 'White (NH)'
    elif 'Asian' in race:
        return 'Asian/PI (NH)'
    elif 'Indian' in race or 'Alaska' in race:
        return 'AIAN (NH)'
    elif 'Hawaiian' in race or 'Pacific' in race:
        return 'Asian/PI (NH)'
    elif 'More than one' in race:
        return 'Multiracial (NH)'
    else:
        return 'Other/Unknown'

def calculate_mmr(
    deaths_df: pd.DataFrame,
    births_df: pd.DataFrame,
    group_by: List[str] = ['race_ethnicity']
) -> pd.DataFrame:
    """
    Calculate maternal mortality rates (MMR) per 100,000 live births.
    
    Merges death and birth data, then calculates rates. Can aggregate by
    any combination of variables (race/ethnicity, year, state, etc.)
    
    Parameters
    ----------
    deaths_df : pd.DataFrame
        Dataframe with maternal deaths, must have 'Deaths' column
    births_df : pd.DataFrame
        Dataframe with births, must have 'Births' column
    group_by : list of str, default ['race_ethnicity']
        Column(s) to group by for rate calculation
        
    Returns
    -------
    pd.DataFrame
        Dataframe with deaths, births, and MMR by specified groups
        Columns: [group_by columns], Deaths, Births, MMR
        
    Examples
    --------
    >>> # Calculate overall rates by race/ethnicity
    >>> rates = calculate_mmr(mortality, births, group_by=['race_ethnicity'])
    
    >>> # Calculate rates by year and race/ethnicity
    >>> temporal_rates = calculate_mmr(
    ...     mortality, births, 
    ...     group_by=['Year', 'race_ethnicity']
    ... )
    
    >>> # Calculate rates by state
    >>> state_rates = calculate_mmr(
    ...     mortality, births,
    ...     group_by=['State', 'race_ethnicity']
    ... )
    
    Notes
    -----
    MMR = (Maternal Deaths / Live Births) × 100,000
    
    CDC considers rates based on <20 deaths as potentially unreliable.
    This function does not suppress these, but they should be interpreted
    with caution.
    """
    # Aggregate deaths
    deaths_agg = deaths_df.groupby(group_by).agg({
        'Deaths': 'sum'
    }).reset_index()
    
    # Aggregate births
    births_agg = births_df.groupby(group_by).agg({
        'Births': 'sum'
    }).reset_index()
    
    # Merge
    merged = deaths_agg.merge(births_agg, on=group_by, how='inner')
    
    # Calculate MMR (per 100,000 births)
    merged['MMR'] = (merged['Deaths'] / merged['Births']) * 100000
    
    # Sort by MMR descending
    merged = merged.sort_values('MMR', ascending=False).reset_index(drop=True)
    
    print(f" Calculated MMR for {len(merged)} groups")
    print(f"   Total deaths: {merged['Deaths'].sum():,.0f}")
    print(f"   Total births: {merged['Births'].sum():,.0f}")
    
    return merged

def create_disparity_ratios(
    mmr_df: pd.DataFrame,
    baseline_group: str = 'White (NH)',
    group_column: str = 'race_ethnicity'
) -> pd.DataFrame:
    """
    Calculate disparity ratios comparing each group to a baseline.
    
    Parameters
    ----------
    mmr_df : pd.DataFrame
        Dataframe with MMR calculations, must have 'MMR' column
    baseline_group : str, default 'White (NH)'
        The reference group for disparity calculations
    group_column : str, default 'race_ethnicity'
        Column name containing the grouping variable
        
    Returns
    -------
    pd.DataFrame
        Original dataframe with added 'Disparity_Ratio' column
        Ratio = Group MMR / Baseline MMR
        
    Examples
    --------
    >>> rates = calculate_mmr(mortality, births)
    >>> rates_with_disparities = create_disparity_ratios(rates)
    >>> print(rates_with_disparities[['race_ethnicity', 'MMR', 'Disparity_Ratio']])
    
    >>> # Use different baseline
    >>> rates_vs_national = create_disparity_ratios(
    ...     state_rates,
    ...     baseline_group='National Average',
    ...     group_column='State'
    ... )
    
    Notes
    -----
    Disparity Ratio = (Group Rate / Baseline Rate)
    - Ratio > 1: Higher risk than baseline
    - Ratio < 1: Lower risk than baseline
    - Ratio = 1: Same risk as baseline
    
    Example: Disparity ratio of 2.6 means group has 2.6x the baseline rate
    """
    df = mmr_df.copy()
    
    # Get baseline MMR
    baseline_mmr = df[df[group_column] == baseline_group]['MMR'].values
    
    if len(baseline_mmr) == 0:
        raise ValueError(f"Baseline group '{baseline_group}' not found in data")
    
    baseline_mmr = baseline_mmr[0]
    
    # Calculate disparity ratios
    df['Disparity_Ratio'] = df['MMR'] / baseline_mmr
    
    print(f" Calculated disparity ratios vs {baseline_group} (MMR: {baseline_mmr:.1f})")
    print(f"\nDisparity Summary:")
    for _, row in df.iterrows():
        if row[group_column] != baseline_group:
            ratio = row['Disparity_Ratio']
            direction = "higher" if ratio > 1 else "lower"
            print(f"   {row[group_column]:30} {ratio:.2f}x ({abs(ratio-1)*100:.0f}% {direction})")
    
    return df

def visualize_disparities(
    mmr_df: pd.DataFrame,
    group_column: str = 'race_ethnicity',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> None:
    """
    Create horizontal bar chart showing maternal mortality rates by group.
    
    Parameters
    ----------
    mmr_df : pd.DataFrame
        Dataframe with MMR data
    group_column : str, default 'race_ethnicity'
        Column to use for grouping
    output_path : str, optional
        If provided, save figure to this path
    figsize : tuple, default (12, 6)
        Figure size in inches (width, height)
        
    Examples
    --------
    >>> rates = calculate_mmr(mortality, births)
    >>> visualize_disparities(rates, output_path='outputs/disparities.png')
    
    >>> # Visualize state disparities
    >>> state_rates = calculate_mmr(mortality, births, group_by=['State'])
    >>> visualize_disparities(
    ...     state_rates.head(10),
    ...     group_column='State',
    ...     output_path='outputs/top_10_states.png'
    ... )
    """
    # Sort by MMR
    df = mmr_df.sort_values('MMR', ascending=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create color map (red for highest, blue for lowest)
    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(df)))
    
    # Create horizontal bar chart
    bars = ax.barh(df[group_column], df['MMR'], color=colors, alpha=0.8)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, df['MMR'])):
        ax.text(val + 1, i, f'{val:.1f}', va='center', fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Maternal Mortality Rate (per 100,000 births)', 
                  fontsize=12, fontweight='bold')
    ax.set_ylabel(group_column.replace('_', ' ').title(), 
                  fontsize=12, fontweight='bold')
    ax.set_title('Maternal Mortality Rates by Group', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f" Saved visualization to {output_path}")
    
    plt.show()

def visualize_temporal_trends(
    mmr_df: pd.DataFrame,
    group_column: str = 'race_ethnicity',
    time_column: str = 'Year',
    output_path: Optional[str] = None,
    figsize: Tuple[int, int] = (14, 8)
) -> None:
    """
    Create line chart showing maternal mortality trends over time by group.
    
    Parameters
    ----------
    mmr_df : pd.DataFrame
        Dataframe with MMR data including time dimension
    group_column : str, default 'race_ethnicity'
        Column to use for grouping lines
    time_column : str, default 'Year'
        Column containing time variable
    output_path : str, optional
        If provided, save figure to this path
    figsize : tuple, default (14, 8)
        Figure size in inches (width, height)
        
    Examples
    --------
    >>> # Calculate rates by year and race
    >>> temporal_rates = calculate_mmr(
    ...     mortality, births,
    ...     group_by=['Year', 'race_ethnicity']
    ... )
    >>> visualize_temporal_trends(
    ...     temporal_rates,
    ...     output_path='outputs/temporal_trends.png'
    ... )
    
    Notes
    -----
    Useful for identifying trends, peaks, and differential impacts over time.
    COVID-19 impact visible as 2020-2021 changes.
    """
    # Pivot data for plotting
    pivot_df = mmr_df.pivot(index=time_column, columns=group_column, values='MMR')
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Define colors for consistency
    color_map = {
        'AIAN (NH)': '#d62728',
        'Black (NH)': '#ff7f0e',
        'Hispanic or Latino': '#2ca02c',
        'White (NH)': '#1f77b4',
        'Asian/PI (NH)': '#9467bd',
        'Multiracial (NH)': '#8c564b'
    }
    
    # Plot each group
    for col in pivot_df.columns:
        if col != 'Other/Unknown':
            color = color_map.get(col, 'gray')
            ax.plot(pivot_df.index, pivot_df[col],
                   marker='o', linewidth=2.5, markersize=8,
                   label=col, color=color)
    
    # Formatting
    ax.set_xlabel(time_column, fontsize=13, fontweight='bold')
    ax.set_ylabel('Maternal Mortality Rate\n(per 100,000 live births)',
                 fontsize=13, fontweight='bold')
    ax.set_title('Maternal Mortality Rates Over Time',
                fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Save if path provided
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f" Saved visualization to {output_path}")
    
    plt.show()

    