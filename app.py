import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
dashboard = dash.Dash(__name__)
df = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')
df = df[['country', 'year', 'co2']]
df = df.dropna()
df['year'] = df['year'].astype(int)
dashboard.layout = html.Div(children=[
    html.H1('Global CO₂ Emissions Dashboard', style={'textAlign': 'center', 'color': '#503D36'}),
    html.Div([
        html.H2('SELECT COUNTRY', style={'margin': '2em'}),
        dcc.Dropdown(df['country'].unique(), value='United States', id='country')
    ]),
    html.Div([
        html.H2('SELECT YEAR', style={'margin-right': '2em'}),
        dcc.Dropdown(df['year'].unique(), value=2000, id='year')
    ]),
    html.Div([
        html.Div([], id='plot1'),
        html.Div([], id='plot2')
    ], style={'display': 'flex'})
])
@dashboard.callback([Output('plot1', 'children'),
                     Output('plot2', 'children')],
                    [Input('country', 'value'),
                     Input('year', 'value')])
def update_graphs(selected_country, selected_year):
    country_data = df[df['country'] == selected_country]
    year_data = country_data[country_data['year'] == selected_year]
    top_countries = df[df['year'] == selected_year].nlargest(10, 'co2')

    fig1 = px.pie(top_countries, values='co2', names='country',
                  title=f"Top 10 CO₂ Emitting Countries in {selected_year}")

    fig2 = px.line(country_data, x='year', y='co2',
                   title=f"{selected_country} CO₂ Emissions Over Time")

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)] 
if __name__ == '__main__':
    dashboard.run_server(debug=True)  
