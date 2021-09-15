# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', options=[
                                        {'label': 'All Sites', 'value': 'All Sites'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                    value='All Sites',
                                    placeholder='Select a Launch Site here'
                                ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0 , max=10000, step=1000, 
                                                marks={
                                                    0: {'label': '0 kg', 'style': {'color': '#77b0b1'}},
                                                    #1000: {'label': '1000 kg'},
                                                    #2000: {'label': '2000 kg'},
                                                    2500: {'label': '2500 kg'},
                                                    #3000: {'label': '3000 kg'},
                                                    #4000: {'label': '4000 kg'},
                                                    5000: {'label': '5000 kg'},
                                                    #6000: {'label': '6000 kg'},
                                                    #7000: {'label': '7000 kg'},
                                                    7500: {'label': '7500 kg'},
                                                    #8000: {'label': '8000 kg'},
                                                    #9000: {'label': '9000 kg'},
                                                    10000: {'label': '10000 kg', 'style': {'color': '#f50'}}
                                                },
                                                value=[spacex_df['Payload Mass (kg)'].min(),spacex_df['Payload Mass (kg)'].max()]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_success_pie_chart(launch_site):
    if launch_site == 'All Sites':
        df = spacex_df.copy()
        df = df.groupby(['Launch Site']).sum()
        df.reset_index(inplace=True)
        df.sort_values(['class'],ascending=False,inplace=True)
        labels = []
        values = []
        for i in range(len(df)):
            labels.append(df['Launch Site'][i])
            values.append(df['class'][i])
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Total Success Launches By Site')
    else:
        # Select data based on the entered launch site
        df =  spacex_df[spacex_df['Launch Site']==launch_site]
        success_launches = df['class'].sum()
        total_launches = df['class'].count()
        labels = ['Successful Launches','Failed Launches']
        values = [success_launches,(total_launches-success_launches)]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title='Total Success Launches for site {}'.format(launch_site))
        fig.update_traces(marker=dict(colors=['#FF6961', '#77DD77']))
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")
)
# If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class. In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
# If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show values Payload Mass (kg) and class for the selected site, and color-label the point using Boosster Version Category likewise.
def update_success_payload_scatter_chart(launch_site,slider_range):
    if launch_site == 'All Sites':
        df =  spacex_df[ (spacex_df['Payload Mass (kg)']>=slider_range[0]) & (spacex_df['Payload Mass (kg)']<=slider_range[1]) ]
        fig = px.scatter(df, x='Payload Mass (kg)',y='class',color='Booster Version Category')
        fig.update_layout(title='Correlation between Success & Payload for all Sites')
    else:
        # Select data based on the entered launch site
        df =  spacex_df[ (spacex_df['Launch Site']==launch_site) & (spacex_df['Payload Mass (kg)']>=slider_range[0]) & (spacex_df['Payload Mass (kg)']<=slider_range[1]) ]
        fig = px.scatter(df, x='Payload Mass (kg)',y='class',color='Booster Version Category')
        fig.update_layout(title='Correlation between Success & Payload for site {}'.format(launch_site))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
