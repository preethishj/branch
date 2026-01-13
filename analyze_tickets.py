#!/usr/bin/env python3
"""
Zendesk Ticket Analysis Tool
Analyzes ticket data to identify trends and themes
"""

import pandas as pd
import os
import json
from collections import Counter
from pathlib import Path
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# NLTK data download
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class TicketAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.insights = {}
        
    def load_data(self):
        """Load data from CSV or Excel file"""
        try:
            if self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.numbers'):
                # Try using pandas to read Numbers format
                try:
                    self.df = pd.read_excel(self.file_path, engine='openpyxl')
                except:
                    print(f"Note: .numbers file detected. Attempting alternative method...")
                    # Numbers files are actually ZIP archives containing XML
                    return self.load_from_numbers_zip()
            
            if self.df is not None:
                print(f"✓ Loaded {len(self.df)} tickets")
                print(f"✓ Columns: {', '.join(self.df.columns.tolist())}\n")
                return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def load_from_numbers_zip(self):
        """Extract and parse Numbers file (ZIP format)"""
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            
            data = []
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                # List available files
                files = zip_ref.namelist()
                
                # Look for table data
                for file in files:
                    if 'table' in file.lower() or 'data' in file.lower():
                        try:
                            content = zip_ref.read(file).decode('utf-8', errors='ignore')
                            # Try to extract text content
                        except:
                            pass
            
            # Fallback: try using pandas with different approach
            print("Attempting to read Numbers file as Excel format...")
            self.df = pd.read_excel(self.file_path)
            return True
            
        except Exception as e:
            print(f"Could not parse Numbers file: {e}")
            return False
    
    def analyze_subjects(self):
        """Analyze ticket subjects for common themes"""
        if 'Subject' not in self.df.columns:
            # Try to find subject-like column
            subject_cols = [col for col in self.df.columns if 'subject' in col.lower()]
            if not subject_cols:
                print("⚠ No 'Subject' column found")
                return
            subject_col = subject_cols[0]
        else:
            subject_col = 'Subject'
        
        subjects = self.df[subject_col].dropna().astype(str).tolist()
        
        # Extract common words/phrases
        words = []
        for subject in subjects:
            # Remove common words
            cleaned = re.sub(r'\b(the|a|an|and|or|is|in|to|for|of|on|with|at|from)\b', 
                           '', subject, flags=re.IGNORECASE)
            words.extend(cleaned.split())
        
        # Filter meaningful words (length > 3)
        meaningful_words = [w.lower().strip('.,!?;:"') for w in words if len(w.strip('.,!?;:"')) > 3]
        
        self.insights['top_keywords'] = Counter(meaningful_words).most_common(15)
        
        # Identify themes using TF-IDF
        if len(subjects) > 2:
            vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
            try:
                tfidf_matrix = vectorizer.fit_transform(subjects)
                self.insights['tfidf_terms'] = vectorizer.get_feature_names_out().tolist()
            except:
                pass
    
    def analyze_sentiment(self):
        """Analyze sentiment of tickets"""
        if 'Subject' not in self.df.columns:
            subject_cols = [col for col in self.df.columns if 'subject' in col.lower()]
            if not subject_cols:
                return
            subject_col = subject_cols[0]
        else:
            subject_col = 'Subject'
        
        sentiments = []
        for subject in self.df[subject_col].dropna().astype(str):
            blob = TextBlob(subject)
            sentiments.append(blob.sentiment.polarity)
        
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        self.insights['avg_sentiment'] = avg_sentiment
        self.insights['sentiment_distribution'] = {
            'positive': sum(1 for s in sentiments if s > 0.1),
            'neutral': sum(1 for s in sentiments if -0.1 <= s <= 0.1),
            'negative': sum(1 for s in sentiments if s < -0.1)
        }
    
    def analyze_status(self):
        """Analyze ticket status distribution"""
        status_cols = [col for col in self.df.columns if 'status' in col.lower()]
        if status_cols:
            status_col = status_cols[0]
            self.insights['status_distribution'] = self.df[status_col].value_counts().to_dict()
    
    def analyze_priority(self):
        """Analyze ticket priority distribution"""
        priority_cols = [col for col in self.df.columns if 'priority' in col.lower()]
        if priority_cols:
            priority_col = priority_cols[0]
            self.insights['priority_distribution'] = self.df[priority_col].value_counts().to_dict()
    
    def analyze_dates(self):
        """Analyze temporal patterns"""
        date_cols = [col for col in self.df.columns if any(x in col.lower() for x in ['date', 'created', 'updated', 'time'])]
        if date_cols:
            date_col = date_cols[0]
            try:
                self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')
                month_dist = self.df[date_col].dt.to_period('M').value_counts().sort_index().to_dict()
                self.insights['monthly_distribution'] = {str(k): v for k, v in month_dist.items()}
            except:
                pass
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*70)
        print("ZENDESK TICKET ANALYSIS REPORT")
        print("="*70 + "\n")
        
        if self.insights.get('top_keywords'):
            print("📊 TOP KEYWORDS IN TICKET SUBJECTS:")
            print("-" * 50)
            for keyword, count in self.insights['top_keywords'][:10]:
                print(f"  • {keyword}: {count} mentions")
        
        if self.insights.get('tfidf_terms'):
            print("\n🎯 KEY THEMES IDENTIFIED:")
            print("-" * 50)
            for i, term in enumerate(self.insights['tfidf_terms'][:8], 1):
                print(f"  {i}. {term}")
        
        if self.insights.get('sentiment_distribution'):
            print("\n💭 SENTIMENT ANALYSIS:")
            print("-" * 50)
            dist = self.insights['sentiment_distribution']
            total = sum(dist.values())
            print(f"  • Positive: {dist.get('positive', 0)} ({dist.get('positive', 0)/total*100:.1f}%)")
            print(f"  • Neutral: {dist.get('neutral', 0)} ({dist.get('neutral', 0)/total*100:.1f}%)")
            print(f"  • Negative: {dist.get('negative', 0)} ({dist.get('negative', 0)/total*100:.1f}%)")
            print(f"  • Average Sentiment Score: {self.insights.get('avg_sentiment', 0):.2f}")
        
        if self.insights.get('status_distribution'):
            print("\n📋 TICKET STATUS DISTRIBUTION:")
            print("-" * 50)
            for status, count in sorted(self.insights['status_distribution'].items(), 
                                       key=lambda x: x[1], reverse=True):
                print(f"  • {status}: {count}")
        
        if self.insights.get('priority_distribution'):
            print("\n⚠️  TICKET PRIORITY DISTRIBUTION:")
            print("-" * 50)
            for priority, count in sorted(self.insights['priority_distribution'].items(),
                                         key=lambda x: x[1], reverse=True):
                print(f"  • {priority}: {count}")
        
        if self.insights.get('monthly_distribution'):
            print("\n📅 TICKETS BY MONTH:")
            print("-" * 50)
            for month in sorted(self.insights['monthly_distribution'].keys())[-6:]:
                count = self.insights['monthly_distribution'][month]
                print(f"  • {month}: {count}")
        
        print("\n" + "="*70 + "\n")
    
    def save_insights(self, output_file='ticket_insights.json'):
        """Save insights to JSON file"""
        # Convert sets and non-serializable objects to lists
        serializable_insights = {}
        for key, value in self.insights.items():
            if isinstance(value, list):
                serializable_insights[key] = value
            elif isinstance(value, dict):
                serializable_insights[key] = value
            else:
                serializable_insights[key] = str(value)
        
        output_path = os.path.join(os.path.dirname(self.file_path), output_file)
        with open(output_path, 'w') as f:
            json.dump(serializable_insights, f, indent=2)
        print(f"✓ Insights saved to {output_path}")

