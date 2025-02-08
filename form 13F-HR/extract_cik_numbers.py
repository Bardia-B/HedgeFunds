def extract_cik_numbers():
    """Extract only CIK numbers from valid_ciks.txt and save to cik_numbers.txt"""
    try:
        # Read valid_ciks.txt and extract only the CIK numbers
        cik_numbers = []
        with open('testing/valid_ciks.txt', 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        cik = parts[1].strip()
                        # Ensure it's a valid CIK number
                        if cik.isdigit():
                            # Pad with leading zeros to 10 digits
                            cik_numbers.append(cik.zfill(10))
        
        # Sort the CIK numbers
        cik_numbers.sort()
        
        # Save to new file
        with open('cik_numbers.txt', 'w') as f:
            for cik in cik_numbers:
                f.write(f"{cik}\n")
        
        print(f"Successfully extracted {len(cik_numbers)} CIK numbers")
        print("Data saved to cik_numbers.txt")
        
        # Print first few entries as sample
        print("\nSample entries:")
        for cik in cik_numbers[:5]:
            print(cik)
            
    except FileNotFoundError:
        print("Error: valid_ciks.txt not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    extract_cik_numbers() 