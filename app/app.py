from app.layout import layout
from app import app

app.layout = layout

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

from app.callbacks import *

server = app.server
