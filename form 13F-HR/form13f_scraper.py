import requests
import pandas as pd
from datetime import datetime
import os
import time
from bs4 import BeautifulSoup
import warnings
import xml.etree.ElementTree as ET
import re

def process_form13f_filings(cik, start_date=None, end_date=None):
    """Process Form 13F filings for a given CIK"""
    base_dir = f"filings_13f_{cik}"
    os.makedirs(base_dir, exist_ok=True)
    
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": "YourCompany yourname@email.com"  # Replace with your details
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        recent_filings = pd.DataFrame(data['filings']['recent'])
        
        # Convert filingDate to datetime
        recent_filings['filingDate'] = pd.to_datetime(recent_filings['filingDate'])
        
        # Filter for last 7 years
        seven_years_ago = pd.Timestamp.now() - pd.DateOffset(years=7)
        recent_filings = recent_filings[recent_filings['filingDate'] >= seven_years_ago]
        
        # Filter for Form 13F-HR
        filtered_filings = recent_filings[recent_filings['form'].str.contains('13F-HR', na=False)]
        
        # Save filing metadata
        filtered_filings.to_csv(f"{base_dir}/form13f_metadata.csv", index=False)
        
        all_holdings = []
        
        for _, filing in filtered_filings.iterrows():
            print(f"\nProcessing Form 13F from {filing['filingDate'].strftime('%Y-%m-%d')}")
            
            filing_dir = f"{base_dir}/filing_{filing['accessionNumber']}"
            os.makedirs(filing_dir, exist_ok=True)
            
            # Get the information table XML
            acc_no_clean = filing['accessionNumber'].replace('-', '')
            info_table_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_clean}/xslForm13F_X02/form13fInfoTable.xml"
            
            try:
                response = requests.get(info_table_url, headers=headers)
                response.raise_for_status()
                
                # Save raw XML
                with open(f"{filing_dir}/form13fInfoTable.xml", 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Parse XML content
                root = ET.fromstring(response.text)
                
                # Process each infoTable entry
                for info_table in root.findall('.//infoTable'):
                    holding = {
                        'NAME OF ISSUER': info_table.find('nameOfIssuer').text.strip(),
                        'TITLE OF CLASS': info_table.find('titleOfClass').text.strip(),
                        'CUSIP': info_table.find('cusip').text.strip(),
                        'VALUE (x$1000)': info_table.find('value').text.strip(),
                        'SHRS OR PRN AMT': info_table.find('sshPrnamt').text.strip(),
                        'SH/PRN': info_table.find('sshPrnamtType').text.strip(),
                        'PUT/CALL': info_table.find('putCall').text.strip() if info_table.find('putCall') is not None else '',
                        'INVESTMENT DISCRETION': info_table.find('investmentDiscretion').text.strip(),
                        'OTHER MANAGER': info_table.find('otherManager').text.strip() if info_table.find('otherManager') is not None else '',
                        'VOTING AUTHORITY SOLE': info_table.find('votingAuthority').find('Sole').text.strip(),
                        'VOTING AUTHORITY SHARED': info_table.find('votingAuthority').find('Shared').text.strip(),
                        'VOTING AUTHORITY NONE': info_table.find('votingAuthority').find('None').text.strip(),
                        'Filing Date': filing['filingDate'].strftime('%Y-%m-%d')
                    }
                    all_holdings.append(holding)
                
                print(f"Processed {len(all_holdings)} holdings from filing {filing['accessionNumber']}")
                time.sleep(0.1)  # Respect SEC rate limits
                
            except Exception as e:
                print(f"Error processing filing {filing['accessionNumber']}: {e}")
                continue
        
        # Create DataFrame and save to CSV/Excel
        if all_holdings:
            df = pd.DataFrame(all_holdings)
            
            # Convert numeric columns
            numeric_columns = ['VALUE (x$1000)', 'SHRS OR PRN AMT', 'VOTING AUTHORITY SOLE', 
                             'VOTING AUTHORITY SHARED', 'VOTING AUTHORITY NONE']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Format the DataFrame
            df = df.sort_values(['Filing Date', 'NAME OF ISSUER'])
            
            # Save to CSV and Excel
            csv_path = os.path.join(base_dir, 'all_13f_holdings.csv')
            excel_path = os.path.join(base_dir, 'all_13f_holdings.xlsx')
            
            df.to_csv(csv_path, index=False)
            
            # Save to Excel with proper formatting
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='13F Holdings')
                worksheet = writer.sheets['13F Holdings']
                
                # Adjust column widths
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            print(f"\nProcessed total of {len(df)} holdings")
            print(f"Data saved to:\n{csv_path}\n{excel_path}")
            
            return df
        
    except Exception as e:
        print(f"Error processing filings: {e}")
        return None

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def download_form13f_files(cik, base_dir):
    """Download Form 13F files"""
    os.makedirs(base_dir, exist_ok=True)
    
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": "YourCompany yourname@email.com"  # Replace with your details
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        recent_filings = pd.DataFrame(data['filings']['recent'])
        
        # Filter for Form 13F-HR
        filtered_filings = recent_filings[recent_filings['form'].str.contains('13F-HR', na=False)]
        
        for _, filing in filtered_filings.iterrows():
            acc_no_clean = filing['accessionNumber'].replace('-', '')
            filing_dir = f"{base_dir}/filing_{filing['accessionNumber']}"
            os.makedirs(filing_dir, exist_ok=True)
            
            # Download XML
            info_table_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_clean}/form13fInfoTable.xml"
            try:
                response = requests.get(info_table_url, headers=headers)
                response.raise_for_status()
                
                # Save as XML
                with open(f"{filing_dir}/form13fInfoTable.xml", 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"Downloaded filing {filing['accessionNumber']}")
                time.sleep(0.1)  # Respect SEC rate limits
                
            except Exception as e:
                print(f"Error downloading filing {filing['accessionNumber']}: {e}")
                continue
                
    except Exception as e:
        print(f"Error fetching filings list: {e}")

