from re import split
from dash import Dash, html, dcc, Input, Output, callback
import dash_bio as dashbio
import plotly.express as px
import pandas as pd
import re
import warnings

import getter

# Get rid of warnings that aren't helpful
warnings.simplefilter(action="ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None

app = Dash(__name__)

# Get compounds data from our API & put it in a pandas df
compounds = getter.get_compounds()
df = pd.DataFrame.from_dict(compounds)

# num_rings from int to str to get discrete rather than continuous categories
for i, nr in enumerate(df["num_rings"]):
    df["num_rings"][i] = str(nr)

# Create our plot
fig = px.scatter(
    df, x="molecular_weight", y="ALogP", color="num_rings",
    hover_data=["compound_id", "molecular_formula"], trendline="ols",
    trendline_scope="trace"
)

# Set up the page layout
app.layout = html.Div(children=[
    dcc.Location(id="url", refresh=False),  # represents the browser bar
    html.H1(children="Compound explorer"),
    html.Div(id="page-content"),
    html.H2(children="Compounds summary"),

    html.Div(children="Explore the compounds data"),

    dcc.Graph(
        id="example-graph",
        figure=fig
    ),

    html.Div(id="smiles-object"),

    html.Div(id="url-resolver")

])


@callback(Output("page-content", "children"),
          [Input("url", "pathname")])
def display_page(pathname):
    return html.Div([
        html.H3(f"You are on page {pathname}")
    ])

def display_smiles(compound_id: str):
    compound = getter.get_compound(compound_id)
    smiles = compound["smiles"]
    return html.Div([
        dashbio.Jsme(
            smiles=smiles
        )
    ])

def single_compound_page(compound_id: str):
    pass

def compounds_page():
    pass

def single_assay_page():
    pass

def assays_page():
    pass

@callback(Output("url-resolver", "children"),
          [Input("url", "pathname")])
def url_resolver(pathname):
    # Match /{first}/{second}
    matched_pattern = re.match(r"\/([a-zA-z]+)\/*(\d+)*", pathname)
    first, second = matched_pattern.groups()
    if first == "compounds":
        if second:
            return single_compound_page(second)
        return compounds_page()
    elif first == "assays":
        if second:
            return single_assay_page(second)
        return assays_page()


    return


if __name__ == "__main__":
    app.run_server(debug=True)
