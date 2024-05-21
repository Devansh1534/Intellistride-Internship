import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import mysql.connector
from datetime import datetime, timedelta

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
                options=[
                    {'label': 'Voltage', 'value': 'Voltage'},
                    {'label': 'Current', 'value': 'Current'},
                    {'label': 'Power', 'value': 'Power'},
                    {'label': 'Energy', 'value': 'Energy'}
                ],
                value='Voltage'
                
            ),
            dcc.Dropdown(
                id='parameter-dropdown-2',
                options=[
                    {'label': 'Voltage', 'value': 'Voltage'},
                    {'label': 'Current', 'value': 'Current'},
                    {'label': 'Power', 'value': 'Power'},
                    {'label': 'Energy', 'value': 'Energy'}
                ],
                value='Current'
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
                options=[
                    {'label': 'Voltage', 'value': 'Voltage'},
                    {'label': 'Current', 'value': 'Current'},
                    {'label': 'Power', 'value': 'Power'},
                    {'label': 'Energy', 'value': 'Energy'}
                ],
                value='Voltage'
            ),
        ], style={'width': '45%', 'display': 'inline-block'}),
        dcc.Graph(id='graph2')
    ], style={'width': '55%', 'display': 'inline-block', 'margin-top': '20px'}),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,
        n_intervals=0
    )
])

def fetch_latest_data():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="mydb"
    )
    query = """
    SELECT voltage, current, power, energy, event_timestamp
    FROM energydata
    WHERE event_timestamp > %s
    ORDER BY event_timestamp DESC
    """
    last_minute = datetime.now() - timedelta(minutes=1)
    df = pd.read_sql(query, mydb, params=(last_minute,))
    mydb.close()
    return df

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
     Input('parameter-dropdown-2', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_instant_readings_and_bar_graph(param1, param2, n_intervals):
    df = fetch_latest_data()
    if df.empty:
        return html.Div(), px.bar(title="No Data Available")
    
    selected_data = df[df['event_timestamp'] == df['event_timestamp'].max()]
    readings_cards = format_readings(selected_data.set_index('event_timestamp').iloc[0].to_dict())
    fig = px.bar(selected_data.melt(id_vars=['event_timestamp'], value_vars=[param1, param2]), 
                 x='variable', y='value', text='value', color='variable',
                 title="Instantaneous Readings", labels={'variable': 'Parameter', 'value': 'Value'})
    return readings_cards, fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('parameter-dropdown-3', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_time_series_graph(param, n_intervals):
    df = fetch_latest_data()
    if df.empty:
        return px.line(title="No Data Available")
    
    fig = px.line(df, x='event_timestamp', y=param.lower(), title=f"{param} Time Series",
                  labels={'event_timestamp': 'Date', param.lower(): 'Value'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)