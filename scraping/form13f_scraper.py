import requests
import pandas as pd
from datetime import datetime
import os
import time
from bs4 import BeautifulSoup
import warnings
import xml.etree.ElementTree as ET
import re
import shutil

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
    
    # Ensure CIK is padded to 10 digits
    cik = str(cik).zfill(10)
    
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
            
            # Try all possible URL patterns
            url_patterns = [
                f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_clean}/xslForm13F_X02/form13fInfoTable.xml",
                f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_clean}/form13fInfoTable.xml",
                f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_clean}/infotable.xml",
                # Add primary document URL pattern
                f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_clean}/{filing['primaryDocument']}"
            ]
            
            success = False
            for url_pattern in url_patterns:
                try:
                    response = requests.get(url_pattern, headers=headers)
                    response.raise_for_status()
                    
                    # If this is the primary document, try to extract the XML URL
                    if url_pattern.endswith(filing['primaryDocument']):
                        soup = BeautifulSoup(response.content, 'html.parser')
                        for doc in soup.find_all('document'):
                            if doc.type and 'XML' in str(doc.type):
                                xml_file = doc.find('filename')
                                if xml_file:
                                    xml_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_clean}/{xml_file.text}"
                                    try:
                                        response = requests.get(xml_url, headers=headers)
                                        response.raise_for_status()
                                        break
                                    except:
                                        continue
                    
                    # Save the successful response
                    with open(f"{filing_dir}/form13fInfoTable.xml", 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    print(f"Downloaded filing {filing['accessionNumber']}")
                    success = True
                    break
                    
                except requests.exceptions.RequestException:
                    continue
            
            if not success:
                print(f"Error downloading filing {filing['accessionNumber']}: Could not find valid URL")
            
            time.sleep(0.1)  # Respect SEC rate limits
                
    except Exception as e:
        print(f"Error fetching filings list: {str(e)}")

def scrape_form13f_tables(directory):
    """Scrape Form 13F tables from downloaded XML files"""
    all_holdings = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    
                    # Get filing accession number from file path
                    accession_number = os.path.basename(os.path.dirname(file_path))
                    
                    # Find all informationTable entries
                    namespace = {'ns': 'http://www.sec.gov/edgar/document/thirteenf/informationtable'}
                    
                    for entry in root.findall('.//ns:infoTable', namespace):
                        holding = {
                            'NAME OF ISSUER': entry.find('.//ns:nameOfIssuer', namespace).text.strip(),
                            'TITLE OF CLASS': entry.find('.//ns:titleOfClass', namespace).text.strip(),
                            'CUSIP': entry.find('.//ns:cusip', namespace).text.strip(),
                            'VALUE (x$1000)': float(entry.find('.//ns:value', namespace).text.strip()),
                            'SHRS OR PRN AMT': float(entry.find('.//ns:sshPrnamt', namespace).text.strip()),
                            'SH/PRN': entry.find('.//ns:sshPrnamtType', namespace).text.strip(),
                            'PUT/CALL': entry.find('.//ns:putCall', namespace).text.strip() if entry.find('.//ns:putCall', namespace) is not None else '',
                            'INVESTMENT DISCRETION': entry.find('.//ns:investmentDiscretion', namespace).text.strip(),
                            'OTHER MANAGER': entry.find('.//ns:otherManager', namespace).text.strip() if entry.find('.//ns:otherManager', namespace) is not None else '',
                            'VOTING AUTHORITY SOLE': int(entry.find('.//ns:votingAuthority/ns:Sole', namespace).text.strip()),
                            'VOTING AUTHORITY SHARED': int(entry.find('.//ns:votingAuthority/ns:Shared', namespace).text.strip()),
                            'VOTING AUTHORITY NONE': int(entry.find('.//ns:votingAuthority/ns:None', namespace).text.strip()),
                            'Filing Number': accession_number  # Changed from 'Filing Date'
                        }
                        all_holdings.append(holding)
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    continue
    
    if all_holdings:
        df = pd.DataFrame(all_holdings)
        
        # Ensure all columns are present even if empty
        required_columns = [
            'NAME OF ISSUER', 'TITLE OF CLASS', 'CUSIP', 'VALUE (x$1000)', 
            'SHRS OR PRN AMT', 'SH/PRN', 'PUT/CALL', 'INVESTMENT DISCRETION',
            'OTHER MANAGER', 'VOTING AUTHORITY SOLE', 'VOTING AUTHORITY SHARED',
            'VOTING AUTHORITY NONE', 'Filing Number'
        ]
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Reorder columns
        df = df[required_columns]
        
        # Save to CSV in the fund's directory
        csv_path = os.path.join(directory, 'form13f_holdings.csv')
        df.to_csv(csv_path, index=False)
        return df
    else:
        return pd.DataFrame()

def get_fund_relationships(ciks):
    """Get fund relationships from SEC data"""
    relationships = {}
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        for cik in ciks:
            # Ensure CIK is padded to 10 digits
            padded_cik = str(cik).zfill(10)
            url = f"https://data.sec.gov/submissions/CIK{padded_cik}.json"
            
            print(f"Fetching data for CIK: {cik}")  # Debug print
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"Error fetching CIK {cik}: Status {response.status_code}")
                continue
                
            data = response.json()
            
            # Get company name and add to relationships
            company_name = data.get('name', '')
            relationships[cik] = {
                'name': company_name,
                'related_ciks': {cik}  # Start with self as related
            }
            
            time.sleep(0.1)  # Respect SEC rate limits
            
    except Exception as e:
        print(f"Error in get_fund_relationships: {e}")
    
    return relationships

def organize_files_by_parent(base_dir):
    """Reorganize files by parent company"""
    relationships = get_fund_relationships()
    
    for parent_cik, info in relationships.items():
        parent_name = info['name'].replace(' ', '_')
        parent_dir = os.path.join(base_dir, parent_name)
        os.makedirs(parent_dir, exist_ok=True)
        
        # Move all related CIK folders
        for related_cik in info['related_ciks']:
            old_path = os.path.join(base_dir, f"fund_{related_cik}")
            new_path = os.path.join(parent_dir, f"cik_{related_cik}")
            
            if os.path.exists(old_path):
                shutil.move(old_path, new_path)

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