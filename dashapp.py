from dash import Dash, html, dcc, Input, Output, callback, dash_table
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


# Set up main template page
app.layout = html.Div(
    children=[
        dcc.Location(id="url"),  # represents the browser bar
        html.H1(children="Compound explorer by Chris Kneller"),
        html.Span(
            [
                html.A("Compounds", href="/compounds"),
                " | ",
                html.A("Assays", href="/assays"),
            ]
        ),
        html.Div(id="url-resolver"),
    ]
)


def single_compound_page(compound_id: str) -> html.Div:
    """
    Given a compound id, get the compound's data from our API and construct
    an html.Div object showing interesting data on that compound.

    Args:
        compound_id (str): the compound's id e.g. 694811

    Returns:
        html.Div: a Python (dash) object to be rendered in html by the app
            engine
    """
    # Get the compound and assay results data from our API
    compound = getter.get_compound(compound_id)

    if not compound:
        return error_404()

    assays = compound["assay_results"]

    # Construct our pandas dataframe & order the columns
    df = pd.DataFrame(assays)
    df = df[["result_id", "target", "result", "operator", "value", "unit"]]

    # Create our plots/tables
    smiles_plot = dashbio.Jsme(
        smiles=compound["smiles"],
        width="100%",
        height="35vh",
    )

    # Create links for the assay IDs (markdown format)
    for i, id in enumerate(df["result_id"]):
        df["result_id"][i] = f"[{id}](/assays/{id})"

    id_col = [
        {"name": i, "id": i, "presentation": "markdown"}
        for i in df.columns
        if i == "result_id"
    ]
    cols_no_id = [{"name": i, "id": i} for i in df.columns if i != "result_id"]
    cols = id_col + cols_no_id

    assay_table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=cols,
        sort_action="native",
        sort_by=[{"column_id": "value", "direction": "desc"}],
    )

    # Put our plots in divs along with any headings or other text
    smiles_div = html.Div(
        [html.H4("Smiles plot"), html.P(compound["smiles"]), smiles_plot],
        className="content-container",
    )
    assay_table_div = html.Div(
        [html.H4("Assay results"), assay_table], className="content-container"
    )

    molecular_formula = convert_molecular_formula_to_html(
        compound["molecular_formula"]
    )

    return html.Div(
        children=[
            html.H2(children=f"Compound {compound_id}"),
            html.Div(
                [
                    html.P(["Molecular formula: ", molecular_formula]),
                    html.P(f"Molecular weight: {compound['molecular_weight']}"),  # noqa
                    html.P(f"ALogP: {compound['ALogP']}"),
                    html.P(f"Number of rings: {compound['num_rings']}"),
                ],
                className="content-container",
            ),
            smiles_div,
            assay_table_div,
        ]
    )


def compounds_page() -> html.Div:
    """
    Get all compound data from our API and construct an html.Div object showing
    interesting data regarding the compounds

    Returns:
        html.Div: a Python (dash) object to be rendered in html by the app
            engine
    """
    # Get compounds data from our API & put it in a pandas df
    compounds = getter.get_compounds()

    # Construct our pandas dataframe & order the colums
    df = pd.DataFrame.from_dict(compounds)
    df = df[
        [
            "compound_id",
            "molecular_weight",
            "ALogP",
            "molecular_formula",
            "num_rings",
            "assay_results",
        ]
    ]

    # change from int to str to get discrete rather than continuous categories
    for i, nr in enumerate(df["num_rings"]):
        df["num_rings"][i] = str(nr)

    # Display the count of assay_results as an int in the table
    for i, ar in enumerate(df["assay_results"]):
        df["assay_results"][i] = len(ar)

    # Create scatter plot
    scatter = px.scatter(
        df,
        x="molecular_weight",
        y="ALogP",
        color="num_rings",
        hover_data=["compound_id", "molecular_formula"],
        trendline="ols",
        trendline_scope="trace",
        labels={"molecular_weight": "Molecular weight", "num_rings": "Number of rings"},
        category_orders={"num_rings": ["5", "4", "3", "2", "1"]},
    )
    scatter.update_layout(
        title={
            "text": "Trends in molecular weight vs ALogP by number of rings",
            "xanchor": "center",
            "x": 0.5,
        }
    )

    # Create links for the compound IDs (markdown format)
    for i, id in enumerate(df["compound_id"]):
        df["compound_id"][i] = f"[{id}](/compounds/{id})"

    cols = [
        {"name": i, "id": i, "presentation": "markdown"} for i in df.columns
    ]

    compounds_table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=cols,
        sort_action="native",
        sort_by=[{"column_id": "value", "direction": "desc"}],
        filter_action="native",
        id="compounds-table",
    )
    compounds_table_div = html.Div(
        [html.H4("Table of compounds"), compounds_table], className="content-container"
    )

    return html.Div(
        children=[
            html.H2(children="Compounds summary"),
            dcc.Graph(id="compounds-weight-alogp-scatter", figure=scatter),
            compounds_table_div,
        ]
    )


