# Copilot Instructions - Zendesk Ticket Analysis

## Project Overview
This project performs **multi-faceted analysis of Zendesk support ticket data** to identify trends, themes, critical issues, and AI-driven insights. The codebase combines data processing, NLP analysis, and visualization to extract actionable intelligence from 1,910+ support tickets for the Branch.io platform.

**Core purpose**: Transform raw Zendesk exports into structured intelligence reports for stakeholder decision-making.

## Architecture & Data Flow

### Input Sources
- **Primary data**: `Weekly_Raw_Data.csv` (~1,910 tickets)
- **Alternative formats**: `tickets.csv.numbers` (Apple Numbers file), `tickets_export.csv`, `tickets.csv`
- **Data structure**: 30+ columns including Ticket ID, Subject, Organization, Severity, Sentiment, Escalation status, Resolution notes

### Processing Pipeline
```
CSV/Data Input → Text Preprocessing → NLP Analysis → Report Generation → Exports
    ↓              ↓                    ↓               ↓                  ↓
Zendesk exports  Clean & tokenize  Sentiment/Topics  Insights/CSV      CSV outputs
```

### Key Components

#### 1. `Zendesk_Ticket_Analysis.ipynb` (Main Notebook - 976 lines)
**Purpose**: Interactive Jupyter notebook for exploratory analysis and reporting
- **Sections 1-2**: Load and explore ticket data (~1,910 records, 30 columns)
- **Sections 3-4**: Data cleaning, deduplication, text preprocessing (lowercase, remove URLs/emails, tokenization)
- **Sections 5-8**: Sentiment analysis (TextBlob polarity scoring), LDA topic modeling (8 topics), TF-IDF keyword extraction
- **Sections 9-10**: Temporal trends, categorical analysis (Contact Reason, Severity, Service Tier)
- **Sections 11**: Critical issue deep-dives with root cause analysis
- **Output**: Visualizations, JSON insights export, `Top_10_Critical_Issues_Report.csv`

#### 2. `analyze_tickets.py` (Modular Analysis Tool - 274 lines)
**Purpose**: Standalone Python class for programmatic ticket analysis
- **TicketAnalyzer class**: 
  - `load_data()`: Support for CSV/Excel/Numbers files with fallback parsing
  - `analyze_subjects()`: Extract keywords via TF-IDF, identify themes
  - `analyze_sentiment()`: TextBlob-based sentiment classification
  - `analyze_status()`, `analyze_priority()`, `analyze_dates()`: Categorical breakdowns
  - `generate_report()`: Formatted terminal output
  - `save_insights()`: JSON serialization to `ticket_insights.json`
- **Design pattern**: Adapter pattern for multiple file formats

#### 3. `extract_numbers.py` (File Format Handler - 88 lines)
**Purpose**: Handle proprietary Apple Numbers file format
- Extracts ZIP-archived XML structure from `.numbers` files
- Fallback methods if standard parsing fails
- Diagnostic output to help troubleshoot data extraction

## Project-Specific Patterns & Conventions

### Data Processing Conventions
1. **Column name flexibility**: Code searches for columns by lowercase pattern matching
   - Example: `'status'` in `col.lower()` finds "Ticket status", "Custom status name", etc.
   - Reason: Zendesk exports vary; this makes code robust to schema changes

2. **Missing data handling**: Use `.fillna()` and `.dropna()` with context awareness
   - Subjects: Fill with 'No Subject' before removing; Summaries: Drop gracefully
   - Never silently ignore; log missing data percentage

3. **Sentiment classification**:
   - **Positive**: TextBlob polarity > 0.1
   - **Neutral**: -0.1 ≤ polarity ≤ 0.1
   - **Negative**: polarity < -0.1
   - This is threshold-based (not categorical); useful for trend analysis

4. **Risk scoring algorithm** (used in critical issue ranking):
   ```python
   risk_score = severity_value
   + 2 if "Very negative" in Sentiment else 0
   + 1 if "Negative" in Sentiment else 0
   + 1 if "Bad" satisfaction rating else 0
   ```
   This multi-factor scoring identifies compounded problems (negative sentiment + bad SAT + escalation).

### NLP Pipeline
1. **Text Preprocessing**: Lowercase → Remove URLs/emails → Remove special chars → Lemmatization with NLTK WordNetLemmatizer
2. **Topic Modeling**: LDA (Latent Dirichlet Allocation) with 8 topics hardcoded (determined empirically)
3. **Keyword Extraction**: TF-IDF with max_features=30, min_df=5 (filters low-frequency terms)
4. **Dependencies**: nltk, textblob, sklearn, pandas

