# AI Prompt for Zendesk Ticket Analysis

## Purpose
Use this prompt with an AI assistant (like Claude, ChatGPT, or GitHub Copilot) to generate the same comprehensive Zendesk ticket analysis results as `analyze_tickets.py` produces.

---

## Prompt to Share with Your Peer

```
I need to analyze a Zendesk ticket dataset to identify trends, themes, and actionable intelligence.

**Dataset Details:**
- CSV file with 570 support tickets from January 13, 2026
- 32 columns including: Ticket ID, Ticket subject, Issue/Request Summary, Sentiment, Severity, 
  P-Level, Escalated, Ticket satisfaction rating, Features, Root Cause, Improvement Suggestions, 
  Organization, Service Tier, etc.
- Data is ~96.8% complete with good coverage of subject lines for NLP analysis

**Analysis Tasks:**

1. **Sentiment Analysis**
   - Use TextBlob to classify ticket subjects as positive (polarity > 0.1), negative (< -0.1), or neutral
   - Generate distribution: positive %, neutral %, negative %
   - Calculate average sentiment score (-1 to +1 scale)
   - Expected output: ~83% neutral, ~10% negative, ~7% positive

2. **Keyword Extraction (TF-IDF)**
   - Extract top 20-30 most important keywords from ticket subjects
   - Use TF-IDF vectorization with:
     - max_features: 30
     - min_df: 5
     - English stopwords removal
   - Expected top keywords: "branch" (85.79), "link" (52.17), "app" (39.62), "issue" (36.29), "data" (34.22)
   - Create horizontal bar chart visualization

3. **Topic Modeling (LDA)**
   - Use Latent Dirichlet Allocation with:
     - 8 topics (empirically determined)
     - CountVectorizer: max_features=50, min_df=5
     - Random state=42
   - For each topic: identify top 5 terms and ticket distribution
   - Expected: Topic 1 has ~23.1% (121 tickets), Topic 2 has ~6.7%, etc.
   - Assign dominant topic to each ticket and calculate confidence

4. **Critical Issues Identification**
   - Identify and rank tickets with:
     - Negative or very negative intent
     - Escalated status
     - Bad satisfaction ratings
     - Emergency/Critical severity levels
   - Risk scoring: Severity (1-5 pts) + Sentiment bonuses (0-2 pts) + Satisfaction penalties (0-1 pt)
   - Export top 10 critical issues to CSV with columns: Rank, Ticket ID, Organization, Subject, 
     Summary, Severity, Sentiment, Risk Score

5. **Data Quality Checks**
   - Count tickets with subjects
   - Remove duplicates based on subject
   - Report missing values per column (%)
   - Validate data completeness

6. **Visualization Output**
   - Sentiment distribution (pie chart + bar chart)
   - TF-IDF keyword importance (horizontal bar chart)
   - Topic distribution (pie chart + bar chart + average confidence)
   - Sentiment by topic (stacked bar chart)

7. **Summary Report**
   - Executive summary with total tickets, unique issues, time period
   - Sentiment breakdown percentages
   - Top 3 dominant topics and their keywords
   - Actionable recommendations (e.g., "Allocate resources to top 3 topics accounting for X% of tickets")
   - Key patterns and emerging issues

**Libraries to Use:**
- Data: pandas, numpy
- NLP: nltk (tokenization, lemmatization, stopwords), textblob (sentiment)
- ML: scikit-learn (TF-IDF, LDA CountVectorizer, LatentDirichletAllocation)
- Visualization: matplotlib, seaborn
- Preprocessing: regex, text cleaning

**Output Format:**
- Console output with emoji indicators (✓, 🔴, 📊, 💭, etc.) for readability
- JSON file (`ticket_insights.json`) with: top_keywords, sentiment_distribution, tfidf_terms, 
  average_sentiment
- CSV file (`Top_10_Critical_Issues_Report.csv`) with critical issues ranking
- Multiple matplotlib visualizations (4+ charts)

**Text Preprocessing Pipeline:**
1. Lowercase conversion
2. Remove URLs and email addresses
3. Remove special characters (keep spaces)
4. Tokenization
5. Lemmatization using WordNetLemmatizer
6. Remove stopwords (NLTK English stopwords)
7. Remove tokens shorter than 3 characters

**Auto-Detection Logic:**
- Script should auto-detect Q425*.csv files in Documents and VS Code directories
- Use most recent file by name if multiple versions exist
- Fall back to generic ticket files if Q425 files not found
- Support CSV, Excel, and Numbers file formats

**Success Criteria:**
- ✅ Analyze 570 tickets successfully
- ✅ Generate 83% neutral, 10.1% negative, 6.9% positive sentiment
- ✅ Identify 8 topics with proper distribution
- ✅ Extract meaningful keywords related to domain (branch, link, app, etc.)
- ✅ Identify critical issues requiring urgent attention
- ✅ Create exportable results for stakeholder review
- ✅ Generate 4+ visualizations
- ✅ Complete in < 2 minutes execution time
```

