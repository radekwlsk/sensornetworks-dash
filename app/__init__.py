import dash
from flask_caching import Cache

app = dash.Dash(name='sensornetworks-dash')
app.title = 'Wireless Sensor Networks'

cache = Cache(app.server, config={
    'CACHE_TYPE':      'filesystem',
    'CACHE_DIR':      'cache',
    'CACHE_THRESHOLD': 256,
    'CACHE_DEFAULT_TIMEOUT': 60*60*24,
})

NODES_RANGE = (10, 150, 100)
NODES_RANGE2 = (50, 800, 100)
POOL_RANGE = (10, 20, 10)
KEYS_RANGE = (1, 15, 5)
DIMENSION_RANGE = (10, 100, 50)
RANGE_RANGE = (0, 100, 10)
