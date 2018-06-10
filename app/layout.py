import dash_core_components as dcc
import dash_html_components as html

from app import POOL_RANGE, NODES_RANGE, NODES_RANGE2, KEYS_RANGE, DIMENSION_RANGE, RANGE_RANGE


def slider(name, marks_range, id, linear=False):
    return html.Div([
        html.Label(name, htmlFor=id),
        dcc.Slider(
            min=marks_range[0],
            max=marks_range[1],
            marks={i: str(i) for i in range(marks_range[0], marks_range[1] + 1, 10)} if linear
            else {i: str(2 ** i) for i in range(marks_range[0], marks_range[1] + 1)},
            value=marks_range[2],
            id=id
        ),
        html.Br(),
    ])


layout = html.Div([
    html.H1("Sensor Network"),

    html.H2("Coverage"),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Coverage by nodes amount in [{}, {}]".format(NODES_RANGE[0], NODES_RANGE[1])),
                slider("Pool size:", POOL_RANGE, 'nodes-pool-slider'),
                slider("Keys per node:", KEYS_RANGE, 'nodes-key-slider'),
                slider("Grid side length:", DIMENSION_RANGE, 'nodes-dim-slider', linear=True),
                slider("Signal range:", RANGE_RANGE, 'nodes-range-slider', linear=True),
                html.Button("Generate", id='nodes-button', className='button-primary', style={'width': '100%'}),
                dcc.Graph(id='nodes-graph')
            ], id='nodes')
        ], className='one-half column'),

        html.Div([
            html.Div([
                html.H3("Coverage by pool size in [{}, {}]".format(2**POOL_RANGE[0], 2**POOL_RANGE[1])),
                slider("Nodes amount:", NODES_RANGE, 'pool-nodes-slider', linear=True),
                slider("Keys per node:", KEYS_RANGE, 'pool-key-slider'),
                slider("Grid side length:", DIMENSION_RANGE, 'pool-dim-slider', linear=True),
                slider("Signal range:", RANGE_RANGE, 'pool-range-slider', linear=True),
                html.Button("Generate", id='pool-button', className='button-primary', style={'width': '100%'}),
                dcc.Graph(id='pool-graph')
            ], id='pool'),
        ], className='one-half column'),
    ], className='row'),

    html.H2("Network Graph"),
    html.Div([
        slider("Nodes amount:", NODES_RANGE2, 'network-nodes-slider'),
        slider("Pool size:", POOL_RANGE, 'network-pool-slider'),
        slider("Keys per node:", KEYS_RANGE, 'network-key-slider'),
        slider("Grid side length:", DIMENSION_RANGE, 'network-dim-slider', linear=True),
        slider("Signal range:", RANGE_RANGE, 'network-range-slider', linear=True),
        # html.Button("Generate", id='network-button', className='button-primary', style={'width': '100%'}),
        dcc.Graph(id='network-graph')
    ], id='pool'),

], style={'width': '80%', 'margin': 'auto'})