---

## How to Use This Prompt

1. **Copy the prompt above** into your preferred AI assistant (Claude, ChatGPT, GitHub Copilot, etc.)
2. **Provide the CSV file location** to the AI when asked
3. **Request Python script output** - ask for a complete, runnable Python script
4. **Run the generated script** with: `python analyze_tickets.py`
5. **Verify outputs** match the expected results listed above

---

## Expected Outputs After Running

Your peer should receive:
- ✅ `ticket_insights.json` - Structured data export (1.1KB)
- ✅ `Top_10_Critical_Issues_Report.csv` - Ranked critical issues (2.1KB)
- ✅ Console output with sentiment analysis, keywords, and topics
- ✅ Multiple visualizations displayed during execution
- ✅ Complete execution in ~60-90 seconds

---

## Quick Reference: Key Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| TF-IDF max_features | 30 | Captures top keywords without noise |
| TF-IDF min_df | 5 | Filters out rare terms |
| LDA n_topics | 8 | Empirically determined optimal clusters |
| LDA max_iter | 10 | Fast convergence for support ticket domain |
| Sentiment threshold (positive) | > 0.1 | Distinguishes satisfied from neutral |
| Sentiment threshold (negative) | < -0.1 | Captures frustration signals |
| Risk score weights | Sev(1-5) + Sent(0-2) + Sat(0-1) | Balanced multi-factor ranking |

---

## Tips for Your Peer

1. **Use a virtual environment** to avoid dependency conflicts
2. **Install all libraries first**: `pip install pandas numpy nltk textblob scikit-learn matplotlib seaborn`
3. **Download NLTK data**: Script handles this, but ensure internet access
4. **Place CSV file** in `/Users/preethish.janardhanan/Documents/` for auto-detection
5. **Check file format**: CSV expected; Excel/Numbers files also supported
6. **Review the generated CSV** for executive summary before sharing with stakeholders

---

## Customization Notes

Your peer can modify:
- **Number of topics**: Change `num_topics = 8` to any value (experiment with 5-12)
- **Visualization style**: Modify color schemes in matplotlib calls
- **Risk scoring weights**: Adjust multipliers in the risk score calculation
- **Output filename**: Change `ticket_insights.json` to preferred name
- **Sentiment thresholds**: Adjust polarity cutoffs (> 0.1, < -0.1) based on domain

---

## Support Questions

If your peer encounters issues:
- **Missing columns?** Verify CSV has expected column names (lowercase pattern matching handles variations)
- **Slow execution?** Reduce max_features or increase min_df threshold
- **No visualizations?** Ensure matplotlib backend is properly configured
- **JSON export errors?** Check file write permissions to project directory

---

**Generated:** 13 January 2026  
**Compatible with:** Python 3.7+, works with any Zendesk ticket export CSV
