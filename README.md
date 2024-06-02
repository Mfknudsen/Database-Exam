# Database-Exam
## Requirements

An environment file not present in the repo containing the links and passwords required to connect to the different databases is needed.

### SQL - Units
When running the python script for data ingestion for the sql script a folder containing different catalogs for the faction armies used in the tabletop 40K board game.

To Install go to:
https://github.com/BSData/wh40k-10e. 
Clone the repo into the folder Database-Exam/SQL - Units.

### Document - Lore

An internet connection is required and the website https://warhammer40k.fandom.com/wiki/Warhammer_40k_Wiki is required to be up and running.

## How to use

### SQL - Units
In the folder SQL - Units.

First start your MySQL database service.

Open and run Create.sql.

Open and run data_ingestion.ipynb.

The SQL database should now be full of data.

### Document - Lore

In the folder Document - Lore.

Open and run DataGathere.ipynb.

Open and run DataUploader.ipynb.

### Application

In the root folder.

Run app.py

Run gui.py