import os
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import requests
import pandas as pd
from datetime import datetime
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")
DASH_HOST = os.getenv("DASH_HOST", "0.0.0.0")
DASH_PORT = int(os.getenv("DASH_PORT", "8050"))
DASH_DEBUG = os.getenv("DASH_DEBUG", "False").lower() == "true"

# Clean Blue & White Color Palette
COLORS = {
    'primary_blue': '#2E86AB',
    'light_blue': '#A23B72',
    'accent_blue': '#F18F01',
    'dark_blue': '#C73E1D',
    'background': '#FFFFFF',
    'card_bg': '#FAFBFC',
    'border': '#E1E5E9',
    'text_dark': '#2D3748',
    'text_light': '#718096',
    'success': '#38A169',
    'warning': '#D69E2E',
    'danger': '#E53E3E'
}

app = dash.Dash(__name__)
app.title = "FPTI Financial Dashboard"

# Custom CSS styling
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("FPTI Financial Dashboard",
                   style={
                       'color': 'white',
                       'font-family': 'Inter, -apple-system, sans-serif',
                       'font-weight': '700',
                       'font-size': '2.5rem',
                       'margin': '0',
                       'letter-spacing': '-0.02em'
                   }),
            html.P("Track your financial health in real-time",
                  style={
                      'color': 'rgba(255, 255, 255, 0.9)',
                      'font-family': 'Inter, -apple-system, sans-serif',
                      'font-size': '1.1rem',
                      'margin': '8px 0 0 0'
                  })
        ], style={
            'max-width': '1200px',
            'margin': '0 auto',
            'padding': '0 2rem'
        })
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["primary_blue"]} 0%, {COLORS["dark_blue"]} 100%)',
        'padding': '2rem 0',
        'margin-bottom': '2rem',
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),
    
    # Main Content Container
    html.Div([
        # Key Metrics Row
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Net Worth", style={'color': COLORS['text_dark'], 'margin': '0 0 10px 0', 'font-size': '1rem', 'font-weight': '600'}),
                    html.Div(id='net-worth-value', style={'font-size': '2rem', 'font-weight': '700', 'color': COLORS['primary_blue']})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '24%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.H3("Portfolio Value", style={'color': COLORS['text_dark'], 'margin': '0 0 10px 0', 'font-size': '1rem', 'font-weight': '600'}),
                    html.Div(id='portfolio-value', style={'font-size': '2rem', 'font-weight': '700', 'color': COLORS['success']})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '24%', 'display': 'inline-block', 'margin-left': '1.33%'}),
            
            html.Div([
                html.Div([
                    html.H3("Monthly Income", style={'color': COLORS['text_dark'], 'margin': '0 0 10px 0', 'font-size': '1rem', 'font-weight': '600'}),
                    html.Div(id='monthly-income', style={'font-size': '2rem', 'font-weight': '700', 'color': COLORS['accent_blue']})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '24%', 'display': 'inline-block', 'margin-left': '1.33%'}),
            
            html.Div([
                html.Div([
                    html.H3("Monthly Expenses", style={'color': COLORS['text_dark'], 'margin': '0 0 10px 0', 'font-size': '1rem', 'font-weight': '600'}),
                    html.Div(id='monthly-expenses', style={'font-size': '2rem', 'font-weight': '700', 'color': COLORS['danger']})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '24%', 'display': 'inline-block', 'margin-left': '1.33%'})
        ], style={'margin-bottom': '2rem'}),
        
        # Charts Row 1
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Cash Flow Analysis", style={'color': COLORS['text_dark'], 'margin': '0 0 20px 0', 'font-size': '1.2rem', 'font-weight': '600'}),
                    dcc.Graph(id='cash-flow-chart', style={'height': '400px'})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '65%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.H3("Asset Allocation", style={'color': COLORS['text_dark'], 'margin': '0 0 20px 0', 'font-size': '1.2rem', 'font-weight': '600'}),
                    dcc.Graph(id='asset-allocation-chart', style={'height': '400px'})
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '33%', 'display': 'inline-block', 'margin-left': '2%'})
        ], style={'margin-bottom': '2rem'}),
        
        # Charts Row 2
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recent Transactions", style={'color': COLORS['text_dark'], 'margin': '0 0 20px 0', 'font-size': '1.2rem', 'font-weight': '600'}),
                    html.Div(id='transactions-table')
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '65%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.H3("Monte Carlo Projection", style={'color': COLORS['text_dark'], 'margin': '0 0 20px 0', 'font-size': '1.2rem', 'font-weight': '600'}),
                    html.Div(id='monte-carlo-analysis')
                ], style={
                    'background': COLORS['card_bg'],
                    'padding': '1.5rem',
                    'border-radius': '12px',
                    'border': f'1px solid {COLORS["border"]}',
                    'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.02)'
                })
            ], style={'width': '33%', 'display': 'inline-block', 'margin-left': '2%'})
        ], style={'margin-bottom': '2rem'}),
        
        # Auto-refresh interval
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        )
    ], style={
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '0 2rem'
    }),
    
    # Footer
    html.Div([
        html.P(f"© 2025 FPTI Financial Dashboard - Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
              style={'color': COLORS['text_light'], 'text-align': 'center', 'margin': '0'})
    ], style={
        'padding': '2rem 0',
        'border-top': f'1px solid {COLORS["border"]}',
        'margin-top': '3rem'
    })
], style={
    'font-family': 'Inter, -apple-system, sans-serif',
    'background-color': COLORS['background'],
    'min-height': '100vh'
})

