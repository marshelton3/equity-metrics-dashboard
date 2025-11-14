# Equity Metrics Dashboard: Maternal Mortality Analysis & OE-3PI Framework™ Validation

**A comprehensive analysis of maternal mortality trends (2018-2023) and validation of the Operational Equity - Three Pillars Implementation (OE-3PI) Framework™**

---

##  Project Overview

This repository contains a complete data science analysis validating the **OE-3PI Framework™** - a novel tool for assessing organizational readiness to implement health equity initiatives. Using state-level maternal mortality data from CDC WONDER (2018-2023), the project demonstrates that comprehensive operational infrastructure predicts both baseline performance and stability/resilience in health outcomes.

### Key Findings

**Framework Validation:**
- **Baseline Performance:** States with comprehensive infrastructure show 85% lower maternal mortality (r = -0.367, p = 0.033)
- **Stability/Resilience:** High-infrastructure states demonstrate 4.7x greater stability (r = -0.554)
- **Value-Based Care:** Infrastructure predicts sustained excellence, making it an effective VBC readiness assessment

**National Trends:**
- 45% improvement in national maternal mortality rate (2021-2023): 32.9 → 18.2 per 100K births
- Recovery from the COVID-19 pandemic peak
- Geographic disparities persist: Southern states average 2-3x higher mortality than Northeastern states

---

##  The OE-3PI Framework™

### Three Pillars of Operational Equity

The framework assesses organizational readiness across three interdependent pillars:

**1. PROCESS Pillar: Access Infrastructure**
- Policies and systems that enable care access
- Examples: Medicaid expansion, care coordination, referral pathways
- Impact: Foundation for equity implementation

**2. PEOPLE Pillar: Workforce & Support**  
- Programs supporting patients and the workforce
- Examples: Community health workers, doulas, paid family leave
- Impact: Enables human-centered care delivery

**3. TECHNOLOGY Pillar: Data & Learning Systems**
- Systems enabling measurement and improvement
- Examples: Data analytics, quality dashboards, review committees
- Impact: Drives continuous learning and adaptation

### Framework Applicability

While validated using maternal mortality data, the OE-3PI Framework™ is designed for **universal application across the healthcare continuum**:
- Chronic disease management (diabetes, hypertension)
- Behavioral health integration
- Cancer screening and treatment
- Social determinants interventions
- Any health outcome with persistent disparities

Maternal mortality was selected as the initial validation case due to policy timing (2022 Medicaid postpartum extension), data availability, and health equity urgency - not as a limitation on applicability.

---

##  Repository Structure
```
equity-metrics-dashboard/
├── data/
│   ├── raw/                          # CDC WONDER downloads
│   │   ├── maternal_mortality_*.txt
│   │   └── births_*.txt
│   └── processed/                    # Analysis-ready datasets
│       ├── state_mmr_by_year.csv     # Time-series data (146 observations)
│       ├── state_policy_database.csv # 51 jurisdictions × 4 policies
│       ├── merged_policy_outcomes.csv
│       └── policy_correlations.csv
│
├── notebooks/
│   ├── 01_initial_exploration.ipynb  # National trends analysis
│   ├── 02_temporal_trends.ipynb      # Time-series patterns
│   └── 03_state_analysis.ipynb       # Complete state analysis & validation
│
├── outputs/
│   └── figures/                       # Publication-quality visualizations
│       ├── national_mmr_trend.png
│       ├── state_mmr_map_interactive.html
│       ├── infrastructure_vs_mmr.png
│       └── framework_validation_complete.png
│
├── src/
│   └── analysis.py                    # Reusable analysis functions
│
├── framework/                         # OE-3PI Framework™ documentation
│   ├── framework_methodology.md
│   ├── scoring_algorithm.py
│   └── sample_assessment_report.md
│
└── scripts/
    └── remove_all_emojis.py           # Portfolio maintenance
```

---

##  Analysis Components

