# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options = {'label', 'All Sites', 'value', 'ALL'},
                                            value = 'ALL',
                                            placeholder = 'Select a Launch Site here',
                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    marks = {2500: {'label' : '2500'},
                                             5000: {'label' : '5000'},
                                             7500: {'label' : '7500'}},
                                    value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdown', component_property = 'value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        df_new = spacex_df.groupby(['Launch Site'])['class'].sum().to_frame()
        df_new = df_new.reset_index()
        fig = px.pie(df_new, 
            values = 'class',
            names = 'Launch Site',
            title = 'total Success Launches by Launch Site')
        return fig
    else:
        df_new = spacex_df[spacex_df['Launch Site'] == entered_site]['class'].value_counts().to_frame()
        df_new['name'] = ['Failure', 'Success']
        fig = px.pie(df_new,
            values = 'class',
            names = 'name',
            title = 'Total Success Launcher for ' + entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
              Input(component_id = 'site-dropdownn', component_property = 'value'),
              Input(component_id = 'payload-slider', component_property = 'value'))

def scatter(i1, i2):
    if i1 == 'ALL':
        df_new = spacex_df[spacex_df['Payload Mass (kg)'] >= i2[0]]
        df_new2 = df_new[df_new['Payload Mass (kg)'] <= i2[1]]
        scatterfig = px.scatter(df_new2,
                                x = 'Payload Mass (kg)',
                                y = 'class',
                                color = 'Booster Version Category')
    else:
        df_new = spacex_df[spacex_df['Launch Site'] == i1]
        df_new_i = df_new[df_new['Payload Mass (kg)'] >= i2[0]]
        df_new_j = df_new_i[df_new_i['Payload Mass (kg)'] <= i2[1]]
        scatterfig = px.scatter(df_new_j,
                                x = 'Payload Mass(kg)',
                                y = 'class',
                                color = 'Booster Version Category')
    return scatterfig


# Run the app
if __name__ == '__main__':
    app.run_server()
