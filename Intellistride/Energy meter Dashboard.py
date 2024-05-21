import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = {
    'PARAMETER': ['Voltage', 'Current', 'Power', 'Energy'],
    'VALUE': [240, 5, 1200, 3600],
    'DATE': pd.to_datetime(['2024-05-14', '2024-05-14', '2024-05-14', '2024-05-14'])
}

df = pd.DataFrame(data)

app = dash.Dash(__name__)  

colors = {'Voltage': 'royalblue', 'Current': 'orange', 'Power': 'green', 'Energy': 'purple'}

app.layout = html.Div([
    html.H1("Energy Meter Dashboard", style={'text-align': 'center', 'color': 'whitesmoke',
                                             'backgroundColor': 'royalblue', 'padding': '10px'}),
    html.Div([
        html.Div([
            html.H3("Instantaneous Readings", style={'text-align': 'center'}),
            html.Div(id='instant-readings-container', style={'padding': '10px', 'border': 'thin lightgrey solid'}),
        ], style={'width': '45%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Parameter Selection", style={'text-align': 'center'}),
            dcc.Dropdown(
                id='parameter-dropdown-1',
                options=[{'label': param, 'value': param} for param in df['PARAMETER']],
                value=df['PARAMETER'].iloc[0]
            ),
            dcc.Dropdown(
                id='parameter-dropdown-2',
                options=[{'label': param, 'value': param} for param in df['PARAMETER']],
                value=df['PARAMETER'].iloc[1]
            ), 
        ], style={'width': '45%', 'display': 'inline-block'}),
    ], style={'background-color': 'whitesmoke', 'padding': '10px'}),
    html.Div([
        dcc.Graph(id='graph1')
    ], style={'width': '100%', 'display': 'inline-block', 'margin-top': '20px'}),
    html.Div([
        html.Div([
            html.H3("Time Series", style={'text-align': 'center'}),
            dcc.Dropdown(
                id='parameter-dropdown-3',
                options=[{'label': param, 'value': param} for param in df['PARAMETER']],
                value=df['PARAMETER'].iloc[0]
            ),
        ], style={'width': '45%', 'display': 'inline-block'}),
        dcc.Graph(id='graph2')
    ], style={'width': '55%', 'display': 'inline-block', 'margin-top': '20px'})
])

def format_readings(data):
    cards = []
    for parameter, value in data.items():
        cards.append(
            html.Div([
                html.H5(parameter, style={'color': colors[parameter]}),
                html.P(f"{value:.2f}", style={'font-size': '24px'}),
            ], style={'padding': '10px', 'border': 'thin lightgrey solid', 'margin-bottom': '10px'})
        )
    return cards

@app.callback(
    [Output('instant-readings-container', 'children'),
     Output('graph1', 'figure')],
    [Input('parameter-dropdown-1', 'value'),
     Input('parameter-dropdown-2', 'value')]
)
def update_instant_readings_and_bar_graph(param1, param2):
    selected_data = df[df['PARAMETER'].isin([param1, param2])]
    readings_cards = format_readings(selected_data.set_index('PARAMETER')['VALUE'].to_dict())
    fig = px.bar(selected_data, x='PARAMETER', y='VALUE', text='VALUE', color='PARAMETER',
                 title="Instantaneous Readings", labels={'PARAMETER': 'Parameter', 'VALUE': 'Value'})
    return readings_cards, fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('parameter-dropdown-3', 'value')]
)
def update_time_series_graph(param):
    fig = px.line(df[df['PARAMETER'] == param], x='DATE', y='VALUE', title=f"{param} Time Series",
                  labels={'DATE': 'Date', 'VALUE': 'Value'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)