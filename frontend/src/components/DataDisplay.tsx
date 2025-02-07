import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { useParams } from 'react-router-dom'


export default function DataDisplay() {
  const { fundId } = useParams()

  return (
    <div className="space-y-8 py-8">
      {/* Overview and Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Fund Manager</h3>
                <p>Renaissance Technologies LLC</p>
              </div>
              <div>
                <h3 className="font-semibold">Assets Under Management</h3>
                <p>$80.2 Billion</p>
              </div>
              <div>
                <h3 className="font-semibold">Filing Period</h3>
                <p>Q4 2023</p>
              </div>
              <div>
                <h3 className="font-semibold">Portfolio Turnover</h3>
                <p>32% (Quarterly)</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Current Portfolio Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Total Positions</h3>
                <p>3,421 holdings</p>
              </div>
              <div>
                <h3 className="font-semibold">Top 10 Holdings</h3>
                <p>42.3% of portfolio</p>
              </div>
              <div>
                <h3 className="font-semibold">Largest Position</h3>
                <p>AAPL (8.2%)</p>
              </div>
              <div>
                <h3 className="font-semibold">New Positions</h3>
                <p>127 this quarter</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sector Allocation */}
      <Card>
        <CardHeader>
          <CardTitle>Sector Allocation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] bg-muted rounded-lg flex items-center justify-center">
            Heat Map Placeholder
          </div>
        </CardContent>
      </Card>

      {/* Current Holdings */}
      <Card>
        <CardHeader>
          <CardTitle>Current Holdings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-4 font-semibold">
              <div>Company</div>
              <div>Shares</div>
              <div>Value ($M)</div>
              <div>% of Portfolio</div>
            </div>
            <div className="grid grid-cols-4">
              <div>Apple Inc.</div>
              <div>2.5M</div>
              <div>$482.3M</div>
              <div>8.2%</div>
            </div>
            <div className="grid grid-cols-4">
              <div>Microsoft Corp.</div>
              <div>1.8M</div>
              <div>$392.1M</div>
              <div>6.7%</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Last Quarter Changes and AI Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Last Quarter Changes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-green-600">Top Increases</h3>
                <p>NVDA: +250,000 shares (+$145.2M)</p>
                <p>TSLA: +180,000 shares (+$98.3M)</p>
              </div>
              <div>
                <h3 className="font-semibold text-red-600">Top Decreases</h3>
                <p>META: -120,000 shares (-$82.1M)</p>
                <p>AMZN: -95,000 shares (-$67.4M)</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>AI Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Key Insights</h3>
                <ul className="list-disc pl-4 space-y-2">
                  <li>Increased exposure to semiconductor sector by 15%</li>
                  <li>Reduced positions in social media companies</li>
                  <li>New focus on AI-related technologies</li>
                  <li>Defensive positioning in healthcare sector</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Historical Quarters */}
      <Card>
        <CardHeader>
          <CardTitle>Historical Quarters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-4 font-semibold">
              <div>Quarter</div>
              <div>AUM ($B)</div>
              <div>Position Count</div>
              <div>Top Holding</div>
            </div>
            <div className="grid grid-cols-4">
              <div>Q4 2023</div>
              <div>80.2</div>
              <div>3,421</div>
              <div>AAPL</div>
            </div>
            <div className="grid grid-cols-4">
              <div>Q3 2023</div>
              <div>78.5</div>
              <div>3,380</div>
              <div>AAPL</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Voting Power */}
      <Card>
        <CardHeader>
          <CardTitle>Voting Power</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-3 font-semibold">
              <div>Company</div>
              <div>Ownership %</div>
              <div>Voting Rights</div>
            </div>
            <div className="grid grid-cols-3">
              <div>Company A</div>
              <div>5.2%</div>
              <div>4.8%</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent News */}
      <Card>
        <CardHeader>
          <CardTitle>Recent News</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="border-b pb-2">
              <p className="font-semibold">Major Position Increase in Tech Sector</p>
              <p className="text-sm text-muted-foreground">March 15, 2024</p>
            </div>
            <div className="border-b pb-2">
              <p className="font-semibold">New Healthcare Initiative Announced</p>
              <p className="text-sm text-muted-foreground">March 10, 2024</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Enhanced Disclaimer */}
      <div className="text-sm text-muted-foreground space-y-2 mt-12 px-4">
        <p className="text-center font-semibold">Important Disclosure</p>
        <p className="text-center">
          The information presented above is sourced from SEC Form 13F-HR filings, which are required to be filed by institutional investment managers with at least $100 million in qualifying assets. Please note that this data represents positions held as of the filing date and is subject to a 45-day delay from the quarter end as mandated by SEC regulations. The most recent data shown here was last updated on {new Date().toLocaleDateString()}.
        </p>
        <p className="text-center">
          13F filings only disclose long positions in SEC-qualified securities and may not represent the complete investment portfolio of the institution. Short positions, cash holdings, and certain other investment types are not required to be reported.
        </p>
        <p className="text-center font-semibold">
          This information is provided for educational purposes only and should not be construed as financial advice. Always conduct your own research and consult with qualified financial advisors before making investment decisions.
        </p>
      </div>
    </div>
  )
} 