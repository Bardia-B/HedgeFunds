import pandas as pd
import time
import os
from tqdm import tqdm
from form13f_scraper import download_form13f_files, scrape_form13f_tables, get_fund_relationships
import shutil  # For deleting directories

def get_hedge_funds_data():
    """Read hedge funds and their CIKs from hedge_funds_with_ciks.csv"""
    try:
        df = pd.read_csv('scraping/hedge_funds_with_ciks.csv')
        # Filter out NOT_FOUND CIKs and create dictionary
        valid_funds = df[df['CIK'] != 'NOT_FOUND']
        return dict(zip(valid_funds['Hedge Fund Name'], valid_funds['CIK']))
    except FileNotFoundError:
        print("hedge_funds_with_ciks.csv not found")
        return {}

if __name__ == "__main__":
    print("Starting 13F Holdings Scraper")
    funds_data = get_hedge_funds_data()
    
    if not funds_data:
        print("No valid hedge funds found in hedge_funds_with_ciks.csv")
        exit(1)
    
    print(f"Found {len(funds_data)} hedge funds to process")
    base_output_dir = "filling"
    
    # Process each fund directly
    for fund_name, cik in funds_data.items():
        print(f"\nProcessing {fund_name} (CIK: {cik})")
        
        # Create directory for this fund
        fund_dir = os.path.join(base_output_dir, f"fund_{cik}")
        os.makedirs(fund_dir, exist_ok=True)
        
        try:
            # Download 13F files
            print(f"Downloading 13F filings...")
            download_form13f_files(cik, fund_dir)
            
            # Scrape tables from downloaded files
            print(f"Processing downloaded filings...")
            holdings_df = scrape_form13f_tables(fund_dir)
            
            if not holdings_df.empty:
                print(f"Found {len(holdings_df)} holdings")
                holdings_df['Fund Name'] = fund_name
                holdings_df['CIK'] = cik
                
                # Save to CSV
                output_path = os.path.join(fund_dir, 'form13f_holdings.csv')
                holdings_df.to_csv(output_path, index=False)
                print(f"Saved holdings to {output_path}")
            else:
                print(f"No holdings found for {fund_name}")
                
        except Exception as e:
            print(f"Error processing {fund_name}: {str(e)}")
            continue
    
    print("\nProcessing complete!")
    print(f"Total hedge funds processed: {len(funds_data)}")
    print(f"\nResults saved to:")
    print(f"Directory: {base_output_dir}") 