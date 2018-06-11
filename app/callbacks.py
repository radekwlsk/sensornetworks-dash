import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from statistics import harmonic_mean

from app import NODES_RANGE, app, POOL_RANGE, KEYS_RANGE, DIMENSION_RANGE, RANGE_RANGE, cache
from sensnet_key_dist.network import SensorNetwork


AVERAGE_OF = 10


def get_figure(x_range, direct_coverage, coverage, components):
    dir_cov_trace = go.Scatter(
        x=x_range,
        y=direct_coverage,
        mode='lines',
        name='direct cov.',
        line=dict(shape='spline',
                  smoothing=1.1)
    )
    cov_trace = go.Scatter(
        x=x_range,
        y=coverage,
        mode='lines',
        name='total cov.',
        yaxis='y2',
        line=dict(shape='spline',
                  smoothing=1.1)
    )
    comp_trace = go.Scatter(
        x=x_range,
        y=components,
        mode='lines',
        name='components',
        yaxis='y3',
        xaxis='x2',
        line=dict(shape='spline',
                  smoothing=1.1)
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
        height=480
    ))


@cache.memoize(timeout=None)
def generate_nodes(p, k, x, r):
    nodes_range = [i for i in range(NODES_RANGE[0], NODES_RANGE[1] + 1, 10)]
    direct_coverage = list()
    coverage = list()
    components = list()
    for i, n in enumerate(nodes_range):
        dir_cov = list()
        cov = list()
        comp = list()
        for _ in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov.append(network.direct_coverage)
            cov.append(network.coverage)
            comp.append(len(network.components))
        direct_coverage.append(harmonic_mean(dir_cov))
        coverage.append(harmonic_mean(cov))
        components.append(harmonic_mean(comp))
        if i >= 4 and coverage[i - 1] >= 0.99:
            nodes_range = nodes_range[:i + 1]
            break
    return nodes_range, direct_coverage, coverage, components


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
    nodes_range, direct_coverage, coverage, components = generate_nodes(p, k, x, r)
    return get_figure(nodes_range, direct_coverage, coverage, components)


@cache.memoize(timeout=None)
def generate_pool(n, k, x, r):
    pool_range = [2 ** i for i in range(POOL_RANGE[0], POOL_RANGE[1] + 1) if 2 ** i >= k]
    direct_coverage = list()
    coverage = list()
    components = list()
    for i, p in enumerate(pool_range):
        dir_cov = list()
        cov = list()
        comp = list()
        for _ in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov.append(network.direct_coverage)
            cov.append(network.coverage)
            comp.append(len(network.components))
        direct_coverage.append(harmonic_mean(dir_cov))
        coverage.append(harmonic_mean(cov))
        components.append(harmonic_mean(comp))
        if i >= 4 and coverage[i - 1] <= 0.1:
            pool_range = pool_range[:i + 1]
            break
    return pool_range, direct_coverage, coverage, components


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
    pool_range, direct_coverage, coverage, components = generate_pool(n, k, x, r)
    return get_figure(pool_range, direct_coverage, coverage, components)


@cache.memoize(timeout=None)
def generate_keys(n, p, x, r):
    # keys_range = [2 ** KEYS_RANGE[0], 2 * 2 ** KEYS_RANGE[0]]
    # while keys_range[-1] < p:
    #     k = keys_range[-1] + keys_range[-2]
    #     if k <= p:
    #         keys_range.append(keys_range[-1] + keys_range[-2])
    #     else:
    #         break
    keys_range = [i for i in range(2 ** KEYS_RANGE[0], (2 ** KEYS_RANGE[1]) + 1, 4) if i <= p]
    direct_coverage = list()
    coverage = list()
    components = list()
    for i, k in enumerate(keys_range):
        dir_cov = list()
        cov = list()
        comp = list()
        for _ in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov.append(network.direct_coverage)
            cov.append(network.coverage)
            comp.append(len(network.components))
        direct_coverage.append(harmonic_mean(dir_cov))
        coverage.append(harmonic_mean(cov))
        components.append(harmonic_mean(comp))
        if i >= 4 and coverage[i - 1] >= 0.99:
            keys_range = keys_range[:i + 1]
            break
    return keys_range, direct_coverage, coverage, components


