# Operational Equity Framework - Assessment Tool

Professional assessment toolkit for evaluating health equity operational infrastructure.

---

## WHAT'S INCLUDED

### Core Components:

**1. Assessment Questions** (`assessment_questions.json`)
- 60 questions across 3 pillars (Process, People, Technology)
- Scoring rubrics for each question
- Rationale explaining why each question matters

**2. Scoring Algorithm** (`scoring_algorithm.py`)
- Automated score calculation
- Gap identification
- Recommendation generation
- Report formatting

**3. Framework Methodology** (`framework_methodology.md`)
- Theoretical foundation
- Evidence base from maternal mortality analysis
- Use cases and applications

**4. Sample Report** (`sample_assessment_report.md`)
- Example of complete assessment deliverable
- Shows depth and quality of analysis
- Template for client reports

---

## HOW TO USE

### Option 1: Run Automated Assessment (Python)

**For testing or generating sample reports:**
```bash
# Activate virtual environment
cd ~/Documents/equity-metrics-dashboard
source venv/bin/activate

# Run scoring algorithm with sample data
python3 framework/scoring_algorithm.py
```

**This generates:**
- Pillar-by-pillar scores
- Gap analysis
- Prioritized recommendations
- Overall assessment

---

### Option 2: Manual Assessment (Client Delivery)

**Step-by-step process for real client engagements:**

#### **PHASE 1: Pre-Assessment (1 hour)**
1. Review `assessment_questions.json` with client
2. Explain framework pillars
3. Schedule data collection period (1-2 weeks)
4. Provide question set for client completion

#### **PHASE 2: Data Collection (1-2 weeks)**
Client completes 60 questions via:
- Google Form (create from JSON)
- Excel spreadsheet
- Interview format (in-person or virtual)

#### **PHASE 3: Scoring & Analysis (2-3 hours)**
1. Input responses into scoring algorithm
2. Run gap analysis
3. Review results
4. Customize recommendations for client context
5. Generate professional report

#### **PHASE 4: Delivery (1 hour)**
1. Present findings in 1-hour debrief
2. Walk through pillar scores
3. Explain priority gaps
4. Discuss implementation roadmap
5. Answer questions

**Total Time Investment:** 4-6 hours per assessment

---

## PRICING STRUCTURE

### **Self-Assessment (Free)**
- 20-question abbreviated version
- Automated scoring
- Basic gap identification
- Lead generation tool

### **Comprehensive Assessment ($5,000-$15,000)**
- Full 60-question evaluation
- Manual review and contextual analysis
- 20-30 page detailed report
- Gap analysis with evidence
- Prioritized recommendations
- 1-hour debrief consultation

### **Implementation Support ($25,000-$75,000)**
- Everything in Comprehensive Assessment
- 6-month implementation guidance
- Monthly check-ins (6 sessions)
- Access to implementation toolkit
- Progress tracking and adjustment
- Re-assessment at 6 months

### **Annual License ($15,000-$50,000/year)**
- Ongoing subscription for large organizations
- Annual comprehensive assessments
- Quarterly advisory calls
- Continuous toolkit access
- Peer benchmarking data
- Priority support

---

## CUSTOMIZATION GUIDE

### Adding New Questions

**Edit `assessment_questions.json`:**
```json
{
  "id": "P21",
  "question": "Your new question text?",
  "type": "binary",
  "options": ["Yes", "No"],
  "scoring": {"Yes": 5, "No": 0},
  "rationale": "Why this matters for equity"
}
```

**Supported question types:**
- `binary`: Yes/No (0 or 5 points)
- `scale`: Multiple choice (0-5 points)
- `percentage`: Range-based (1-5 points)

---

### Modifying Scoring

**In `scoring_algorithm.py`, adjust:**
```python
# Change interpretation thresholds
def _interpret_score(self, percentage: float) -> str:
    if percentage <= 40:
        return "Critical gaps"
    elif percentage <= 60:
        return "Moderate gaps"
    # etc.
```

---

### Customizing Reports

**Use `sample_assessment_report.md` as template:**

1. Replace "Sample Health System" with client name
2. Update scores from algorithm output
3. Customize recommendations for client's context
4. Add client-specific data/context
5. Adjust implementation timeline for client resources

---

## SAMPLE OUTPUT

