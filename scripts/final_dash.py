import pandas as pd
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

cases = pd.read_csv("E:/uni/Data_Science_E/Data_Science_Enterprise/data/final_cases.csv")

fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data

    Goal of the project is to teach data science by applying a cross industry standard process,
    it covers the full walkthrough of: automated data gathering, data transformations,
    filtering and machine learning to approximating the doubling time, and
    (static) deployment of responsive dashboard.

    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in cases['location'].unique()],
        value=['Germany','Italy'], # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select other graphs
        '''),


    dcc.Dropdown(
    id='daily_stats',
    options=[
        {'label': 'Daily New Cases', 'value': 'new_cases_smoothed'},
        {'label': 'Daily New Deaths', 'value': 'new_deaths_smoothed'},
        {'label': 'Total Cases', 'value': 'total_cases'},
        {'label': 'Total Deaths', 'value': 'total_deaths'},
    ],
    value='new_cases_smoothed',
    multi=False
    ), 

    dcc.Graph(figure=fig, id='main_window_slope')
])



@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('daily_stats', 'value')])

def update_figure(country_list,show_stats):

    traces = []
    for each in country_list:

        df_plot=cases[cases['location']==each]


        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_stats],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      }
        )
    }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)
