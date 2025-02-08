from secedgar.cik_lookup import CIKLookup
import time
from tqdm import tqdm

def normalize_company_name(name):
    """Normalize company names for better matching"""
    replacements = {
        ' LLC': '',
        ' L.L.C.': '',
        ' LP': '',
        ' L.P.': '',
        ' INC': '',
        ' INCORPORATED': '',
        ' CORP': '',
        ' CORPORATION': '',
        ' LTD': '',
        ' LIMITED': '',
        '&': 'AND',
        '.': '',
        ',': '',
    }
    
    name = name.upper()
    for old, new in replacements.items():
        name = name.replace(old, new)
    return name.strip()

def try_sec_api_endpoints(company_name):
    """Try multiple SEC API endpoints to find CIK"""
    
    headers = {
        'User-Agent': 'Individual Investor name@email.com',  # Replace with your details
        'Accept': 'application/json'
    }
    
    # First endpoint: company_tickers.json
    try:
        time.sleep(0.1)  # Rate limiting
        url1 = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(url1, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            company_name_lower = company_name.lower()
            
            for entry in data.values():
                if company_name_lower in entry['title'].lower():
                    return str(entry['cik_str']).zfill(10)
        
        # Second endpoint: CIK-lookup-data.txt
        time.sleep(0.1)  # Rate limiting
        url2 = "https://data.sec.gov/submissions/CIK-lookup-data.txt"
        response = requests.get(url2, headers=headers)
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            company_name_lower = company_name.lower()
            
            for line in lines:
                if line.strip():
                    fields = line.split('\t')
                    if len(fields) >= 2 and company_name_lower in fields[1].lower():
                        return fields[0].zfill(10)
        
        return 'NOT_FOUND'
        
    except Exception as e:
        print(f"Error searching for {company_name}: {str(e)}")
        return 'NOT_FOUND'

def load_existing_results():
    """Load existing results from file"""
    existing_results = {}
    try:
        with open('hedge_funds_with_ciks.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    fund, cik = parts
                    if cik != 'NOT_FOUND':
                        existing_results[fund] = cik
    except FileNotFoundError:
        pass
    return existing_results

def lookup_ciks(companies):
    """Look up CIKs using secedgar"""
    try:
        lookup = CIKLookup(companies, 
                          user_agent="Individual Investor name@email.com")  # Replace with your email
        return lookup.lookup_dict
    except Exception as e:
        print(f"Error during lookup: {str(e)}")
        return {}

def process_hedge_funds():
    # Load existing results
    existing_results = load_existing_results()
    print(f"Loaded {len(existing_results)} existing CIKs")
    
    # Read hedge fund names
    with open('hedge_fund_names.txt', 'r') as f:
        hedge_funds = [line.strip() for line in f.readlines()]
    
    # Process in small batches
    batch_size = 5
    results = []
    found_count = 0
    
    print("Looking up CIKs...")
    for i in tqdm(range(0, len(hedge_funds), batch_size)):
        batch = hedge_funds[i:i + batch_size]
        
        # Filter out ones we already have
        new_lookups = [fund for fund in batch if fund not in existing_results]
        
        if new_lookups:
            # Look up new CIKs
            cik_dict = lookup_ciks(new_lookups)
            
            # Process results for this batch
            for fund in batch:
                if fund in existing_results:
                    cik = existing_results[fund]
                    found_count += 1
                elif fund in cik_dict:
                    cik = str(cik_dict[fund]).zfill(10)
                    found_count += 1
                    print(f"Found new CIK for {fund}: {cik}")
                else:
                    cik = 'NOT_FOUND'
                
                results.append(f"{fund}\t{cik}")
            
            # Add delay between batches
            time.sleep(0.5)
    
    # Save all results
    with open('hedge_funds_with_ciks.txt', 'w') as f:
        for result in results:
            f.write(f"{result}\n")
    
    # Print summary
    print(f"\nResults saved to 'hedge_funds_with_ciks.txt'")
    print(f"Total CIKs found: {found_count}")
    print(f"Missing CIKs: {len(hedge_funds) - found_count}")
    
    # Show sample of missing ones
    print("\nSample of funds still missing CIKs:")
    missing = [fund for fund, result in zip(hedge_funds, results) if 'NOT_FOUND' in result]
    for fund in missing[:5]:
        print(f"- {fund}")

def manual_cik_lookup():
    """Function to manually look up specific CIKs"""
    print("Enter a hedge fund name to look up (or 'quit' to exit):")
    while True:
        fund = input("> ").strip()
        if fund.lower() == 'quit':
            break
        cik = try_sec_api_endpoints(fund)
        print(f"Result for {fund}: {cik}")

def test_single_lookup():
    """Test the lookup with a single known company"""
    test_companies = ['APPLE INC', 'MICROSOFT CORP', 'BERKSHIRE HATHAWAY INC']
    print("Testing lookup with known companies...")
    result = lookup_ciks(test_companies)
    print("Results:", result)

if __name__ == "__main__":
    # First test with known companies
    test_single_lookup()
    
    print("\nContinue with full process? (y/n)")
    if input().lower() == 'y':
        process_hedge_funds()
