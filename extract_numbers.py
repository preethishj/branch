#!/usr/bin/env python3
"""
Extract data from Apple Numbers files and convert to CSV
"""

import zipfile
import os
import csv
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_numbers_to_csv(numbers_file, output_csv):
    """Extract table data from Numbers file and save as CSV"""
    try:
        # Numbers files are actually ZIP archives
        with zipfile.ZipFile(numbers_file, 'r') as zip_ref:
            # Find the document.xml file which contains the data
            file_list = zip_ref.namelist()
            
            # Extract and parse the index file first
            try:
                index_xml = zip_ref.read('Index.xml').decode('utf-8')
            except:
                # Try alternate location
                try:
                    index_xml = zip_ref.read('index.xml').decode('utf-8')
                except:
                    print("Could not find index file")
                    return False
            
            # Parse and look for table references
            root = ET.fromstring(index_xml)
            
            # Try to find the main data file
            for file in file_list:
                if 'Data' in file and file.endswith('.xml'):
                    try:
                        data_content = zip_ref.read(file)
                        # Try to parse as XML
                        data_root = ET.fromstring(data_content)
                        
                        # Extract table data
                        rows_data = []
                        headers = None
                        
                        # Look for table elements
                        for table in data_root.iter():
                            # Look for row data
                            if 'row' in table.tag.lower() or 'cell' in table.tag.lower():
                                pass
                        
                        if rows_data or headers:
                            print(f"Found data structure in {file}")
                            
                    except Exception as e:
                        print(f"Could not parse {file}: {e}")
                        pass
        
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def try_alternative_extraction(numbers_file):
    """Try alternative methods to extract Numbers data"""
    try:
        import zipfile
        with zipfile.ZipFile(numbers_file, 'r') as zip_ref:
            # List all files in the archive
            print("Files in Numbers archive:")
            for file in sorted(zip_ref.namelist())[:20]:
                print(f"  - {file}")
                
                # Try to read smaller XML files
                if file.endswith('.xml') and 'Data' in file:
                    try:
                        content = zip_ref.read(file).decode('utf-8')
                        # Save for inspection
                        with open('/tmp/numbers_data.xml', 'w') as f:
                            f.write(content[:2000])
                        print(f"\nSample content from {file} saved to /tmp/numbers_data.xml")
                    except:
                        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    numbers_file = '/Users/preethish.janardhanan/Documents/tickets.csv.numbers'
    
    if os.path.exists(numbers_file):
        print(f"📦 Examining Numbers file structure...\n")
        try_alternative_extraction(numbers_file)
    else:
        print(f"❌ File not found: {numbers_file}")
