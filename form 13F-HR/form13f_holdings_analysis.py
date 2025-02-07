import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import numpy as np

def analyze_holdings_changes(cik, base_dir=None):
    """Analyze changes in holdings across multiple filings"""
    if base_dir is None:
        base_dir = f"filings_13f_{cik}"
        
    all_filings = []
    
    # Process each filing
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'form13fInfoTable.xml':
                filing_path = os.path.join(root, file)
                # Extract date from directory name (format: filing_0001291422-YY-NNNNNN)
                filing_dir = os.path.basename(os.path.dirname(filing_path))
                filing_date = filing_dir.split('-')[1]  # Get the year part
                if len(filing_date) == 2:
                    filing_date = f"20{filing_date}"  # Convert YY to YYYY
                
                try:
                    tree = ET.parse(filing_path)
                    root_elem = tree.getroot()
                    ns = {'ns1': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}
                    
                    for info_table in root_elem.findall('.//ns1:infoTable', ns):
                        try:
                            holding = {
                                'filing_date': filing_date,
                                'name': info_table.find('ns1:nameOfIssuer', ns).text,
                                'cusip': info_table.find('ns1:cusip', ns).text,
                                'value': int(info_table.find('ns1:value', ns).text),
                                'shares': int(info_table.find('.//ns1:sshPrnamt', ns).text),
                                'type': info_table.find('ns1:titleOfClass', ns).text,
                                'discretion': info_table.find('ns1:investmentDiscretion', ns).text
                            }
                            all_filings.append(holding)
                        except Exception as e:
                            print(f"Error processing holding in {filing_path}: {e}")
                            continue
                    
                except Exception as e:
                    print(f"Error processing {filing_path}: {e}")
                    continue
    
    if not all_filings:
        print("No holdings found")
        return None, None
    
    # Convert to DataFrame
    df = pd.DataFrame(all_filings)
    df['filing_date'] = pd.to_datetime(df['filing_date'], format='%Y')
    
    # Get latest and previous filing dates
    latest_date = df['filing_date'].max()
    prev_date = df['filing_date'].unique()[-2] if len(df['filing_date'].unique()) > 1 else None
    
    if prev_date is None:
        print("Only one filing found - cannot calculate changes")
        return None, None
    
    # Calculate position changes
    latest = df[df['filing_date'] == latest_date]
    previous = df[df['filing_date'] == prev_date]
    
    # Merge latest and previous holdings
    changes = pd.merge(
        latest[['name', 'cusip', 'value', 'shares', 'type']],
        previous[['name', 'cusip', 'value', 'shares']],
        on=['name', 'cusip'],
        how='outer',
        suffixes=('_current', '_prev')
    )
    
    # Calculate changes
    changes['value_change'] = changes['value_current'].fillna(0) - changes['value_prev'].fillna(0)
    changes['shares_change'] = changes['shares_current'].fillna(0) - changes['shares_prev'].fillna(0)
    changes['value_change_pct'] = (changes['value_change'] / changes['value_prev'].fillna(1) * 100).round(2)
    
    # Generate summary
    summary = {
        'latest_filing_date': latest_date.strftime('%Y-%m-%d'),
        'previous_filing_date': prev_date.strftime('%Y-%m-%d'),
        'total_positions': len(latest),
        'total_value': latest['value'].sum() / 1000,  # Convert to millions
        'new_positions': len(changes[changes['value_prev'].isna()]),
        'closed_positions': len(changes[changes['value_current'].isna()]),
        'increased_positions': len(changes[changes['shares_change'] > 0]),
        'decreased_positions': len(changes[changes['shares_change'] < 0]),
        'top_holdings': latest.nlargest(10, 'value')[['name', 'type', 'value', 'shares']],
        'biggest_increases': changes.nlargest(5, 'value_change')[
            ['name', 'type', 'value_change', 'value_change_pct']
        ],
        'biggest_decreases': changes.nsmallest(5, 'value_change')[
            ['name', 'type', 'value_change', 'value_change_pct']
        ]
    }
    
    return summary, changes

def print_holdings_summary(summary):
    """Print formatted holdings summary"""
    print(f"\n=== Holdings Summary as of {summary['latest_filing_date']} ===")
    print(f"Previous Filing Date: {summary['previous_filing_date']}")
    print(f"\nPortfolio Overview:")
    print(f"Total Positions: {summary['total_positions']:,}")
    print(f"Total Value: ${summary['total_value']:,.2f}M")
    
    print(f"\nPosition Changes:")
    print(f"New Positions: {summary['new_positions']}")
    print(f"Closed Positions: {summary['closed_positions']}")
    print(f"Increased Positions: {summary['increased_positions']}")
    print(f"Decreased Positions: {summary['decreased_positions']}")
    
    print(f"\nTop 10 Current Holdings:")
    print(summary['top_holdings'].to_string(index=False))
    
    print(f"\nBiggest Position Increases:")
    print(summary['biggest_increases'].to_string(index=False))
    
    print(f"\nBiggest Position Decreases:")
    print(summary['biggest_decreases'].to_string(index=False))

if __name__ == "__main__":
    cik = "0001291422"
    summary, changes = analyze_holdings_changes(cik)
    if summary:
        print(f"\n=== Holdings Summary as of {summary['latest_filing_date']} ===")
        print(f"Previous Filing Date: {summary['previous_filing_date']}")
        print(f"\nPortfolio Overview:")
        print(f"Total Positions: {summary['total_positions']:,}")
        print(f"Total Value: ${summary['total_value']:,.2f}M")
        
        print(f"\nPosition Changes:")
        print(f"New Positions: {summary['new_positions']}")
        print(f"Closed Positions: {summary['closed_positions']}")
        print(f"Increased Positions: {summary['increased_positions']}")
        print(f"Decreased Positions: {summary['decreased_positions']}")
        
        print(f"\nTop 10 Current Holdings:")
        print(summary['top_holdings'].to_string(index=False))
        
        print(f"\nBiggest Position Increases:")
        print(summary['biggest_increases'].to_string(index=False))
        
        print(f"\nBiggest Position Decreases:")
        print(summary['biggest_decreases'].to_string(index=False)) 