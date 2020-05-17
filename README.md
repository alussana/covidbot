# CovidBot
Monitoring of COVID-19 pandemic over time

## COVID-19 Pandemic Monitoring

Data collection of relevant statistics about the novel Coronavirus pandemic was started between 2020-03-15 and 2020-03-17, with the exception of the clinical tests counts, which was started on 2020-04-04. Plots generated by CovidBot are reported below and automatically updated every day at 22:00, Helsinki time (GMT+2).

--- **Notice** ---

------

==**Data collection stopped after 2020-05-14**==

-----------------

Note that only the data for a subset of countries is displayed. The row data contains information for 22 countries.

### Confirmed Coronavirus Cases Per 1 Million Citizens

![covid_cases_1M_pop](covid_cases_1M_pop.svg)

### Confirmed Total Coronavirus Cases

![covid_total_cases](covid_total_cases.svg)

### Coronavirus Death Rate

![covid_death_rate](covid_death_rate.svg)

### Total Confirmed Deaths Due To Coronavirus

![covid_total_deaths](covid_total_deaths.svg)

### Fraction Of Population Tested For SARS-CoV-2

![covid_tests_1M_pop](covid_tests_1M_pop.svg)

### Global Fraction Of SARS-CoV-2 Tests With Positive Outcome

![covid_pos_rate](covid_pos_rate.svg)

## Data Collection

CovidBot fetches the current data published at https://www.worldometers.info/coronavirus/ and adds those data to existing local files. If those files are not present, it starts the data collection from scratch. This task is not meant to be performed more than once per day. After every run, CovidBot uses all the available data to generate updated plots.

Data collected and processed over time are stored in the following tsv files:

* `covid_cases_1M_pop.tsv`: number of cases per 1 million citizens
* `covid_death_rate.tsv`: number of deaths / number of cases
* `covid_total_cases.tsv`: total number of cases
* `covid_total_deaths.tsv`: total number of deaths
* `covid_total_tests.tsv`: total number of tests
* `covid_tests_1M_pop.tsv`: number of tests per 1 million citizens
* `covid_pos_rate.tsv`: total number of cases / total number of tests

Then, the following plots are generated:

* `covid_cases_1M_pop.svg`
* `covid_death_rate.svg`
* `covid_total_cases.svg`
* `covid_total_deaths.svg`
* `covid_tests_1M_pop.svg`
* `covid_pos_rate.svg`

Plots of non-cumulative distributions of new deaths and new cases for a given `${country}` can be also generated. The naming convention is the following:

* `covid_cases_${country}.svg`
* `covid_deaths_${country}.svg`

For instance, at the bottom of this page additional plots for [Italy](#italian-situation) and [Finland](#finnish-situation) are displayed.

## How To Use CovidBot

CovidBot can be run every day to automatically collect data over time, store them locally, and generate plots. To do so the easiest and fully-automatic way is to use `crontab` to run it daily at a specified time, e.g. 23:55. Here is how to do it:

Clone this repository in a `/path/of/your/choice`:

```
cd /path/of/your/choice
git clone https://github.com/alussana/covidbot
```

Add the task to the `crontab` schedule:

* `crontab -e` will open the crontab task file

* Add the following and save:

  ```
  SHELL=/bin/bash
  55 23 * * * cd /path/of/your/choice/covidbot; ./covidbot.py >/dev/null 2>&1
  ```

### Requirements

* [Firefox browser](https://www.mozilla.org)
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
* [Python3](https://www.python.org), plus following libraries:
  * [Pandas](https://pandas.pydata.org)
  * [Seaborn](https://seaborn.pydata.org)
  * [Selenium](https://selenium-python.readthedocs.io)

## Background

Around the 15th of March 2020 COVID-19 cases started to increase in Finland, the country that is hosting me while I'm working on my Master's thesis project. I then developed a simple tool to track the changes of a few metrics related to the COVID-19 pandemic over time and in different regions of the world. I decided to collect publicly available data for my personal interest, in order to monitor the situation and display the information that are more relevant to me in a customized manner.

## Italian Situation

Country-specific plots for Italy

### Confirmed New Cases Distribution

![covid_cases_Italy](covid_cases_Italy.svg)

### Confirmed New Deaths Distribution

![covid_deaths_Italy](covid_deaths_Italy.svg)

## Finnish Situation

Country-specific plots for Finland

### Confirmed New Cases Distribution

![covid_deaths_Finland](covid_cases_Finland.svg)

### Confirmed New Deaths Distribution

![covid_deaths_Finland](covid_deaths_Finland.svg)

## Upcoming Features

[X] Plot of death rate by country

[X] Country-specific plots of non-cumulative distribution of new cases and new deaths

[_] Plot of total clinical tests by country

[X] Plot of fraction of tested population by country

[X] Plot of global fraction of tests with positive outcome by country

[_] Plot of per-day fraction of tests with positive outcome by country

[_] Mail alert

Have comments, suggestions, or interest in collaboration? Just drop a quick email to alessandro.lussana@pm.me