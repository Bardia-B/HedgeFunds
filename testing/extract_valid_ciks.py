def extract_valid_ciks():
    """Extract valid CIKs and company names from hedge_funds_with_ciks.txt"""
    valid_entries = []
    
    try:
        with open('hedge_funds_with_ciks.txt', 'r') as f:
            for line in f:
                if 'NOT_FOUND' not in line and line.strip():
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        company = parts[0].strip()
                        cik = parts[1].strip()
                        # Ensure it's a valid CIK
                        if cik.isdigit():
                            # Pad with leading zeros to 10 digits
                            cik = cik.zfill(10)
                            valid_entries.append(f"{company}\t{cik}")
    
        # Save to new file
        with open('valid_ciks.txt', 'w') as f:
            for entry in valid_entries:
                f.write(f"{entry}\n")
        
        print(f"Successfully extracted {len(valid_entries)} valid CIKs")
        print("Data saved to valid_ciks.txt")
        
        # Print first few entries as sample
        print("\nSample entries:")
        for entry in valid_entries[:5]:
            print(entry)
            
    except FileNotFoundError:
        print("hedge_funds_with_ciks.txt not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    extract_valid_ciks() 