**When you run `scoring_algorithm.py`, you'll see:**
```
PROCESS:   40/100 (40.0%) - Critical gaps
PEOPLE:    34/100 (34.0%) - Critical gaps  
TECHNOLOGY: 21/100 (21.0%) - Critical gaps

OVERALL SCORE: 31.7%
INTERPRETATION: Critical gaps - High risk of poor equity outcomes

PRIORITY FOCUS AREA: TECHNOLOGY
Recommended Actions:
  1. Enable real-time outcome stratification by race/ethnicity in EHR
  2. Implement automated risk alerts for maternal health conditions
  [etc.]
```

---

##  FRAMEWORK EVIDENCE BASE

**Developed from analysis of:**
- **6,214 maternal deaths** (2018-2022, CDC WONDER Multiple Cause of Death data)
- **19.3 million births** (CDC WONDER Natality data)
- **5-year period** spanning pre-COVID baseline (2018-2019) and pandemic impact (2020-2022)
- **All 50 states** + District of Columbia
- **Racial/ethnic stratification** across 6 categories

**Key Evidence:**
- COVID-19 served as natural experiment: universal policy expansion with differential outcomes
- Disparities WIDENED during 2020-2021 despite emergency coverage expansion
- AIAN maternal mortality increased 192%, Black increased 86%, Hispanic increased 141%
- Demonstrated that policy coverage ≠ equitable outcomes without operational infrastructure

**Framework Status:**
- Currently validated through 2018-2022 analysis
- Designed for ongoing validation as 2023-2024 data becomes available (CDC release expected late 2025/early 2026)
- Assessment tool ready for organizational implementation
- Future validation will test whether infrastructure predicts policy effectiveness (Medicaid postpartum extension outcomes)

---

##  RELATED WORK

**Technical Analysis:**
- GitHub: [github.com/marshelton3/equity-metrics-dashboard](https://github.com/marshelton3/equity-metrics-dashboard)
- Maternal mortality analysis notebooks
- Reusable analytics toolkit

**Publications:**
- [Coming: AJPH paper on policy evaluation]
- [Coming: Health Affairs on implementation]
- [Coming: White paper on framework methodology]

---

##  FOR CLIENTS

**Interested in an assessment?**

**Contact:**
Marshawn Shelton, MPH, PMP, CCMP  
Founder, Isosalus  
Email: marshawn@isosalus.com  
Website: isosalus.com/services  
LinkedIn: linkedin.com/in/marshawnshelton

**What to expect:**
1. Initial consultation (30 min, free)
2. Scope discussion and pricing
3. Assessment completion (1-2 weeks)
4. Report delivery and debrief (1 hour)
5. Optional: Implementation support engagement

---

##  TECHNICAL REQUIREMENTS

**To run the scoring algorithm:**

**Python Version:** 3.8+

**Dependencies:**
```bash
# No external packages required!
# Uses only Python standard library:
# - json
# - typing
# - datetime
```

**Installation:**
```bash
# Clone repository
git clone https://github.com/marshelton3/equity-metrics-dashboard.git
cd equity-metrics-dashboard

# No pip install needed - uses standard library only!

# Run assessment
python3 framework/scoring_algorithm.py
```

---

##  VERSION HISTORY

**v1.0 (November 2025)**
- Initial framework release
- 60 questions across 3 pillars
- Automated scoring algorithm
- Sample assessment report
- Evidence base from 2018-2022 maternal mortality analysis

**v1.1 (Planned: Q1 2026)**
- Web-based self-assessment tool
- PDF report generation
- Implementation toolkit templates
- Extended white paper

**v2.0 (Planned: Q2 2026)**
- Validation with 10+ organizational assessments
- Benchmarking database
- Certification program framework
- Peer comparison capabilities

---

## LICENSE

**Framework Methodology:** Open for academic and educational use with attribution

**Assessment Tool:** Available for organizational self-assessment

**Commercial Use:** Contact Isosalus for licensing

**Attribution Required:**
```
Operational Equity Framework by Marshawn Shelton, MPH, PMP, CCMP
Isosalus | isosalus.com
```

---

## ACKNOWLEDGMENTS

This framework was developed through analysis of CDC WONDER data and builds on implementation science, health equity research, and operational excellence methodologies.

**Special thanks to:**
- Communities affected by maternal health disparities
- Health systems committed to operationalizing equity

---

**Last Updated:** November 12, 2025  
**Questions?** marshawn@isosalus.com