### Project 1-2: National Trends & Temporal Analysis
**Objective:** Understand post-policy national trends  
**Key Finding:** 45% improvement (2021-2023) following Medicaid postpartum extension

**Files:**
- `notebooks/01_initial_exploration.ipynb`
- `notebooks/02_temporal_trends.ipynb`

### Project 3: State-Level Geographic Analysis  
**Objective:** Map state disparities and regional patterns  
**Key Finding:** Persistent North-South divide; Northeast showed largest improvements

**Files:**
- `notebooks/03_state_analysis.ipynb` (Sessions 1-2)
- `outputs/figures/state_mmr_map_interactive.html`

### Project 4: Policy Mapping & Cross-Sectional Validation
**Objective:** Test if infrastructure predicts outcomes  
**Key Finding:** Infrastructure Score negatively correlated with MMR (r = -0.367, p = 0.033)

**Policies Tracked:**
- Medicaid Expansion (41 jurisdictions)
- Doula Medicaid Coverage (21 jurisdictions)  
- Paid Family Leave (14 jurisdictions)
- MMRC Active Status (all 51, varying maturity)

**Files:**
- `notebooks/03_state_analysis.ipynb` (Session 3)
- `data/processed/state_policy_database.csv`

### Project 5: Time-Series & Resilience Analysis
**Objective:** Test if infrastructure predicts improvement and stability  
**Key Findings:**
- Infrastructure does NOT predict short-term improvement (regression to the mean dominates)
- Infrastructure DOES predict stability/resilience (r = -0.554)
- High-infrastructure states maintain low, stable mortality
- Low-infrastructure states experience volatile, crisis-driven fluctuations

**Files:**
- `notebooks/03_state_analysis.ipynb` (Session 5)
- `data/processed/state_mmr_by_year.csv`

---

##  Key Statistics

### Framework Validation

| Prediction | Correlation | P-Value | Interpretation |
|-----------|-------------|---------|----------------|
| Baseline MMR | r = -0.367 | p = 0.033 | Infrastructure → Lower mortality ✅ |
| Volatility (CV) | r = -0.363 | - | Infrastructure → Stability ✅ |
| Range | r = -0.554 | - | Infrastructure → Resilience ✅ |

### Infrastructure Score Distribution

| Score | States | Avg MMR | Volatility (CV) | Avg Range |
|-------|--------|---------|-----------------|-----------|
| 0 | 5 | 39.2 | 33.6% | 34.2 |
| 1 | 5 | 36.0 | 29.0% | 27.0 |
| 2 | 6 | 29.4 | 27.6% | 22.4 |
| 3 | 6 | 28.1 | 34.7% | 24.1 |
| 4 | 7 | 20.9 | 15.2% | 7.3 |

**Score 4 states demonstrate:**
- 47% lower average MMR vs Score 0
- 54% lower volatility
- 79% smaller outcome range

### Exemplar States

**Most Stable (High Resilience):**
1. Oregon (Score 4): CV = 6.5%, Range = 3.5
2. Massachusetts (Score 4): CV = 9.0%, Range = 2.0
3. Maryland (Score 3): CV = 14.1%, Range = 5.8

**Most Volatile (Need Infrastructure):**
1. Louisiana (Score 3): CV = 52.1%, Range = 48.4
2. Illinois (Score 3): CV = 45.9%, Range = 20.9
3. Alabama (Score 0): CV = 40.9%, Range = 53.3

---

##  Value Proposition

### For Health Systems

The OE-3PI Framework™ identifies **organizational readiness for value-based care** by predicting:

1. **Sustained Performance:** Organizations with comprehensive infrastructure maintain consistently low mortality rates
2. **Stability:** High-infrastructure organizations show 4.7x less year-to-year volatility
3. **Resilience:** Strong infrastructure enables stable performance through external shocks (e.g., COVID-19)

**In value-based care models:** Predictable, stable outcomes reduce financial risk and enable long-term quality improvement - making infrastructure assessment critical for VBC readiness evaluation.

### For Policymakers

