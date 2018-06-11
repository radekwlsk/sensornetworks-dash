import dash_core_components as dcc
import dash_html_components as html

from app import POOL_RANGE, NODES_RANGE, NODES_RANGE2, KEYS_RANGE, DIMENSION_RANGE, RANGE_RANGE
from app import strings


def slider(name, marks_range, id, linear=False):
    step = 10
    if linear and marks_range[1] - marks_range[0] > 200:
        step = 50
    return html.Div([
        html.Label(name, htmlFor=id),
        dcc.Slider(
            min=marks_range[0],
            max=marks_range[1],
            marks={i: str(i) for i in range(marks_range[0], marks_range[1] + 1, step)} if linear
            else {i: str(2 ** i) for i in range(marks_range[0], marks_range[1] + 1)},
            value=marks_range[2],
            id=id
        ),
        html.Br(),
    ])


layout = html.Div([
    html.Header([
        html.H1("Wireless Sensor Network"),
    ], style={'textAlign': 'center', 'padding': '50px 0'}),

    html.Div([
        html.Div([
            html.H2("Wireless sensor network"),
            dcc.Markdown(strings.WIRELESS_SENSOR_NETWORK),

            html.Hr(),

            html.H2("Key Distribution algorithm by L. Eschenauer and V. D. Gligor"),
            dcc.Markdown(strings.ALGORITHM),

            html.Hr(),

            html.H2("Key Distribution Simulation"),
            dcc.Markdown(strings.SIMULATION),

        ], style={'maxWidth': '100%', 'width': '780px', 'margin': 'auto'}),

        html.Hr(),

        html.Div([
            html.H2("Coverage"),
            dcc.Markdown(strings.COVERAGE),
            html.Div([
                html.H3("Coverage by keys stored"),
                dcc.Markdown(strings.KEYS),
                slider("Nodes amount:", NODES_RANGE, 'keys-nodes-slider', linear=True),
                slider("Pool size:", POOL_RANGE, 'keys-pool-slider'),
                slider("Grid side length:", DIMENSION_RANGE, 'keys-dim-slider', linear=True),
                slider("Signal range:", RANGE_RANGE, 'keys-range-slider', linear=True),
                html.Button("Generate", id='keys-button', className='button-primary', style={'width': '100%'}),
                html.P("Note: results can take significant time to generate depending on the values selected."),
                dcc.Graph(id='keys-graph')
            ], id='keys'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Coverage by pool size"),
                        dcc.Markdown(strings.POOL),
                        slider("Nodes amount:", NODES_RANGE, 'pool-nodes-slider', linear=True),
                        slider("Keys per node:", KEYS_RANGE, 'pool-key-slider'),
                        slider("Grid side length:", DIMENSION_RANGE, 'pool-dim-slider', linear=True),
                        slider("Signal range:", RANGE_RANGE, 'pool-range-slider', linear=True),
                        html.Button("Generate", id='pool-button', className='button-primary', style={'width': '100%'}),
                        html.P("Note: results can take significant time to generate depending on the values selected."),
                        dcc.Graph(id='pool-graph')
                    ], id='pool'),

                    html.Div([
                        html.H3("Coverage by grid dimension"),
                        dcc.Markdown(strings.DIM),
                        slider("Nodes amount:", NODES_RANGE, 'dim-nodes-slider', linear=True),
                        slider("Pool size:", POOL_RANGE, 'dim-pool-slider'),
                        slider("Keys per node:", KEYS_RANGE, 'dim-key-slider'),
                        slider("Signal range:", RANGE_RANGE, 'dim-range-slider', linear=True),
                        html.Button("Generate", id='dim-button', className='button-primary', style={'width': '100%'}),
                        html.P("Note: results can take significant time to generate depending on the values selected."),
                        dcc.Graph(id='dim-graph')
                    ], id='dim'),
                ], className='one-half column'),

                html.Div([
                    html.Div([
                        html.H3("Coverage by nodes amount"),
                        dcc.Markdown(strings.NODES),
                        slider("Pool size:", POOL_RANGE, 'nodes-pool-slider'),
                        slider("Keys per node:", KEYS_RANGE, 'nodes-key-slider'),
                        slider("Grid side length:", DIMENSION_RANGE, 'nodes-dim-slider', linear=True),
                        slider("Signal range:", RANGE_RANGE, 'nodes-range-slider', linear=True),
                        html.Button("Generate", id='nodes-button', className='button-primary', style={'width': '100%'}),
                        html.P("Note: results can take significant time to generate depending on the values selected."),
                        dcc.Graph(id='nodes-graph')
                    ], id='nodes'),

                    html.Div([
                        html.H3("Coverage by transmission range"),
                        dcc.Markdown(strings.RANGE),
                        slider("Nodes amount:", NODES_RANGE, 'range-nodes-slider', linear=True),
                        slider("Pool size:", POOL_RANGE, 'range-pool-slider'),
                        slider("Keys per node:", KEYS_RANGE, 'range-key-slider'),
                        slider("Grid side length:", DIMENSION_RANGE, 'range-dim-slider', linear=True),
                        html.Button("Generate", id='range-button', className='button-primary', style={'width': '100%'}),
                        html.P("Note: results can take significant time to generate depending on the values selected."),
                        dcc.Graph(id='range-graph')
                    ], id='range'),
                ], className='one-half column'),
            ], className='row'),
        ], id='coverage'),

        html.Hr(),

        html.Div([
            html.H2("Network Graph"),
            dcc.Markdown(strings.NETWORK),
            html.Div([
                slider("Nodes amount:", NODES_RANGE2, 'network-nodes-slider', linear=True),
                slider("Pool size:", POOL_RANGE, 'network-pool-slider'),
                slider("Keys per node:", KEYS_RANGE, 'network-key-slider'),
                slider("Grid side length:", DIMENSION_RANGE, 'network-dim-slider', linear=True),
                slider("Signal range:", RANGE_RANGE, 'network-range-slider', linear=True),
                # html.Button("Generate", id='network-button', className='button-primary', style={'width': '100%'}),
                dcc.Graph(id='network-graph')
            ]),
        ], id='network'),
    ], style={'width': '80%', 'margin': 'auto'}),

    html.Hr(),

    html.Footer([
        dcc.Markdown(
            "Copyright \u00A9 2018 Radosław Kowalski | Created using [Dash](https://plot.ly/products/dash/) by Plotly"
        )
    ], style={'margin': '50px 0', 'textAlign': 'center'})
])

