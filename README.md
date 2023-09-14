# Engeto-third-project

The third project at Python Academy by Engeto.

## Project description

This project is used to extract the results from the parliamentary elections in 2017. Link:https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

## Installing libraries
The libraries that are used in the code are stored in the requirements.txt file. For installation, I recommend using a new virtual environment and running it as follows with the manager installed.

```bash
$ pip3 --verison                    # version verification 
$ pip3 install -r requirements.txt  # installing libraries
```

## Project launch

Running the election-scraper.py file within the terminal requires two mandatory arguments.

```bash
python election-scraper.py "url-of-regional-self-governing-unit" "final-file"
```

## Project display

How to start for the Prostějov district:

```bash
python election-scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "prostejov.csv"
```
