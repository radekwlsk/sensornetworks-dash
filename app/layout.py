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
    html.Header([
        html.H1("Wireless Sensor Network"),
    ], style={'textAlign': 'center', 'padding': '50px 0'}),

    html.Div([
        html.Div([
            html.H2("Wireless sensor network"),
            dcc.Markdown(["""Created by a group of sensors (*nodes*) scattered across vast area that monitor and 
collect environment data over extended periods of time the **wireless sensor networks** are very limited in resources. 
Main characteristics of such networks are:

  - power consumption constraint (battery supplied, passive energy harvesting),
  - nodes failures resilience (must operate even when fraction of nodes fail),
  - limited computational power (strong, hard cryptography protocols are not available),
  - limited memory (can not store or process lot of big variables),
  - unattended operation without network infrastructure (all nodes are the same and have to establish connection on 
their own once deployed in random places over the area).

Given those limitations it is still critical to provide security of processed and transmitted data. As authentication 
protocols used in large networks (like WiFi, LTE) are based on hard computational problems they are not suitable for 
wireless sensor networks.

Easiest way to encrypt and authenticate the communication between the nodes of such network is to store single shared 
private key. But such approach compromises entire network on breach of single node's secret. To tackle this problem 
various protocols were proposed, one of them being *A Key-Management Scheme for Distributed Sensor Networks* proposed 
by **Laurent Eschenauer** and **Virgil D. Gligor** that allows increased security without sacrificing a lot of memory 
and requiring little computational power."""
            ]),

            html.Hr(),

            html.H2("Key Distribution algorithm by L. Eschenauer and V. D. Gligor"),
            dcc.Markdown(["""As described in [A Key-Management Scheme for Distributed Sensor Networks]({}) (Chapter 2) 
a 3-step approach can be used for key distribution:

  1. Key pre-distribution:
    - key pool *P* generation,
    - random drawing of *k* keys out of *P* without replacement at random for each node,
    - loading of the selected keys to each node's memory.
  2. Shared-key discovery:
    - after nodes deployment,
    - each node broadcasts its keys to find all nodes in range that it shares at least one key with creating *link*,
    - network topology is established after that step.
  3. Path-key establishment:
    - assigns *path-key* to node pairs that do not share a key but are connected by two or more links after shared-key 
  discovery phase.""".format("https://people.eecs.berkeley.edu/~dawnsong/papers/key-dist.pdf")]),

            html.Hr(),

            html.H2("Key Distribution Simulation"),
            dcc.Markdown(["""This application allows for simulating first 2 phases of the algorithm, giving information 
about direct links coverage, total coverage and number of components in a wireless sensor network that adopts this 
approach. Parameters of the network are:

  - *n*: number of nodes (size of the network),
  - *s*: size of key pool *P*,
  - *k*: number of randomly selected keys from the key pool *P* stored in each node,
  - *x*: dimension of a grid on which it is deployed,
  - *r*: transmission range of each node (calculated in Manhattan distance).
  
Each parameter changes the network's security and topology, the goal is to provide best key protection, lowest 
requirements with highest total network coverage. 

To see how change of each parameter affects the coverage one can use provided plots generators in 
[**Coverage** section](#coverage) and find details about their impact on security. 

A network topology using such key distribution protocol can be simulated in [**Network Graph** section](#network)."""]),

        ], style={'maxWidth': '100%', 'width': '780px', 'margin': 'auto'}),

        html.Hr(),

        html.Div([
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
                        html.P("Note: results can take significant time to generate depending on the values selected."),
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
                        html.P("Note: results can take significant time to generate depending on the values selected."),
                        dcc.Graph(id='pool-graph')
                    ], id='pool'),
                ], className='one-half column'),
            ], className='row'),
        ], id='coverage'),

        html.Hr(),

        html.Div([
            html.H2("Network Graph"),
            dcc.Markdown("""\
    The graph below updates automatically after change of the arguments with sliders below. 
    
    Right part shows the network's coverage (direct and total). 
    
    > Note that scale is not always 0-100%
    
    Nodes belonging to one component have the same colour, sometimes the nodes can overlap as their coordinates on the 
    network grid are selected at random. Links between nodes are marked as edges of the graph. 
    
    On hover over a node its details are displayed: 
    
      - unique id of the node,
      - coordinates on the grid in *(x, y)* form,
      - list of node's neighbours (as id's) if any.
    """),
            html.Div([
                slider("Nodes amount:", NODES_RANGE2, 'network-nodes-slider'),
                slider("Pool size:", POOL_RANGE, 'network-pool-slider'),
                slider("Keys per node:", KEYS_RANGE, 'network-key-slider'),
                slider("Grid side length:", DIMENSION_RANGE, 'network-dim-slider', linear=True),
                slider("Signal range:", RANGE_RANGE, 'network-range-slider', linear=True),
                # html.Button("Generate", id='network-button', className='button-primary', style={'width': '100%'}),
                dcc.Graph(id='network-graph')
            ], id='pool'),
        ], id='network'),
    ], style={'width': '80%', 'margin': 'auto'}),

    html.Hr(),

    html.Footer([
        dcc.Markdown(
            "Copyright \u00A9 2018 Radosław Kowalski | Created using [Dash](https://plot.ly/products/dash/) by Plotly"
        )
    ], style={'margin': '50px 0', 'textAlign': 'center'})
])

