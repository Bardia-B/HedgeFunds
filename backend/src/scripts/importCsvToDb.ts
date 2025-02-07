import { createConnection } from 'mysql2/promise'
import * as fs from 'fs'
import * as path from 'path'
import { parse } from 'csv-parse'
import * as dotenv from 'dotenv'

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
}

function formatFilingDate(filingId: string): string {
    const parts = filingId.split('-')
    const year = '20' + parts[1]
    const quarter = Math.ceil(parseInt(parts[2]) / 3)
    
    const quarterEndDates = {
        1: '03-31',
        2: '06-30',
        3: '09-30',
        4: '12-31'
    }
    
    return `${year}-${quarterEndDates[quarter]}`
}

async function importCsvData() {
    const connection = await createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME
    })

    try {
        // Clear existing data
        await connection.execute('DELETE FROM holdings')
        await connection.execute('DELETE FROM filings')

        const csvFilePath = path.join(__dirname, '../../../form 13F-HR/form13f_holdings.csv')
        const fileContent = fs.readFileSync(csvFilePath, { encoding: 'utf-8' })

        // Parse CSV file
        const records = await new Promise<Holding[]>((resolve, reject) => {
            parse(fileContent, {
                columns: true,
                skip_empty_lines: true
            }, (err, records) => {
                if (err) reject(err)
                else resolve(records as Holding[])
            })
        })

        // Group by filing date
        const filingGroups: { [key: string]: Holding[] } = {}
        records.forEach(record => {
            const filingId = record['Filing Date']  // This is actually the filing ID
            if (!filingGroups[filingId]) {
                filingGroups[filingId] = []
            }
            filingGroups[filingId].push(record)
        })

        // Process each filing
        for (const [filingId, holdings] of Object.entries(filingGroups)) {
            console.log(`Processing filing ${filingId} with ${holdings.length} holdings`)

            // Insert filing with both ID and formatted date
            const [filingResult] = await connection.execute(
                'INSERT INTO filings (filing_id, filing_date, cik) VALUES (?, ?, ?)',
                [
                    filingId,
                    formatFilingDate(filingId),
                    filingId.split('-')[0]
                ]
            )
            const dbFilingId = (filingResult as any).insertId

            // Insert holdings
            for (const holding of holdings) {
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
            }
        }

        console.log('Import completed successfully')

    } catch (error) {
        console.error('Error importing data:', error)
    } finally {
        await connection.end()
    }
}

importCsvData().catch(console.error) 