
import { useNavigate, useLocation } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import { ThemeToggle } from './components/ThemeToggle'
import SearchPage from './components/SearchPage'
import DataDisplay from './components/DataDisplay'

function App() {
  const location = useLocation()
  const isHomePage = location.pathname === '/'

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background text-foreground">
        <header className="fixed top-4 right-4 z-50">
          <ThemeToggle />
        </header>
        <div className="container mx-auto px-4 py-8">
          {/* Search bar always visible */}
          <div className="mb-8">
            <SearchPage minimal={!isHomePage} />
          </div>
          
          {/* Main content with ad space padding */}
          <div className="grid grid-cols-12 gap-4">
            {/* Left ad space */}
            <div className="hidden xl:block col-span-2">
              <div className="h-full w-full bg-muted/5 rounded-lg">
                {/* Ad space */}
              </div>
            </div>

            {/* Main content */}
            <main className="col-span-12 xl:col-span-8">
              {!isHomePage && <DataDisplay />}
            </main>

            {/* Right ad space */}
            <div className="hidden xl:block col-span-2">
              <div className="h-full w-full bg-muted/5 rounded-lg">
                {/* Ad space */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App