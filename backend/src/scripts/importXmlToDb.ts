import * as fs from 'fs'
import * as path from 'path'
import * as xml2js from 'xml2js'
import mysql from 'mysql2/promise'
import dotenv from 'dotenv'

dotenv.config()

async function parseXmlFile(xmlPath: string): Promise<any> {
    try {
        console.log(`Reading file: ${xmlPath}`)
        const xmlContent = fs.readFileSync(xmlPath, 'utf-8')
        console.log(`XML content length: ${xmlContent.length} bytes`)
        
        // Create parser with more lenient options
        const parser = new xml2js.Parser({
            explicitArray: false,
            ignoreAttrs: true,
            // Add XML namespaces
            xmlns: true,
            normalizeTags: true,
            explicitRoot: false,
            tagNameProcessors: [xml2js.processors.stripPrefix]
        })
        
        // Clean the XML content
        const cleanXml = xmlContent
            .replace(/xmlns=["'][^"']+["']/g, '')  // Remove xmlns declarations
            .replace(/ns1:/g, '')                   // Remove ns1: prefixes
            .replace(/\r?\n\s*/g, '')              // Remove whitespace
        
        const result = await parser.parseStringPromise(cleanXml)
        console.log('XML parsed successfully')
        return result
    } catch (error) {
        console.error(`Error parsing XML file ${xmlPath}:`, error.message)
        // Log the first 500 characters of the file for debugging
        const content = fs.readFileSync(xmlPath, 'utf-8').slice(0, 500)
        console.log('File start:', content)
        return null
    }
}

async function importXmlData() {
    console.log('Starting import process...')
    
    // First check if we can connect to the database
    const connection = await mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME
    })
    
    console.log('Connected to database successfully')

    try {
        // Clear existing data
        console.log('Clearing existing data...')
        await connection.execute('DELETE FROM holdings')
        await connection.execute('DELETE FROM filings')
        
        const baseDir = path.join(__dirname, '../../../')
        console.log('Looking for files in:', baseDir)
        
        const folders = fs.readdirSync(baseDir)
        console.log('Found folders:', folders.filter(f => f.startsWith('filings_13f_')))
        
        let totalFilings = 0
        let totalHoldings = 0

        for (const folder of folders) {
            if (folder.startsWith('filings_13f_')) {
                const cik = folder.replace('filings_13f_', '')
                console.log(`\nProcessing CIK: ${cik}`)
                
                const filingFolders = fs.readdirSync(path.join(baseDir, folder))
                console.log(`Found ${filingFolders.length} filing folders`)
                
                for (const filingFolder of filingFolders) {
                    if (filingFolder.startsWith('filing_')) {
                        const xmlPath = path.join(baseDir, folder, filingFolder, 'form13fInfoTable.xml')
                        if (fs.existsSync(xmlPath)) {
                            console.log(`\nProcessing ${filingFolder}...`)
                            
                            const result = await parseXmlFile(xmlPath)
                            if (!result) {
                                console.log(`Skipping ${filingFolder} due to XML parsing error`)
                                continue
                            }

                            try {
                                // Insert filing record
                                console.log('Inserting filing record...')
                                const [filingResult] = await connection.execute(
                                    `INSERT INTO filings (filing_id, filing_date, cik) 
                                     VALUES (?, CURDATE(), ?)`,
                                    [filingFolder.replace('filing_', ''), cik]
                                )
                                const filingId = (filingResult as any).insertId
                                totalFilings++

                                // Process holdings
                                const infoTables = Array.isArray(result.infotable) 
                                    ? result.infotable 
                                    : [result.infotable]
                                
                                console.log(`Found ${infoTables.length} holdings to process`)
                                
                                let processedCount = 0

                                for (const info of infoTables) {
                                    try {
                                        if (!info) continue
                                        
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
                                                filingId,
                                                info.nameofissuer || '',
                                                info.titleofclass || '',
                                                info.cusip || '',
                                                parseInt(info.value) || 0,
                                                parseInt(info.sshprnamt) || 0,
                                                info.sshprnamttype || '',
                                                info.putcall || null,
                                                info.investmentdiscretion || '',
                                                info.othermanager || null,
                                                parseInt(info.votingauthority?.sole) || 0,
                                                parseInt(info.votingauthority?.shared) || 0,
                                                parseInt(info.votingauthority?.none) || 0
                                            ]
                                        )
                                        processedCount++
                                        totalHoldings++
                                    } catch (error) {
                                        console.error('Error processing holding:', error.message)
                                    }
                                }
                                console.log(`Successfully processed ${processedCount} holdings from ${filingFolder}`)
                            } catch (error) {
                                console.error(`Error processing filing ${filingFolder}:`, error.message)
                            }
                        } else {
                            console.log(`No XML file found for ${filingFolder}`)
                        }
                    }
                }
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

importXmlData().catch(console.error) 