@app.callback(Output('keys-graph', 'figure'),
              [Input('keys-button', 'n_clicks')],
              state=[State('keys-nodes-slider', 'value'),
                     State('keys-pool-slider', 'value'),
                     State('keys-dim-slider', 'value'),
                     State('keys-range-slider', 'value')])
def generate_keys_graph(clicks, n, p, x, r):
    if not clicks:
        raise PreventUpdate()
    p = 2 ** p
    keys_range, direct_coverage, coverage, components = generate_keys(n, p, x, r)
    return get_figure(keys_range, direct_coverage, coverage, components)


@cache.memoize(timeout=None)
def generate_dim(n, p, k, r):
    dim_range = [i for i in range(DIMENSION_RANGE[0], DIMENSION_RANGE[1] + 1, 10) if i >= r]
    direct_coverage = list()
    coverage = list()
    components = list()
    for i, x in enumerate(dim_range):
        dir_cov = list()
        cov = list()
        comp = list()
        for _ in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov.append(network.direct_coverage)
            cov.append(network.coverage)
            comp.append(len(network.components))
        direct_coverage.append(harmonic_mean(dir_cov))
        coverage.append(harmonic_mean(cov))
        components.append(harmonic_mean(comp))
        if i >= 4 and coverage[i - 1] <= 0.01:
            dim_range = dim_range[:i + 1]
            break
    return dim_range, direct_coverage, coverage, components


@app.callback(Output('dim-graph', 'figure'),
              [Input('dim-button', 'n_clicks')],
              state=[State('dim-nodes-slider', 'value'),
                     State('dim-pool-slider', 'value'),
                     State('dim-key-slider', 'value'),
                     State('dim-range-slider', 'value')])
def generate_dim_graph(clicks, n, p, k, r):
    if not clicks:
        raise PreventUpdate()
    dim_range, direct_coverage, coverage, components = generate_dim(n, p, k, r)
    return get_figure(dim_range, direct_coverage, coverage, components)


@cache.memoize(timeout=None)
def generate_range(n, k, p, x):
    range_range = [i for i in range(RANGE_RANGE[0], RANGE_RANGE[1] + 1, 2) if i <= x]
    direct_coverage = list()
    coverage = list()
    components = list()
    for i, r in enumerate(range_range):
        dir_cov = list()
        cov = list()
        comp = list()
        for _ in range(AVERAGE_OF):
            network = SensorNetwork(n, k, p, x, r)
            dir_cov.append(network.direct_coverage)
            cov.append(network.coverage)
            comp.append(len(network.components))
        direct_coverage.append(harmonic_mean(dir_cov))
        coverage.append(harmonic_mean(cov))
        components.append(harmonic_mean(comp))
        if i >= 4 and coverage[i - 1] >= 0.99:
            range_range = range_range[:i + 1]
            break

    return range_range, direct_coverage, coverage, components


@app.callback(Output('range-graph', 'figure'),
              [Input('range-button', 'n_clicks')],
              state=[State('range-nodes-slider', 'value'),
                     State('range-pool-slider', 'value'),
                     State('range-key-slider', 'value'),
                     State('range-dim-slider', 'value')])
def generate_range_graph(clicks, n, p, k, x):
    if not clicks:
        raise PreventUpdate()
    range_range, direct_coverage, coverage, components = generate_range(n, k, p, x)
    return get_figure(range_range, direct_coverage, coverage, components)


@app.callback(Output('network-graph', 'figure'),
              [Input('network-nodes-slider', 'value'),
               Input('network-pool-slider', 'value'),
               Input('network-key-slider', 'value'),
               Input('network-dim-slider', 'value'),
               Input('network-range-slider', 'value')])
def generate_network_graph(n, p, k, x, r):
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
        height=720,
    ))
