import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


from models import *

df = pd.DataFrame({'date':['2021-12-01 14:00:0', '2021-12-02 18:00:0', '2021-12-03 7:00:0', '2021-12-04 1:00:0'],'sales':[100,121,125,142]})

print(df)
# exit()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in df.columns[1:]],
        value=df.columns[1],
        clearable=False,
    ),
    dcc.Graph(id="time-series-chart"),
])

@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(df, x='date', y=ticker)
    return fig

app.run_server(debug=True)