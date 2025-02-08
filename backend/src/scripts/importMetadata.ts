import fs from 'fs'
import path from 'path'
import { parse } from 'csv-parse'
import mysql from 'mysql2/promise'
import dotenv from 'dotenv'

dotenv.config()

interface FilingMetadata {
    accessionNumber: string;
    filingDate: string;
    reportDate: string;
    form: string;
    fileNumber: string;
    size: number;
}

async function processMetadataFile(filePath: string, cik: string, connection: mysql.Connection) {
    const fileContent = fs.readFileSync(filePath, { encoding: 'utf-8' })
    
    return new Promise((resolve, reject) => {
        parse(fileContent, {
            columns: true,
            skip_empty_lines: true
        }, async (err, records: FilingMetadata[]) => {
            if (err) {
                reject(err)
                return
            }

            try {
                for (const record of records) {
                    await connection.execute(
                        `INSERT IGNORE INTO filings_metadata 
                        (cik, accession_number, filing_date, report_date, form, file_number, size)
                        VALUES (?, ?, ?, ?, ?, ?, ?)`,
                        [
                            cik,
                            record.accessionNumber,
                            new Date(record.filingDate),
                            new Date(record.reportDate),
                            record.form,
                            record.fileNumber,
                            record.size
                        ]
                    )
                }
                resolve(records.length)
            } catch (error) {
                reject(error)
            }
        })
    })
}

async function importAllMetadata() {
    const connection = await mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME
    })

    try {
        const baseDir = path.join(__dirname, '../../../form 13F-HR')
        const folders = fs.readdirSync(baseDir)
        
        for (const folder of folders) {
            if (folder.startsWith('filings_13f_')) {
                const cik = folder.replace('filings_13f_', '')
                const metadataPath = path.join(baseDir, folder, 'form13f_metadata.csv')
                
                if (fs.existsSync(metadataPath)) {
                    try {
                        const recordCount = await processMetadataFile(metadataPath, cik, connection)
                        console.log(`Processed ${recordCount} records for CIK ${cik}`)
                    } catch (error) {
                        console.error(`Error processing ${cik}: ${error}`)
                    }
                }
            }
        }
    } finally {
        await connection.end()
    }
}

importAllMetadata().catch(console.error) 