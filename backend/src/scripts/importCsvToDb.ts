import { createConnection } from 'mysql2/promise'
import * as fs from 'fs'
import * as path from 'path'
import { parse } from 'csv-parse'
import * as dotenv from 'dotenv'
import * as os from 'os'

dotenv.config()

interface Holding {
    'NAME OF ISSUER': string
    'TITLE OF CLASS': string
    'CUSIP': string
    'VALUE (x$1000)': string
    'SHRS OR PRN AMT': string
    'SH/PRN': string
    'PUT/CALL': string
    'INVESTMENT DISCRETION': string
    'OTHER MANAGER': string
    'VOTING AUTHORITY SOLE': string
    'VOTING AUTHORITY SHARED': string
    'VOTING AUTHORITY NONE': string
    'Filing Date': string
    'CIK': string
}

interface FilingMetadata {
    accessionNumber: string
    filingDate: string
    reportDate: string
    form: string
    fileNumber: string
    size: number
}

function extractDateFromFilingId(filingId: string): string {
    // Filing ID format: 0001567619-22-020109
    const parts = filingId.split('-')
    if (parts.length >= 2) {
        const year = `20${parts[1]}`
        const quarter = Math.ceil(parseInt(parts[2].substring(0, 2)) / 3)
        const quarterEndDates = {
            1: '03-31',
            2: '06-30',
            3: '09-30',
            4: '12-31'
        }
        return `${year}-${quarterEndDates[quarter]}`
    }
    return '2024-01-01' // Default date if parsing fails
}

async function findMostRecentHoldingsFile(): Promise<string | null> {
    const downloadsPath = path.join(os.homedir(), 'Downloads')
    const files = fs.readdirSync(downloadsPath)
    
    const holdingsFiles = files
        .filter(file => file.startsWith('all_13f_holdings_') && file.endsWith('.csv'))
        .map(file => ({
            name: file,
            path: path.join(downloadsPath, file),
            time: fs.statSync(path.join(downloadsPath, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time)

    return holdingsFiles.length > 0 ? holdingsFiles[0].path : null
}

async function importCsvData() {
    console.log('Starting import process...')
    
    const holdingsFile = await findMostRecentHoldingsFile()
    if (!holdingsFile) {
        console.error('No holdings file found in Downloads folder')
        return
    }
    
    console.log(`Found holdings file: ${holdingsFile}`)

    const connection = await createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME
    })

    try {
        // Clear existing data
        console.log('Clearing existing data...')
        await connection.execute('DELETE FROM holdings')
        await connection.execute('DELETE FROM filings')

        // Read and parse the CSV file
        const holdingsContent = fs.readFileSync(holdingsFile, { encoding: 'utf-8' })
        const holdings = await new Promise<Holding[]>((resolve, reject) => {
            parse(holdingsContent, {
                columns: true,
                skip_empty_lines: true
            }, (err, records) => {
                if (err) reject(err)
                else resolve(records as Holding[])
            })
        })

        console.log(`Found ${holdings.length} holdings to process`)

        // Group holdings by CIK and Filing ID
        const filingGroups = new Map<string, Holding[]>()
        holdings.forEach(holding => {
            const key = `${holding.CIK}_${holding['Filing Date']}`
            if (!filingGroups.has(key)) {
                filingGroups.set(key, [])
            }
            filingGroups.get(key)!.push(holding)
        })

        let totalFilings = 0
        let totalHoldings = 0

        // Process each filing group
        for (const [key, filingHoldings] of filingGroups) {
            const [cik, filingId] = key.split('_')
            
            try {
                // Extract date from filing ID
                const filingDate = extractDateFromFilingId(filingId)
                console.log(`Processing filing: ${filingId} with date ${filingDate}`)

                // Create filing record
                const [filingResult] = await connection.execute(
                    `INSERT INTO filings (filing_id, filing_date, cik) 
                     VALUES (?, ?, ?)`,
                    [filingId, filingDate, cik]
                )
                const dbFilingId = (filingResult as any).insertId
                totalFilings++

                // Insert holdings for this filing
                for (const holding of filingHoldings) {
                    try {
                        await connection.execute(
                            `INSERT INTO holdings (
                                filing_id,
                                name_of_issuer,
                                title_of_class,
                                cusip,
                                value,
                                shares,
                                share_type,
                                put_call,
                                investment_discretion,
                                other_manager,
                                voting_authority_sole,
                                voting_authority_shared,
                                voting_authority_none
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                            [
                                dbFilingId,
                                holding['NAME OF ISSUER'],
                                holding['TITLE OF CLASS'],
                                holding['CUSIP'],
                                parseInt(holding['VALUE (x$1000)']) || 0,
                                parseInt(holding['SHRS OR PRN AMT']) || 0,
                                holding['SH/PRN'],
                                holding['PUT/CALL'] || null,
                                holding['INVESTMENT DISCRETION'],
                                holding['OTHER MANAGER'] || null,
                                parseInt(holding['VOTING AUTHORITY SOLE']) || 0,
                                parseInt(holding['VOTING AUTHORITY SHARED']) || 0,
                                parseInt(holding['VOTING AUTHORITY NONE']) || 0
                            ]
                        )
                        totalHoldings++
                    } catch (error) {
                        console.error(`Error inserting holding for ${holding['NAME OF ISSUER']}:`, error)
                    }
                }
                
                console.log(`Processed ${filingHoldings.length} holdings for CIK ${cik} on ${filingDate}`)
            } catch (error) {
                console.error(`Error processing filing group ${key}:`, error)
            }
        }

        console.log('\nImport completed successfully!')
        console.log(`Total filings processed: ${totalFilings}`)
        console.log(`Total holdings processed: ${totalHoldings}`)

    } catch (error) {
        console.error('Error importing data:', error)
    } finally {
        await connection.end()
    }
}

importCsvData().catch(console.error) 