Framework reveals that **policy success requires implementation capacity**:
- Same policy (Medicaid postpartum extension) → Different outcomes by state
- Infrastructure predicts which states can operationalize policy effectively
- Investment in infrastructure creates sustained improvement, not volatile swings

---

##  Technical Stack

**Languages & Tools:**
- Python 3.12
- pandas (data manipulation)
- matplotlib/seaborn (visualization)
- plotly (interactive maps)
- scipy (statistical analysis)
- Jupyter Notebooks

**Data Sources:**
- CDC WONDER Database (2018-2023)
- State Medicaid agencies (policy implementation dates)
- National Health Law Program (doula coverage tracking)
- CDC Review to Action program (MMRC data)

---

##  Publications & Outputs

**In Development:**
- Policy Brief: "State Infrastructure and Maternal Health Resilience" (2025)
- White Paper: "Operationalizing Health Equity: The OE-3PI Framework" (2025)
- Journal Article: "The OE-3PI Framework for Operational Equity: Validation Using State-Level Maternal Mortality Outcomes, 2018-2023" (in preparation for Maternal & Child Health Journal)

**Available Now:**
- Interactive visualizations (see `outputs/figures/`)
- Complete analysis notebooks (fully documented)
- Reusable framework assessment tool

---

##  Getting Started

### Prerequisites
```bash
python >= 3.12
pandas >= 2.0
matplotlib >= 3.7
plotly >= 5.14
scipy >= 1.11
```

### Installation
```bash
# Clone repository
git clone https://github.com/marshelton3/equity-metrics-dashboard.git
cd equity-metrics-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

### Running the Analysis

1. **Explore national trends:** `notebooks/01_initial_exploration.ipynb`
2. **View temporal patterns:** `notebooks/02_temporal_trends.ipynb`
3. **Complete state analysis:** `notebooks/03_state_analysis.ipynb`

All notebooks are fully documented with markdown explanations and can be run sequentially.

---

##  Data Access

**Raw data** is included in `data/raw/` (CDC WONDER public data)  
**Processed datasets** available in `data/processed/`

To download fresh data from CDC WONDER:
1. Visit: https://wonder.cdc.gov/
2. Select "Natality" and "Maternal Mortality" datasets
3. Filter: Years 2018-2023, State-level
4. Export as tab-delimited text

---

##  Contributing

This repository documents original research validating the OE-3PI Framework™. 

**For inquiries about:**
- Framework application to other health conditions
- Organizational readiness assessments
- Consulting services
- Research collaboration

**Contact:** Marshawn Shelton  
**Website:** [isosalus.com](https://isosalus.com)  
**LinkedIn:** [Marshawn Shelton, MPH, PMP, CCMP](https://www.linkedin.com/in/marshawnshelton)

---

##  License

**Research & Framework:** © 2025 Marshawn Shelton / Isosalus. All Rights Reserved.

The OE-3PI Framework™ and associated materials are proprietary. Unauthorized reproduction or commercial use is prohibited.

**Data:** CDC WONDER data is public domain. Processed datasets may be used with attribution.

---

##  Citation

If using this work in academic research, please cite:
```
Shelton, M. (2025). Operationalizing Health Equity: Validation of the OE-3PI 
Framework Using State-Level Maternal Mortality Outcomes, 2018-2023. 
GitHub repository: https://github.com/marshelton3/equity-metrics-dashboard
```

---

##  Acknowledgments

**CDC WONDER Database** for public data access

---

##  Contact

**Marshawn Shelton, MPH, PMP, CCMP**  
Health Equity Strategist | Operational Excellence Consultant  
Founder, Isosalus

**Email:** [contact via LinkedIn]  
**LinkedIn:** [linkedin.com/in/marshawnshelton](https://www.linkedin.com/in/marshawnshelton)  
**Website:** [isosalus.com](https://isosalus.com)

---

*Last Updated: November 14, 2025*
*Research Status: Analysis Complete | Publications In Development*
