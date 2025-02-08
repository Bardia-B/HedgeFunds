import pandas as pd
import time
import os
from tqdm import tqdm
from form13f_scraper import download_form13f_files, scrape_form13f_tables
import shutil  # For deleting directories

def get_ciks_from_file():
    """Read CIKs from cik_numbers.txt"""
    try:
        with open('cik_numbers.txt', 'r') as f:
            ciks = [line.strip() for line in f if line.strip()]
        return ciks
    except FileNotFoundError:
        print("cik_numbers.txt not found")
        return []

def get_downloads_path():
    """Get the user's Downloads folder path"""
    return os.path.join(os.path.expanduser('~'), 'Downloads')

if __name__ == "__main__":
    print("Starting 13F Holdings Scraper")
    ciks = get_ciks_from_file()
    
    if not ciks:
        print("No CIKs found in cik_numbers.txt")
        exit(1)
    
    print(f"Found {len(ciks)} CIKs to process")
    downloads_path = get_downloads_path()
    
    all_holdings = []
    for cik in tqdm(ciks, desc="Processing CIKs"):
        try:
            print(f"\nProcessing CIK: {cik}")
            
            # Create directory in Downloads folder
            base_dir = os.path.join(downloads_path, f"filings_13f_{cik}")
            
            # First download the files
            download_form13f_files(cik, base_dir)
            
            # Then scrape the data
            holdings_df = scrape_form13f_tables(base_dir)
            
            if not holdings_df.empty:
                # Add CIK column to identify the source
                holdings_df['CIK'] = cik
                all_holdings.append(holdings_df)
                print(f"Successfully processed {len(holdings_df)} holdings for CIK {cik}")
            else:
                print(f"No holdings found for CIK {cik}, skipping...")
                # Remove empty directory
                if os.path.exists(base_dir):
                    shutil.rmtree(base_dir)
                continue
            
            time.sleep(1)  # Respect rate limits
            
        except Exception as e:
            print(f"Error processing CIK {cik}: {str(e)}")
            # Clean up directory if there was an error
            if os.path.exists(base_dir):
                shutil.rmtree(base_dir)
            continue
    
    # Only proceed if we found any holdings
    if all_holdings:
        final_df = pd.concat(all_holdings, ignore_index=True)
        
        # Only save if we have actual data
        if not final_df.empty:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            csv_path = os.path.join(downloads_path, f'all_13f_holdings_{timestamp}.csv')
            excel_path = os.path.join(downloads_path, f'all_13f_holdings_{timestamp}.xlsx')
            
            # Save to CSV
            final_df.to_csv(csv_path, index=False)
            
            # Save to Excel with formatting
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                final_df.to_excel(writer, index=False, sheet_name='13F Holdings')
                worksheet = writer.sheets['13F Holdings']
                
                # Format column widths
                for idx, col in enumerate(final_df.columns):
                    max_length = max(
                        final_df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
                
                # Format numeric columns
                numeric_cols = ['VALUE (x$1000)', 'SHRS OR PRN AMT', 
                              'VOTING AUTHORITY SOLE', 'VOTING AUTHORITY SHARED', 
                              'VOTING AUTHORITY NONE']
                
                for row in range(2, len(final_df) + 2):
                    for col, col_name in enumerate(final_df.columns, 1):
                        if col_name in numeric_cols:
                            worksheet.cell(row=row, column=col).number_format = '#,##0'
            
            print("\nProcessing complete!")
            print(f"Total holdings processed: {len(final_df)}")
            print(f"\nResults saved to:")
            print(f"CSV: {csv_path}")
            print(f"Excel: {excel_path}")
            
            # Display sample of the data
            print("\nSample of combined holdings:")
            print(final_df.head())
        else:
            print("\nNo valid holdings found in any filings")
    else:
        print("\nNo holdings were found for any CIK") 