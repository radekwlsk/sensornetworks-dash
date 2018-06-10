import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import NODES_RANGE, app, POOL_RANGE
from sensnet_key_dist.network import SensorNetwork


AVERAGE_OF = 10


def get_figure(x_range, direct_coverage, coverage, components):
    dir_cov_trace = go.Scatter(
        x=x_range,
        y=direct_coverage,
        mode='lines',
        name='direct cov.'
    )
    cov_trace = go.Scatter(
        x=x_range,
        y=coverage,
        mode='lines',
        name='total cov.',
        yaxis='y2'
    )
    comp_trace = go.Scatter(
        x=x_range,
        y=components,
        mode='lines',
        name='components',
        yaxis='y3',
        xaxis='x2'
    )

    data = [dir_cov_trace, cov_trace, comp_trace]

    return go.Figure(data=data, layout=go.Layout(
        hovermode='closest',
        legend=dict(orientation="h"),
        yaxis=dict(
            title='direct coverage',
            domain=[0, 0.65],
            anchor='x'
        ),
        yaxis2=dict(
            title='total coverage',
            overlaying='y',
            side='right',
            anchor='x'
        ),
        yaxis3=dict(
            title='components',
            domain=[0.7, 1],
            anchor='x2'
        ),
        margin=dict(l=50, b=10, t=10, r=50),
        height=500
    ))


@app.callback(Output('nodes-graph', 'figure'),
              [Input('nodes-button', 'n_clicks')],
              state=[State('nodes-pool-slider', 'value'),
                     State('nodes-key-slider', 'value'),
                     State('nodes-dim-slider', 'value'),
                     State('nodes-range-slider', 'value')])
def generate_nodes_graph(clicks, p, k, x, r):
    if not clicks:
        raise PreventUpdate()

    p = 2 ** p
    k = 2 ** k

    nodes_range = [i for i in range(NODES_RANGE[0], NODES_RANGE[1]+1, 10)]
    direct_coverage = list()
    coverage = list()
    components = list()
    for n in nodes_range:
        print(f"starting n={n}")
        dir_cov = 0.0
        cov = 0.0
        comp = 0.0
        for i in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov += network.direct_coverage
            cov += network.coverage
            comp += len(network.components)
        direct_coverage.append(dir_cov / AVERAGE_OF)
        coverage.append(cov / AVERAGE_OF)
        components.append(comp / AVERAGE_OF)

    return get_figure(nodes_range, direct_coverage, coverage, components)


@app.callback(Output('pool-graph', 'figure'),
              [Input('pool-button', 'n_clicks')],
              state=[State('pool-nodes-slider', 'value'),
                     State('pool-key-slider', 'value'),
                     State('pool-dim-slider', 'value'),
                     State('pool-range-slider', 'value')])
def generate_pool_graph(clicks, n, k, x, r):
    if not clicks:
        raise PreventUpdate()

    k = 2 ** k

    pool_range = [2**i for i in range(POOL_RANGE[0], POOL_RANGE[1] + 1) if 2**i >= k]
    direct_coverage = list()
    coverage = list()
    components = list()
    for p in pool_range:
        print(f"starting p={p}")
        dir_cov = 0.0
        cov = 0.0
        comp = 0.0
        for i in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov += network.direct_coverage
            cov += network.coverage
            comp += len(network.components)
        direct_coverage.append(dir_cov / AVERAGE_OF)
        coverage.append(cov / AVERAGE_OF)
        components.append(comp / AVERAGE_OF)

    return get_figure(pool_range, direct_coverage, coverage, components)


@app.callback(Output('network-graph', 'figure'),
              [Input('network-nodes-slider', 'value'),
               Input('network-pool-slider', 'value'),
               Input('network-key-slider', 'value'),
               Input('network-dim-slider', 'value'),
               Input('network-range-slider', 'value')])
def generate_network_graph(n, p, k, x, r):
    n = 2 ** n
    p = 2 ** p
    k = 2 ** k
    network = SensorNetwork(n, k, p, x, r)
    network.create_graph()
    network.graph['data'].append(go.Bar(
        x=['direct cov.', 'total cov.'],
        y=[network.direct_coverage, network.coverage],
        text=['{:.2%}'.format(network.direct_coverage), '{:.2%}'.format(network.coverage)],
        hoverinfo='text',
        xaxis='x2',
        yaxis='y2'
    ))

    return go.Figure(data=network.graph['data'], layout=go.Layout(
        hovermode='closest',
        showlegend=False,
        xaxis=dict(
            domain=[0, 0.8],
            zeroline=False
        ),
        yaxis=dict(zeroline=False),
        xaxis2=dict(
            domain=[0.85, 1]
        ),
        yaxis2=dict(
            side='right',
            anchor='x2'
        ),
        margin=dict(l=30, b=30, t=30, r=30),
        height=900,
    ))
