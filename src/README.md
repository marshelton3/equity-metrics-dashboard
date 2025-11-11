# Isosalus Maternal Mortality Analysis Toolkit

Reusable Python module for analyzing maternal mortality disparities using CDC WONDER data.

## Installation
```python
import sys
sys.path.append('/path/to/equity-metrics-dashboard')
from src.analysis import *
```

## Functions

### Data Loading

**`load_maternal_data(filepath, na_values=None)`**
- Load CDC WONDER maternal mortality data
- Handles suppression codes automatically
- Returns cleaned DataFrame

**`load_birth_data(filepath, na_values=None)`**
- Load CDC WONDER natality data
- Returns cleaned DataFrame with birth counts

### Data Processing

**`create_race_ethnicity(row)`**
- Standardizes race/ethnicity from CDC categories
- Hispanic ethnicity takes precedence
- Returns: 'AIAN (NH)', 'Black (NH)', 'White (NH)', etc.

**`calculate_mmr(deaths_df, births_df, group_by=['race_ethnicity'])`**
- Calculate maternal mortality rates per 100K births
- Can group by any variable(s): race, year, state, etc.
- Returns DataFrame with Deaths, Births, MMR

**`create_disparity_ratios(mmr_df, baseline_group='White (NH)', group_column='race_ethnicity')`**
- Calculate disparity ratios vs baseline
- Returns DataFrame with Disparity_Ratio column

### Visualization

**`visualize_disparities(mmr_df, group_column='race_ethnicity', output_path=None, figsize=(12,6))`**
- Horizontal bar chart of MMR by group
- Color-coded by severity
- Optional save to file

**`visualize_temporal_trends(mmr_df, group_column='race_ethnicity', time_column='Year', output_path=None, figsize=(14,8))`**
- Line chart showing trends over time
- Multiple groups on same chart
- Optional save to file

## Quick Start Example
```python
from src.analysis import *

# Load data
mortality = load_maternal_data('data/raw/maternal_mortality_national.txt')
births = load_birth_data('data/raw/births_national.txt')

# Standardize race/ethnicity
mortality['race_ethnicity'] = mortality.apply(create_race_ethnicity, axis=1)
births['race_ethnicity'] = births.apply(create_race_ethnicity, axis=1)

# Calculate rates
rates = calculate_mmr(mortality, births, group_by=['race_ethnicity'])

# Calculate disparities
rates_with_disparities = create_disparity_ratios(rates)

# Visualize
visualize_disparities(rates_with_disparities, output_path='outputs/disparities.png')
```

## Advanced Usage

### Temporal Analysis
```python
# Calculate rates by year and race
temporal_rates = calculate_mmr(
    mortality, 
    births, 
    group_by=['Year', 'race_ethnicity']
)

# Visualize trends
visualize_temporal_trends(
    temporal_rates,
    output_path='outputs/temporal_trends.png'
)
```

### State-Level Analysis
```python
# Calculate rates by state
state_rates = calculate_mmr(
    mortality,
    births,
    group_by=['State', 'race_ethnicity']
)

# Top 10 worst states
top_10 = state_rates.nlargest(10, 'MMR')
visualize_disparities(
    top_10,
    group_column='State',
    output_path='outputs/top_10_states.png'
)
```

## Author

Marshawn Shelton, MPH, PMP, CCMP  
Founder, Isosalus - Operationalizing Health Equity

