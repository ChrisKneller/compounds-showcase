from dash import Dash, html, dcc, Input, Output, callback
import dash_bio as dashbio
import plotly.express as px
import pandas as pd
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
    dcc.Location(id='url', refresh=False),  # represents the browser bar
    html.H1(children="Compound explorer"),
    html.Div(id="page-content"),
    html.H2(children="Compounds summary"),

    html.Div(children="Explore the compounds data"),

    dcc.Graph(
        id="example-graph",
        figure=fig
    ),
    # html.Div([
    #     dashbio.Jsme(
    #         smiles=df["smiles"][0]
    #     )
    # ])
    html.Div(id="smiles-object"),


])


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H3(f'You are on page {pathname}')
    ])


@callback(Output('smiles-object', 'children'),
          [Input('url', 'pathname')])
def display_smiles(pathname):
    compound_id = pathname[1:]  # remove the leading / from pathname
    try:
        compound = df.loc[df["compound_id"] == int(compound_id)]
    except:
        return
    # import pdb; pdb.set_trace()
    smiles = compound["smiles"].values[0]
    return html.Div([
        dashbio.Jsme(
            smiles=smiles
        )
    ])


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    app.run_server(debug=True)
