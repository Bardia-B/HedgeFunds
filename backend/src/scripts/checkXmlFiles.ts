import * as fs from 'fs'
import * as path from 'path'

function checkXmlFiles() {
    const baseDir = path.join(__dirname, '../../../')
    const folders = fs.readdirSync(baseDir)
    
    for (const folder of folders) {
        if (folder.startsWith('filings_13f_')) {
            const cik = folder.replace('filings_13f_', '')
            console.log(`\nChecking CIK: ${cik}`)
            
            // Check the filing folders
            const filingFolders = fs.readdirSync(path.join(baseDir, folder))
            for (const filingFolder of filingFolders) {
                if (filingFolder.startsWith('filing_')) {
                    const xmlPath = path.join(baseDir, folder, filingFolder, 'form13fInfoTable.xml')
                    if (fs.existsSync(xmlPath)) {
                        const stats = fs.statSync(xmlPath)
                        console.log(`Found XML in ${filingFolder}: ${stats.size} bytes`)
                    }
                }
            }
        }
    }
}

checkXmlFiles() 