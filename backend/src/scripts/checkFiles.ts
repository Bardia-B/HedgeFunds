import * as fs from 'fs'
import * as path from 'path'

function checkFiles() {
    const baseDir = path.join(__dirname, '../../../')  // This should point to your root folder
    console.log('Looking in directory:', baseDir)
    
    const folders = fs.readdirSync(baseDir)
    console.log('\nFound folders:', folders)
    
    for (const folder of folders) {
        if (folder.startsWith('filings_13f_')) {
            const cik = folder.replace('filings_13f_', '')
            const metadataPath = path.join(baseDir, folder, 'form13f_metadata.csv')
            const holdingsPath = path.join(baseDir, folder, 'all_13f_holdings.csv')
            
            console.log(`\nChecking CIK: ${cik}`)
            
            if (fs.existsSync(metadataPath)) {
                const stats = fs.statSync(metadataPath)
                console.log(`Metadata file exists: ${stats.size} bytes`)
                
                // Read first few lines
                const content = fs.readFileSync(metadataPath, 'utf8').split('\n').slice(0, 3)
                console.log('First few lines:', content)
            } else {
                console.log('❌ No metadata file found')
            }
            
            if (fs.existsSync(holdingsPath)) {
                const stats = fs.statSync(holdingsPath)
                console.log(`Holdings file exists: ${stats.size} bytes`)
                
                // Read first few lines
                const content = fs.readFileSync(holdingsPath, 'utf8').split('\n').slice(0, 3)
                console.log('First few lines:', content)
            } else {
                console.log('❌ No holdings file found')
            }
        }
    }
}

checkFiles() 