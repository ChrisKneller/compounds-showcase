# Background

The purpose of this is to show some interesting software engineering based on a single json file with compound & assay data.

# Setup

## Requirements

Before going through the installation steps, ensure you have the following installed:
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

The below have been tested and successfully run on Ubuntu20.04 and MacOS Catalina (10.15.7) at the time of writing (commit hash `ceff610741d3291770fb8ed9d470bb14ec717d2f`).

### Cloning

- Clone this repo & cd into it

```shell
$ git clone https://github.com/ChrisKneller/compounds-showcase
$ cd compounds-showcase
```

### Option 1: Automatic installation and running (Linux/MacOS)

```shell
$ ./setup.sh
```

<sub>(permissions should persist via the git setup, but if you get `permission denied: ./setup.sh`, you need to run `chmod +x setup.sh` before then running `./setup.sh` again)</sub>

This will create a virtual environment, activate it, install requirements, run a Prefect pipeline to convert the json data into a database and then serve two web servers at 0.0.0.0 (API on port 5000; dashboard on port 8050).

After running this script once you can always just run `python3 runservers.py` to just run the servers.

### Option 2: Run the comands for yourself

1. Set up a virtual environment, activate it and install the requirements

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

2. Run the `Prefect` flow to create a database and tables from the json data

```shell
$ python3 flaskapp/transform.py
```

Check that `compound_assay.sqlite` has been created in the `flaskapp` folder. Prefect should provide some logging to show which stages were successful or unsuccessful.

3. Run the servers locally

```shell
$ python3 runservers.py
```

# What just happened?

The above steps should have:

- created a sqlite database
- created a flask app based on the above database providing API endpoints (GET only at this stage), served locally on port 5000 
- created a dash app allowing browsing of compound and assay data, with some visuals to explore the data, served locally on port 8050 

You should have some logging to confirm this:

```text
INFO:waitress:Serving on http://0.0.0.0:5000
INFO:waitress:Serving on http://0.0.0.0:8050
```

Go to http://localhost:8050 or http://0.0.0.0:8050 and click compounds to start browsing compound data.

# Time to explore! Things to do...

 ## On the [compounds](http://0.0.0.0:8050/compounds) page:
 
 ### Check out the scatter plot
- hover over any data points that you want more detail for, including the trendlines
- in the "Number of rings" key, click any category to remove it from the plot (recommend removing 1); click it again to add it back

### Check out the table
 - Sort any column
 - Filter columns
	 - Try filtering e.g. for "Cl" in molecular_formula to see any compounds containing chlorine. You can further filter for e.g. molecular weight ">500", ALogP "<5". You can then see that there is only one compound containing chlorine with a molecular weight about 500 and ALogP below 5
- Click through to any compound to see a dedicated page with further information on the compound

## On an [individual compound](http://0.0.0.0:8050/compounds/1175669) page:
### Summary
- Read through the summary of the compound
### Check out the smiles plot
- You can play around with the compound and modify it here
- After modifying you can then produce a new smiles code by clicking the button with two triangles
- With this same button you can also paste in a new smiles code
- None of this will be saved
### Check out the assay results
- The table of assay results shows all assay results associated with the compound along with their data.
- Click through to any individual assay page to see a basic dedicated page for that assay

## On the [assays](http://0.0.0.0:8050/assays) page

### Check out the bar graph
- hover over any data points that you want more detail for, including the trendlines
- in the "target, result" key, click any category to remove it from the plot (recommend removing 1); click it again to add it back

### Check out the table
 - Sort any column
 - Filter columns
	 - Try filtering e.g. for "Cl" in molecular_formula to see any compounds containing chlorine. You can further filter for e.g. molecular weight ">500", ALogP "<5". You can then see that there is only one compound containing chlorine with a molecular weight about 500 and ALogP below 5
- Click through to any compound to see a dedicated page with further information on the compound

# Notes

## Design choices & potential future updates

### Prefect

- I wanted to get some experience in using Prefect for running flows so using this was a deliberate choice to experiment for the first time.
- There was no need to use the UI here but I would like to implement and play around with the UI in future. This would make it nicer for others to run flows and see the log data.

### Database

- Sqlite was used for speed and ease of implementation. For a basic showcase that only includes reading and not writing, I consider it good enough; in a true production environment (especially where writing is required) I would probably use Postgres.

### API
- This is an incredibly basic API implementation in Flask that, again, is suitable for a basic showcase.
- For a more complex project I would update the project structure or consider switching to DRF. FastAPI is also good option depending on the circumstances.
- Depending on user needs, it may or may not be beneficial to set up POST endpoints to add additional compounds and assays and/or PUT endpoints to update existing information.

### Language
- I am first and foremost a backend developer and wanted to write as much as possible in Python. Dash, in my opinion, is a great framework for using almost pure Python to build a decent looking web dashboard.

### Deployment & server
- The built-in server in Flask is not suitable for use in production, so I chose to use [waitress](https://github.com/Pylons/waitress), a "production-quality pure-Python WSGI server with very acceptable performance" which no dependencies other than those in the standard Python library.
- Hosting at 0.0.0.0 allows other devices on the same network to access the server by visiting {host_computer_ip}:8050. This would require the appropriate firewall settings to allow access.
- I chose local deployment as I considered that the most likely use case for this type of information & dashboard would be internal teams connected to the same network.

### Docker
- Docker has not been used here, but a good future update would be to dockerise both apps and a postgres db and then run all 3 with docker-compose.