def main():
    # Find the tickets file
    documents_dir = Path('/Users/preethish.janardhanan/Documents')
    vs_code_dir = Path('/Users/preethish.janardhanan/Documents/VS Code')
    
    # Look for Q425 file first (newest), then CSV export, then any ticket files
    q425_files = list(documents_dir.glob('Q425*.csv')) + list(vs_code_dir.glob('Q425*.csv'))
    if q425_files:
        ticket_file = str(sorted(q425_files)[-1])  # Use most recent
    else:
        # Look for CSV export
        csv_export = documents_dir / 'tickets_export.csv'
        if csv_export.exists():
            ticket_file = str(csv_export)
        else:
            # Look for ticket files
            ticket_files = list(documents_dir.glob('tickets.*')) + list(vs_code_dir.glob('tickets.*'))
            
            if not ticket_files:
                print("❌ No tickets file found in Documents directory")
            return
        
        ticket_file = str(ticket_files[0])
    
    print(f"📂 Found ticket file: {ticket_file}\n")
    
    # Create analyzer
    analyzer = TicketAnalyzer(ticket_file)
    
    # Load and analyze
    if analyzer.load_data():
        analyzer.analyze_subjects()
        analyzer.analyze_sentiment()
        analyzer.analyze_status()
        analyzer.analyze_priority()
        analyzer.analyze_dates()
        analyzer.generate_report()
        analyzer.save_insights()
    else:
        print("❌ Failed to load ticket data")

if __name__ == '__main__':
    main()
