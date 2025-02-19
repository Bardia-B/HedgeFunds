import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

class HedgeFundAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        
        # Convert accession number to date (format: 0000919574-13-005137)
        def extract_date_from_accession(acc_num):
            try:
                # Extract year from accession number (position 11-13)
                year = '20' + acc_num.split('-')[1]
                # Use first day of the quarter for simplicity
                return f"{year}-01-01"
            except:
                return None
        
        # Convert accession numbers to dates
        self.df['Filing Date'] = pd.to_datetime(
            self.df['Filing Date'].apply(extract_date_from_accession)
        )
        
        # Convert value columns to numeric
        numeric_cols = ['VALUE (x$1000)', 'SHRS OR PRN AMT', 
                       'VOTING AUTHORITY SOLE', 'VOTING AUTHORITY SHARED', 
                       'VOTING AUTHORITY NONE']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
    
    def generate_fund_summary(self, fund_name):
        """Generate a summary for a specific fund"""
        fund_data = self.df[self.df['Fund Name'] == fund_name]
        
        # Get date range
        date_range = f"{fund_data['Filing Date'].min():%Y-%m-%d} to {fund_data['Filing Date'].max():%Y-%m-%d}"
        
        # Calculate key metrics
        total_value = fund_data['VALUE (x$1000)'].sum() * 1000  # Convert back to dollars
        unique_stocks = fund_data['NAME OF ISSUER'].nunique()
        avg_position_size = total_value / unique_stocks if unique_stocks > 0 else 0
        
        # Get top holdings
        latest_filing = fund_data[fund_data['Filing Date'] == fund_data['Filing Date'].max()]
        top_holdings = latest_filing.nlargest(10, 'VALUE (x$1000)')
        
        # Calculate portfolio concentration (top 10 holdings as % of total)
        total_portfolio_value = latest_filing['VALUE (x$1000)'].sum()
        concentration = (top_holdings['VALUE (x$1000)'].sum() / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
        
        return {
            'fund_name': fund_name,
            'date_range': date_range,
            'total_value': total_value,
            'unique_stocks': unique_stocks,
            'avg_position_size': avg_position_size,
            'top_holdings': top_holdings,
            'portfolio_concentration': concentration
        }
    
    def plot_portfolio_evolution(self, fund_name):
        """Plot the evolution of portfolio value over time"""
        fund_data = self.df[self.df['Fund Name'] == fund_name]
        portfolio_values = fund_data.groupby('Filing Date')['VALUE (x$1000)'].sum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=portfolio_values.index, 
            y=portfolio_values.values,
            mode='lines+markers',
            name='Portfolio Value'
        ))
        fig.update_layout(
            title=f'{fund_name} - Portfolio Value Over Time',
            xaxis_title='Filing Date',
            yaxis_title='Value ($ Millions)',
            hovermode='x'
        )
        return fig
    
    def analyze_sector_exposure(self, fund_name, date=None):
        """Analyze sector exposure for a specific date or latest filing"""
        fund_data = self.df[self.df['Fund Name'] == fund_name]
        if date:
            fund_data = fund_data[fund_data['Filing Date'] == date]
        else:
            latest_date = fund_data['Filing Date'].max()
            fund_data = fund_data[fund_data['Filing Date'] == latest_date]
        
        holdings_by_value = fund_data.groupby('NAME OF ISSUER')['VALUE (x$1000)'].sum().sort_values(ascending=False)
        total_value = holdings_by_value.sum()
        holdings_by_percentage = (holdings_by_value / total_value * 100).round(2)
        
        return holdings_by_percentage
    
    def calculate_turnover(self, fund_name):
        """Calculate portfolio turnover between filings"""
        fund_data = self.df[self.df['Fund Name'] == fund_name]
        dates = sorted(fund_data['Filing Date'].unique())
        
        turnovers = []
        for i in range(len(dates)-1):
            holdings_t1 = fund_data[fund_data['Filing Date'] == dates[i]]
            holdings_t2 = fund_data[fund_data['Filing Date'] == dates[i+1]]
            
            merged = pd.merge(holdings_t1, holdings_t2, 
                            on=['NAME OF ISSUER'], 
                            how='outer', 
                            suffixes=('_t1', '_t2'))
            
            merged = merged.fillna(0)
            total_t1 = merged['VALUE (x$1000)_t1'].sum()
            turnover = abs(merged['VALUE (x$1000)_t2'] - merged['VALUE (x$1000)_t1']).sum() / total_t1 if total_t1 > 0 else 0
            
            turnovers.append({
                'date': dates[i+1],
                'turnover': turnover * 100  # Convert to percentage
            })
            
        return pd.DataFrame(turnovers)

    def generate_html_report(self, fund_name):
        """Generate an HTML report with all analyses"""
        summary = self.generate_fund_summary(fund_name)
        portfolio_evolution = self.plot_portfolio_evolution(fund_name)
        turnover = self.calculate_turnover(fund_name)
        sector_exposure = self.analyze_sector_exposure(fund_name)
        
        html = f"""
        <h1>{fund_name} - Investment Analysis</h1>
        <h2>Summary ({summary['date_range']})</h2>
        <ul>
            <li>Total Portfolio Value: ${summary['total_value']:,.2f}</li>
            <li>Unique Stocks: {summary['unique_stocks']}</li>
            <li>Average Position Size: ${summary['avg_position_size']:,.2f}</li>
            <li>Portfolio Concentration (Top 10): {summary['portfolio_concentration']:.1f}%</li>
        </ul>
        
        <h2>Top 10 Holdings (Latest Filing)</h2>
        {summary['top_holdings'].to_html()}
        
        <h2>Portfolio Evolution</h2>
        {portfolio_evolution.to_html()}
        
        <h2>Portfolio Turnover</h2>
        {turnover.to_html()}
        
        <h2>Holdings by Value (%)</h2>
        {sector_exposure.head(20).to_frame().to_html()}
        """
        
        return html

def save_fund_analysis(df, output_dir="filling/analysis"):
    """Save analysis for all funds"""
    os.makedirs(output_dir, exist_ok=True)
    analyzer = HedgeFundAnalyzer(df)
    
    for fund_name in df['Fund Name'].unique():
        print(f"Analyzing {fund_name}...")
        
        # Generate report
        html_report = analyzer.generate_html_report(fund_name)
        
        # Save report with UTF-8 encoding
        report_path = os.path.join(output_dir, f"{fund_name.replace(' ', '_')}_analysis.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # Save plots
        portfolio_evolution = analyzer.plot_portfolio_evolution(fund_name)
        portfolio_evolution.write_html(
            os.path.join(output_dir, f"{fund_name.replace(' ', '_')}_portfolio.html")
        )
        
        print(f"Analysis saved to {report_path}")

if __name__ == "__main__":
    # Read the CSV file
    df = pd.read_csv('filling/fund_0001273087/form13f_holdings.csv')
    
    # Add Fund Name column if it doesn't exist
    if 'Fund Name' not in df.columns:
        df['Fund Name'] = 'Millennium Management LLC'  # Using actual fund name
    
    # Save analysis
    save_fund_analysis(df)