### Output Conventions
- **Console output**: Uses emoji prefixes (🔴, 📊, 💭) for visual scanning
- **Reports**: CSV exports to `/Users/preethish.janardhanan/Documents/` with timestamp-friendly names
- **JSON structure**: Nested dict with lists (keywords) and dicts (distributions) for compatibility

## Critical Developer Workflows

### Running Analysis
```bash
# Execute Jupyter notebook
jupyter notebook /Users/preethish.janardhanan/Documents/Zendesk_Ticket_Analysis.ipynb

# Run Python analysis tool
python /Users/preethish.janardhanan/Documents/analyze_tickets.py
```

### Data Refresh Workflow
1. Export latest Zendesk tickets to CSV → Save as `Weekly_Raw_Data.csv`
2. Run `analyze_tickets.py` to generate summary insights
3. Open notebook and run all cells for detailed visualizations
4. Export critical issues table: `Top_10_Critical_Issues_Report.csv`

### Key Outputs to Monitor
- `ticket_insights.json`: Serialized keyword frequencies, sentiment distributions (used for dashboards)
- `Top_10_Critical_Issues_Report.csv`: Executive report with risk scores
- Notebook cell outputs: Visualizations and unstructured insights

## Integration Points & External Dependencies

### Data Source: Zendesk API
- Raw exports assumed to be manual CSV downloads (no live API integration currently)
- **Column assumptions** (from Weekly_Raw_Data.csv):
  - Ticket ID, Ticket subject, Issue / Request Summary (body text)
  - Requester email, Ticket organization name
  - Sentiment (pre-calculated), Escalated, Ticket satisfaction rating
  - Severity, Service Tier, P-Level, Urgency
  - Root Cause / Technical Finding, Resolution Steps Taken, Improvement Suggestions

### Dependencies
- **Data processing**: pandas, numpy
- **NLP**: nltk (punkt, stopwords, wordnet), textblob, sklearn (TfidfVectorizer, CountVectorizer, LDA)
- **Visualization**: matplotlib, seaborn
- **File handling**: zipfile, xml.etree (for Numbers format), openpyxl (fallback)

### Known Limitations
1. **Numbers format parsing**: Incomplete XML extraction; typically falls back to Excel read
2. **NLTK data downloads**: Code auto-downloads (~500KB) on first run; requires internet
3. **Hardcoded paths**: Analysis references `/Users/preethish.janardhanan/Documents/` paths directly
4. **Topic count**: LDA fixed to 8 topics; no dynamic optimization
5. **Older NLTK data**: Code warns if iOS SDK is outdated (hardcoded check in notebook)

## Patterns for Extending This Project

### Adding New Analysis Types
1. Create new method in `TicketAnalyzer` class (e.g., `analyze_resolution_time()`)
2. Follow signature: `def analyze_X(self):` → populate `self.insights[key_name]`
3. Add to `main()` call sequence
4. Update `generate_report()` to display findings

### Handling New CSV Columns
- Use lowercase pattern matching in `load_data()` or analysis methods
- Document assumptions in comments (e.g., "assumes 'sentiment' is pre-calculated")
- Test with stub data before deploying

### Modifying Visualization Style
- All matplotlib figures use `sns.set_style("whitegrid")` globally
- Color schemes: `{'positive': '#2ecc71', 'neutral': '#95a5a6', 'negative': '#e74c3c'}` (consistent green/gray/red)
- Preference: Horizontal bar charts for category comparisons; line plots for trends

## Tested Scenarios
- ✅ 1,910 ticket CSV with mixed data quality (10% missing values typical)
- ✅ Negative sentiment detection in ticket subjects (94/1,910 = ~5% negative)
- ✅ LDA topic modeling convergence with n_components=8
- ✅ Critical issue ranking by compound risk scoring
- ✅ Executive user identification (email pattern matching: "ceo", "founder", "vp", etc.)
- ❌ Apple Numbers file parsing (falls back to Excel method; XML extraction incomplete)

## Questions to Ask When Extending
1. **Data freshness**: Is CSV updated weekly? Should analysis run automatically?
2. **Threshold calibration**: Are sentiment cutoffs (-0.1, +0.1) correct for this org's communication style?
3. **Topic count**: Should 8 topics be dynamic based on corpus size?
4. **Escalation routes**: Are critical issues auto-routed, or just reported?
5. **Archiving**: When should old tickets be excluded from analysis?
