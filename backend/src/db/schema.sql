CREATE TABLE IF NOT EXISTS filings_metadata (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cik VARCHAR(10) NOT NULL,
    accession_number VARCHAR(20) NOT NULL,
    filing_date DATE NOT NULL,
    report_date DATE NOT NULL,
    form VARCHAR(10) NOT NULL,
    file_number VARCHAR(20),
    size INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_filing (cik, accession_number)
);

CREATE TABLE IF NOT EXISTS filings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filing_id VARCHAR(50) NOT NULL,
    filing_date DATE NOT NULL,
    cik VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_filing (filing_id)
);

CREATE TABLE IF NOT EXISTS holdings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filing_id INT NOT NULL,
    name_of_issuer VARCHAR(255) NOT NULL,
    title_of_class VARCHAR(100),
    cusip VARCHAR(9),
    value DECIMAL(15, 2),
    shares DECIMAL(15, 2),
    share_type VARCHAR(5),
    put_call VARCHAR(4),
    investment_discretion VARCHAR(20),
    other_manager VARCHAR(100),
    voting_authority_sole INT,
    voting_authority_shared INT,
    voting_authority_none INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (filing_id) REFERENCES filings(id)
); 