# Helper function to safely make API calls
def safe_api_call(url, default_value=None):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API call failed for {url}: {e}")
        return default_value or {}

# Callbacks
@app.callback(
    [Output('net-worth-value', 'children'),
     Output('portfolio-value', 'children'),
     Output('monthly-income', 'children'),
     Output('monthly-expenses', 'children'),
     Output('cash-flow-chart', 'figure'),
     Output('asset-allocation-chart', 'figure'),
     Output('transactions-table', 'children'),
     Output('monte-carlo-analysis', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    # Fetch data
    net_worth_data = safe_api_call(f"{API_BASE}/net-worth", {"net_worth": 0})
    portfolio_data = safe_api_call(f"{API_BASE}/portfolio/value", {"portfolio_value": 0})
    cash_flow_data = safe_api_call(f"{API_BASE}/cash-flow", {"income": [], "expenses": [], "dates": []})
    asset_allocation_data = safe_api_call(f"{API_BASE}/asset-allocation", {})
    transactions_data = safe_api_call(f"{API_BASE}/transactions", [])
    monte_carlo_data = safe_api_call(f"{API_BASE}/monte-carlo", {})
    
    # Format key metrics
    net_worth = f"${net_worth_data.get('net_worth', 0):,.2f}"
    portfolio_value = f"${portfolio_data.get('portfolio_value', 0):,.2f}"
    
    # Calculate monthly income/expenses
    income_list = cash_flow_data.get('income', [])
    expenses_list = cash_flow_data.get('expenses', [])
    monthly_income = f"${income_list[-1]:,.2f}" if income_list else "$0.00"
    monthly_expenses = f"${expenses_list[-1]:,.2f}" if expenses_list else "$0.00"
    
    # Cash Flow Chart
    cash_flow_fig = go.Figure()
    if cash_flow_data.get('dates'):
        cash_flow_fig.add_trace(go.Scatter(
            x=cash_flow_data['dates'],
            y=cash_flow_data['income'],
            mode='lines+markers',
            name='Income',
            line=dict(color=COLORS['success'], width=3),
            marker=dict(size=8)
        ))
        cash_flow_fig.add_trace(go.Scatter(
            x=cash_flow_data['dates'],
            y=cash_flow_data['expenses'],
            mode='lines+markers',
            name='Expenses',
            line=dict(color=COLORS['danger'], width=3),
            marker=dict(size=8)
        ))
    
    cash_flow_fig.update_layout(
        title="",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        template='plotly_white',
        font=dict(family="Inter, -apple-system, sans-serif"),
        margin=dict(t=20, r=20, b=40, l=60),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Asset Allocation Chart
    asset_allocation_fig = go.Figure()
    if asset_allocation_data:
        asset_allocation_fig.add_trace(go.Pie(
            labels=list(asset_allocation_data.keys()),
            values=list(asset_allocation_data.values()),
            hole=0.4,
            marker_colors=[COLORS['primary_blue'], COLORS['success'], COLORS['accent_blue']],
            textinfo='label+percent',
            textfont_size=12
        ))
    
    asset_allocation_fig.update_layout(
        title="",
        template='plotly_white',
        font=dict(family="Inter, -apple-system, sans-serif"),
        margin=dict(t=20, r=20, b=20, l=20),
        showlegend=False
    )
    
    # Transactions Table
    transactions_table = html.Div([
        html.Div([
            html.Div("Date", style={'font-weight': '600', 'color': COLORS['text_dark']}),
            html.Div("Description", style={'font-weight': '600', 'color': COLORS['text_dark']}),
            html.Div("Category", style={'font-weight': '600', 'color': COLORS['text_dark']}),
            html.Div("Amount", style={'font-weight': '600', 'color': COLORS['text_dark'], 'text-align': 'right'})
        ], style={
            'display': 'grid',
            'grid-template-columns': '1fr 2fr 1fr 1fr',
            'gap': '1rem',
            'padding': '0.75rem',
            'border-bottom': f'2px solid {COLORS["border"]}',
            'margin-bottom': '0.5rem'
        })
    ] + [
        html.Div([
            html.Div(transaction['date'][:10], style={'color': COLORS['text_light']}),
            html.Div(transaction['description'][:30] + ("..." if len(transaction['description']) > 30 else ""), 
                    style={'color': COLORS['text_dark']}),
            html.Div(transaction['category'], style={'color': COLORS['text_light']}),
            html.Div(f"${transaction['amount']:,.2f}", 
                    style={'color': COLORS['success'] if transaction['amount'] > 0 else COLORS['danger'], 
                          'text-align': 'right', 'font-weight': '600'})
        ], style={
            'display': 'grid',
            'grid-template-columns': '1fr 2fr 1fr 1fr',
            'gap': '1rem',
            'padding': '0.75rem',
            'border-bottom': f'1px solid {COLORS["border"]}',
            'border-radius': '4px'
        })
        for transaction in transactions_data[:10]  # Show only first 10 transactions
    ])
    
    # Monte Carlo Analysis
    monte_carlo_analysis = html.Div([
        html.P("10-Year Portfolio Projections:", style={'font-weight': '600', 'margin-bottom': '1rem', 'color': COLORS['text_dark']}),
        html.Div([
            html.Div([
                html.Div("Conservative (10%)", style={'font-size': '0.9rem', 'color': COLORS['text_light']}),
                html.Div(f"${monte_carlo_data.get('percentile_10', 0):,.0f}", 
                        style={'font-size': '1.5rem', 'font-weight': '700', 'color': COLORS['danger']})
            ], style={'margin-bottom': '1rem'}),
            html.Div([
                html.Div("Expected (50%)", style={'font-size': '0.9rem', 'color': COLORS['text_light']}),
                html.Div(f"${monte_carlo_data.get('percentile_50', 0):,.0f}", 
                        style={'font-size': '1.5rem', 'font-weight': '700', 'color': COLORS['primary_blue']})
            ], style={'margin-bottom': '1rem'}),
            html.Div([
                html.Div("Optimistic (90%)", style={'font-size': '0.9rem', 'color': COLORS['text_light']}),
                html.Div(f"${monte_carlo_data.get('percentile_90', 0):,.0f}", 
                        style={'font-size': '1.5rem', 'font-weight': '700', 'color': COLORS['success']})
            ])
        ])
    ])
    
    return (net_worth, portfolio_value, monthly_income, monthly_expenses, 
            cash_flow_fig, asset_allocation_fig, transactions_table, monte_carlo_analysis)

if __name__ == '__main__':
    app.run_server(debug=DASH_DEBUG, host=DASH_HOST, port=DASH_PORT)