def single_assay_page(result_id: str) -> html.Div:
    """
    Given a result_id, get the assay's data from our API and construct
    an html.Div object showing data on that assay

    Args:
        result_id (str): the compound's id e.g. 8046403

    Returns:
        html.Div: a Python (dash) object to be rendered in html by the app
            engine
    """
    # Get the compound and assay results data from our API
    assay = getter.get_assay(result_id)

    if not assay:
        return error_404()

    return html.Div(
        children=[
            html.H2(children=f"Assay {result_id}"),
            html.Div(
                [
                    html.P(f"Target: {assay['target']}"),
                    html.P(f"Result: {assay['result']}"),
                    html.P(f"Operator: {assay['operator']}"),
                    html.P(f"Value: {assay['value']}"),
                    html.P(f"Unit: {assay['unit']}"),
                ],
                className="content-container",
            ),
        ]
    )


def assays_page() -> html.Div:
    """
    Get all assay data from our API and construct an html.Div object showing
    interesting data regarding the compounds

    Returns:
        html.Div: a Python (dash) object to be rendered in html by the app
            engine
    """
    # Get compounds data from our API & put it in a pandas df
    assays = getter.get_assays()

    # Construct our pandas dataframe & order the colums
    df = pd.DataFrame.from_dict(assays)
    df = df[["result_id", "target", "result", "operator", "value", "unit"]]

    bar = px.histogram(
        df,
        x="target",
        color="target",
        pattern_shape="result",
        category_orders={
            "target": [
                "Bromodomain-containing protein 4",
                "Bromodomain-containing protein 3",
                "Bromodomain-containing protein 2",
            ]
        },
    )

    bar.update_layout(
        title={
            "text": "Occurence of assay targets and results",
            "xanchor": "center",
            "x": 0.5,
        }
    )

    # Create links for the assay IDs (markdown format)
    for i, id in enumerate(df["result_id"]):
        df["result_id"][i] = f"[{id}](/assays/{id})"

    id_col = [
        {"name": i, "id": i, "presentation": "markdown"}
        for i in df.columns
        if i == "result_id"
    ]
    cols_no_id = [{"name": i, "id": i} for i in df.columns if i != "result_id"]
    cols = id_col + cols_no_id

    assay_table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=cols,
        sort_action="native",
        sort_by=[{"column_id": "value", "direction": "desc"}],
        filter_action="native",
        id="assays-table",
    )

    assay_table_div = html.Div(
        [html.H4("Table of assays"), assay_table], className="content-container"
    )

    return html.Div(
        children=[
            html.H2(children="Assays summary"),
            dcc.Graph(id="assays-box-plot-target", figure=bar),
            assay_table_div,
        ]
    )


def error_404() -> html.P:
    """
    Return a html.P object stating that the page does not exist

    Returns:
        html.P: a Python (dash) object to be rendered in html by the app
            engine
    """
    return html.P("Page does not exist.")


@callback(Output("url-resolver", "children"), [Input("url", "pathname")])
def url_resolver(pathname: str) -> html:
    """
    Given a pathname after the url (/{first}/{second}), return a relevant html
    object

    Args:
        pathname (str): a url pathname following the url

    Returns:
        html: a Python (dash) object to be rendered in html by the app
            engine
    """
    matched_pattern = re.match(r"\/([a-zA-Z0-9]+)\/*([a-zA-Z0-9]+)*", pathname)

    if not matched_pattern:
        return
    first, second = matched_pattern.groups()

    if first in ["compound", "compounds"]:
        if second:
            return single_compound_page(second)
        return compounds_page()

    elif first in ["assay", "assays"]:
        if second:
            return single_assay_page(second)
        return assays_page()

    return error_404()


def convert_molecular_formula_to_html(molecular_formula: str) -> html.Span:
    """
    Given a molecular formula e.g. C22H22ClN5O2, convert it to an html
    representation that appropriately uses <sub></sub> around numbers

    This turns out to be a bit of a sliding window problem as we want to handle
    consecutive letters and consecutive numbers together

    Args:
        molecular_formula (str): the molecular formula to convert

    Returns:
        html.Span: an html.Span object converted to show numbers as <sub> as
            appropriate
    """
    formula_list = []
    current_string = ""
    previous = ""
    for char in molecular_formula:
        if char.isdigit():
            if previous.isdigit():
                current_string += char
            else:
                formula_list.append(current_string)
                current_string = char
            previous = char
        elif char.isalpha():
            if previous.isalpha():
                current_string += char
            else:
                formula_list.append(html.Sub(current_string))
                current_string = char
            previous = char
        else:
            # Not a letter or a number; something went wrong
            return
    return html.Span(formula_list[1:])


if __name__ == "__main__":
    app.run_server(debug=True)
