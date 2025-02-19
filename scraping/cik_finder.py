import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import pandas as pd

def lookup_cik(company_name):
    """Look up CIK using SEC's web form"""
    url = "https://www.sec.gov/cgi-bin/cik_lookup"
    headers = {
        "User-Agent": "Individual Investor (your.email@domain.com)",  # Replace with your email
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
    }
    
    # Form data
    data = {
        "company": company_name
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            # Parse the response HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for pre tags containing CIK links
            results = soup.find_all('pre')
            
            for result in results:
                # Find all links in the pre tag
                links = result.find_all('a')
                for link in links:
                    if 'CIK=' in link.get('href', ''):
                        cik = link.text.strip()
                        company = result.text.split(cik)[1].strip()
                        return cik, company
            
            return None, "No match found"
        else:
            return None, f"Error: Status code {response.status_code}"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

def process_companies(filename='scraping/cik/hedge_fund_names.txt'):
    """Process all companies with careful rate limiting"""
    
    # Load companies
    with open(filename, 'r') as f:
        companies = [line.strip() for line in f.readlines()]
    
    # Create DataFrame to store results
    results_df = pd.DataFrame(columns=['Hedge Fund Name', 'CIK'])
    
    print(f"Total companies to process: {len(companies)}")
    print("Starting lookups...")
    
    found_count = 0
    
    for i, company in enumerate(companies, 1):
        print(f"[{i}/{len(companies)}] Looking up: {company}")
        
        # Random delay between 3 and 5 seconds
        delay = random.uniform(3, 5)
        time.sleep(delay)
        
        cik, result = lookup_cik(company)
        
        if cik:
            found_count += 1
            print(f"Found CIK: {cik}")
            results_df.loc[len(results_df)] = [company, cik]
        else:
            print(f"No CIK found: {result}")
            results_df.loc[len(results_df)] = [company, 'NOT_FOUND']
        
        # Every 10 requests, take a longer break
        if i % 10 == 0:
            long_delay = random.uniform(10, 15)
            print(f"Taking a {long_delay:.1f} second break...")
            time.sleep(long_delay)
        
        # Save progress periodically
        if i % 5 == 0:
            results_df.to_csv('scraping/hedge_funds_with_ciks.csv', index=False)
            print("Progress saved")
    
    # Save final results
    results_df.to_csv('scraping/hedge_funds_with_ciks.csv', index=False)
    
    print("\nFinal Summary:")
    print(f"Total companies processed: {len(companies)}")
    print(f"CIKs found: {found_count}")
    print(f"Missing CIKs: {len(companies) - found_count}")
    print("Results saved to 'hedge_funds_with_ciks.csv'")

if __name__ == "__main__":
    print(f"Starting CIK lookup process at {datetime.now()}")
    process_companies('scraping/hedge_fund_names.txt')