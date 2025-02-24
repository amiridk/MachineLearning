import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np


np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100)
})


app = dash.Dash(__name__)


app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("Data Visualization Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div(style={'marginBottom': '20px'}, children=[
        html.P(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            style={'fontSize': '16px', 'color': '#34495e'}
        ),
        html.P(
            "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            style={'fontSize': '16px', 'color': '#34495e'}
        ),
    ]),
    
    dcc.Graph(id='histogram', style={'marginBottom': '20px'}),
    dcc.Graph(id='scatter-plot', style={'marginBottom': '20px'}),
    
    html.Label("Select Range for X-axis:", style={'fontSize': '18px', 'color': '#2c3e50'}),
    dcc.RangeSlider(
        id='range-slider',
        min=-3,
        max=3,
        step=0.1,
        marks={i: str(i) for i in range(-3, 4)},
        value=[-1, 1],
        tooltip={'placement': 'bottom', 'always_visible': True}
    ),
    
    html.Div(style={'marginTop': '30px'}, children=[
        html.H3("Filtered Data Table", style={'color': '#2c3e50'}),
        dash_table.DataTable(
            id='data-table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto', 'marginBottom': '20px'},
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'backgroundColor': '#f9f9f9',
                'color': '#2c3e50',
                'padding': '10px',
                'textAlign': 'left'
            }
        )
    ])
])

# Callback to update the plots and table based on the range slider or scatter plot selection
@app.callback(
    [Output('histogram', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('data-table', 'data')],
    [Input('range-slider', 'value'),
     Input('scatter-plot', 'selectedData')],
    [State('scatter-plot', 'figure')]
)
def update_plots(selected_range, selected_data, scatter_figure):

    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'range-slider':

        filtered_df = df[(df['x'] >= selected_range[0]) & (df['x'] <= selected_range[1])]
    elif triggered_id == 'scatter-plot' and selected_data:

        selected_points = selected_data['points']
        selected_indices = [point['pointIndex'] for point in selected_points]
        filtered_df = df.iloc[selected_indices]
    else:

        filtered_df = df


    hist_fig = px.histogram(filtered_df, x='x', nbins=20, title='Histogram of x')
    hist_fig.update_layout(
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        font={'color': '#2c3e50'}
    )
    

    scatter_fig = px.scatter(filtered_df, x='x', y='y', title='Scatter Plot of x vs y')
    scatter_fig.update_layout(
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        font={'color': '#2c3e50'}
    )
    

    table_data = filtered_df.to_dict('records')
    
    return hist_fig, scatter_fig, table_data


if __name__ == '__main__':
    app.run_server(debug=True)