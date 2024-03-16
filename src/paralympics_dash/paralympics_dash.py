""" Code as at the end of week 7 activities """
import pandas as pd
import requests
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from figures import line_chart, bar_gender, scatter_geo, event_data

external_stylesheets = [dbc.themes.BOOTSTRAP]
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Create the Plotly Express line chart object, e.g. to show number of sports
line = line_chart("sports")

# Create the Plotly Express stacked bar chart object to show gender split of participants for the type of event
bar = bar_gender("winter")

# Create the scatter map
map = scatter_geo()


# Layout variables

# the layout for the card is now generated by a function
def create_card(event_id):
    """
    Generate a card for the event specified by event_id.

    Uses the REST API route.

    Args:
        event_id:

    Returns:
        card: dash boostrap components card for the event
    """
    # Use python requests to access your REST API on your localhost
    # Make sure you run the REST APP first and check your port number if you changed it from the default 5000
    url = f"http://127.0.0.1:5000/events/{event_id}"
    event_response = requests.get(url)
    ev = event_response.json()

    # Variables for the card contents
    logo = f'logos/{ev['year']}_{ev['host']}.jpg'
    dates = f'{ev['start']} to {ev['end']}'
    host = f'{ev['host']} {ev['year']}'
    highlights = f'Highlights: {ev['highlights']}'
    participants = f'{ev['participants']} athletes'
    events = f'{ev['events']} events'
    countries = f'{ev['countries']} countries'

    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4([html.Img(src=app.get_asset_url(logo), width=35, className="me-1"),
                         host]),
                html.Br(),
                html.H6(dates, className="card-subtitle"),
                html.P(highlights, className="card-text"),
                html.P(participants, className="card-text"),
                html.P(events, className="card-text"),
                html.P(countries, className="card-text"),
            ]
        ),
    ],
        style={"width": "18rem"},
    )
    return card


def create_card_from_df(event_id):
    """
    Generate a card for the event specified by event_id.

    Uses the DataFrame.

    Args:
        event_id:

    Returns:
        card: dash boostrap components card for the event
    """

    #
    df_events = pd.read_csv(event_data)
    ev = df_events.iloc[event_id - 1]

    # Variables for the card contents
    logo = f'logos/{ev['year']}_{ev['host']}.jpg'
    dates = f'{ev['start']} to {ev['end']}'
    host = f'{ev['host']} {ev['year']}'
    highlights = f'Highlights: {ev['highlights']}'
    participants = f'{ev['participants']} athletes'
    events = f'{ev['events']} events'
    countries = f'{ev['countries']} countries'

    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4([html.Img(src=app.get_asset_url(logo), width=35, className="me-1"),
                         host]),
                html.Br(),
                html.H6(dates, className="card-subtitle"),
                html.P(highlights, className="card-text"),
                html.P(participants, className="card-text"),
                html.P(events, className="card-text"),
                html.P(countries, className="card-text"),
            ]
        ),
    ],
        style={"width": "18rem"},
    )
    return card

from dash import Input, Output


@app.callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_line_chart(chart_type):
    figure = line_chart(chart_type)
    return figure


# This version requires the Flask REST app to be running
# card = create_card(12)

# This version does not require the Flask REST app to be running
card = create_card_from_df(12)

dropdown = dbc.Select(
    id="type-dropdown",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],
    id="checklist-input",
    inline=True,
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Paralympics Dashboard"), html.P(
            "Use the charts to help you answer the questions.")
                 ], width=12),
    ]),
)

row_two = dbc.Row([
    dbc.Col(children=[
        dropdown
    ], width=2),
    dbc.Col(children=[
        checklist,
    ], width={"size": 2, "offset": 4}),
], align="start")

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line", figure=line),
    ], width=6),
    dbc.Col(children=[
        dcc.Graph(id="bar", figure=bar),
        # html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid"),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
        # html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid"),
    ], width=8, align="start"),
    dbc.Col(children=[
        html.Br(),
        card,
    ], width=4, align="start"),
])

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
    # Runs on port 8050 by default, this just shows the parameter to use to change to another port if needed
