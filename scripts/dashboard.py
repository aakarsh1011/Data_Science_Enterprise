import pandas as pd
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

def get_data(url):
    
    """
    Reads CSV data COVID-19 data of different counties from the url  
    
    INPUT: URL of the CSV
    OUTPUT: Pandas dataframe

    """
    
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    covid_data = pd.read_csv(url,sep=",")
    print(f"The number of unique countries in the data are {len(covid_data['location'].unique())}")
    
    return covid_data
    
    
def clean_data(df):
    """
    Takes in the dataframe and
    - removes unnecessary columns
    - fills the NaN values with zeroes [Assumption: NaN means there were no cases that day instead of filling it with mean values] 
    - correcting the datetime format
    
    INPUT: Pandas dataframe
    OUTPUT: Cleaned dataframe

    """
    cases = df[['date','location','new_cases_smoothed','total_cases', 'total_deaths', 'new_deaths_smoothed']]
    cases = cases.fillna(0)
    
    # converting date object into datetime
    cases["date"]= pd.to_datetime(cases["date"])
    
    # reseting the index
    cases = cases.reset_index(drop = True)
    
    loc = "E:/uni/Data_Science_E/Data_Science_Enterprise/data/final_cases.csv"
    # saving the dataset
    cases.to_csv(loc,index=False)
    
    return cases
    
    
# url from the Covid-19 data is extracted
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

covid_data = get_data(url)
cases = clean_data(covid_data)

fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data

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

    app.run_server(debug=True, use_reloader=False, port=8056)