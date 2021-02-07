# ShotHub

## Requirements
* \>= `Python 3.8.x`
* `pip`
* Linux, Mac OS, or Windows

## Development

### Setting up local environment

* Step 1: Clone this repo and `cd` into it
```
git clone https://github.com/AtaGowani/ShotHub.git && cd ShotHub
```

* Step 2: Set up the virtual environment and add `.env`
```
python3 -m venv .venv
```
```
cat .env_EXAMPLE >> .env
```
This will create a new file `.env` with a template of what the file shuold look like please navigate to your GCP account to populate the data in order to establish a proper db connection.

* Step 3: Start up the virutal environment
```
source .venv/bin/activate
```

* Step 4: Download the dependencies
```
pip install -r requirements.txt
```

* Step 5: Start the server
`python main.py`

### DB Population Scripts
* `create_patients.py`
* `create_tables.py`
* `create_technicians.py`
* `create_vac_records.py`
* `create_vaccines.py`