def scrape_form13f_tables(base_dir):
    """Scrape Form 13F data from XML files"""
    all_holdings = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'form13fInfoTable.xml':
                filing_path = os.path.join(root, file)
                print(f"Processing {filing_path}")
                
                try:
                    # Get filing date from directory path
                    filing_dir = os.path.basename(os.path.dirname(filing_path))
                    filing_date = filing_dir.split('_')[1] if '_' in filing_dir else ''
                    
                    # Parse XML
                    tree = ET.parse(filing_path)
                    root_elem = tree.getroot()
                    
                    # Define namespace
                    ns = {'ns1': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}
                    
                    # Find all infoTable elements
                    for info_table in root_elem.findall('.//ns1:infoTable', ns):
                        try:
                            holding = {
                                'NAME OF ISSUER': clean_text(info_table.find('ns1:nameOfIssuer', ns).text),
                                'TITLE OF CLASS': clean_text(info_table.find('ns1:titleOfClass', ns).text),
                                'CUSIP': clean_text(info_table.find('ns1:cusip', ns).text),
                                'VALUE (x$1000)': clean_text(info_table.find('ns1:value', ns).text),
                                'SHRS OR PRN AMT': clean_text(info_table.find('.//ns1:sshPrnamt', ns).text),
                                'SH/PRN': clean_text(info_table.find('.//ns1:sshPrnamtType', ns).text),
                                'PUT/CALL': clean_text(info_table.find('ns1:putCall', ns).text if info_table.find('ns1:putCall', ns) is not None else ''),
                                'INVESTMENT DISCRETION': clean_text(info_table.find('ns1:investmentDiscretion', ns).text),
                                'OTHER MANAGER': clean_text(info_table.find('ns1:otherManager', ns).text if info_table.find('ns1:otherManager', ns) is not None else ''),
                                'VOTING AUTHORITY SOLE': clean_text(info_table.find('.//ns1:votingAuthority/ns1:Sole', ns).text),
                                'VOTING AUTHORITY SHARED': clean_text(info_table.find('.//ns1:votingAuthority/ns1:Shared', ns).text),
                                'VOTING AUTHORITY NONE': clean_text(info_table.find('.//ns1:votingAuthority/ns1:None', ns).text),
                                'Filing Date': filing_date
                            }
                            all_holdings.append(holding)
                        except Exception as e:
                            print(f"Error processing holding in {filing_path}: {str(e)}")
                            continue
                    
                    print(f"Found {len(all_holdings)} holdings in {filing_path}")
                        
                except Exception as e:
                    print(f"Error processing {filing_path}: {str(e)}")
                    continue
    
    # Create DataFrame and format it
    if all_holdings:
        df = pd.DataFrame(all_holdings)
        
        # Convert numeric columns
        numeric_columns = [
            'VALUE (x$1000)', 
            'SHRS OR PRN AMT', 
            'VOTING AUTHORITY SOLE',
            'VOTING AUTHORITY SHARED', 
            'VOTING AUTHORITY NONE'
        ]
        
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Format the DataFrame
        df = df.sort_values(['Filing Date', 'NAME OF ISSUER'])
        
        # Save to CSV and Excel
        csv_path = os.path.join(base_dir, 'form13f_holdings.csv')
        excel_path = os.path.join(base_dir, 'form13f_holdings.xlsx')
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Form 13F Holdings')
            worksheet = writer.sheets['Form 13F Holdings']
            
            # Format column widths
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            # Format numeric columns
            for row in range(2, len(df) + 2):
                worksheet.cell(row=row, column=4).number_format = '#,##0'  # VALUE column
                worksheet.cell(row=row, column=5).number_format = '#,##0'  # SHRS OR PRN AMT column
                for col in range(10, 13):  # VOTING AUTHORITY columns
                    worksheet.cell(row=row, column=col).number_format = '#,##0'
        
        df.to_csv(csv_path, index=False)
        
        print(f"\nProcessed {len(df)} total holdings")
        print(f"Data saved to:\n{csv_path}\n{excel_path}")
        
        return df
    else:
        print("No holdings found")
        return pd.DataFrame()

if __name__ == "__main__":
    cik = "0001291422"  # Replace with your CIK
    base_dir = f"filings_13f_{cik}"
    
    # First download the files
    download_form13f_files(cik, base_dir)
    
    # Then scrape the data
    try:
        holdings_df = scrape_form13f_tables(base_dir)
        if not holdings_df.empty:
            print("\nSample of extracted data:")
            print(holdings_df.head())
    except Exception as e:
        print(f"Error running script: {str(e)}") 