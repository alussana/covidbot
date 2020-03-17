# CovidBot
Non-retrospectively monitoring of COVID-19 pandemic over time

## COVID-19 Cases

Data collection of relevant statistics about the novel Coronavirus pandemic was started on 2020-03-15. Plots generated by CovidBot are reported below and updated every day. Note than only the data for a subset of countries is displayed. The row data contains information for 22 countries.

### Confirmed Coronavirus Cases Per 1 Million Citizens

![covid_cases_1M_pop](covid_cases_1M_pop.svg)

### Confirmed Total Coronavirus Cases

![covid_total_cases](covid_total_cases.svg)

## Data Collection

CovidBot fetches the data that are currently published at https://www.worldometers.info/coronavirus/

[...]

## How To Use CovidBot

[...]

## Requirements

* [Firefox browser](https://www.mozilla.org)
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* [Python3](https://www.python.org), plus following libraries:
  * [Pandas](https://pandas.pydata.org)
  * [Seaborn](https://seaborn.pydata.org)
  * [Selenium](https://selenium-python.readthedocs.io)

## Upcoming Features

* Plot with death rate by country
* Mail alert