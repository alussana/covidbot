#!/usr/bin/env python3

from selenium import webdriver
from datetime import datetime
from pathlib import Path
from math import log2
from selenium.webdriver.firefox.options import Options
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CovidBot():
    
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        print('CovidBot: deployed webdriver.')
        self.names = [  'China', 'Italy', 'Iran', 'S. Korea', 'Spain', 'Germany', \
                        'France', 'USA', 'Switzerland', 'Norway', 'UK', 'Netherlands', \
                        'Sweden', 'Belgium', 'Denmark', 'Japan', 'Malaysia', 'Qatar', \
                        'Australia', 'Canada', 'Portugal', 'Finland']
        self.plottable_names = ['China', 'USA', 'Australia', 'Japan', \
                                'Germany', 'UK', 'France', 'Italy', 'Spain', \
                                'Norway', 'Sweden', 'Finland']
        try:
            self.total_counts = pd.read_table('covid_total_cases.tsv', header=0, index_col=0)
            self.cases_1M_pop = pd.read_table('covid_cases_1M_pop.tsv', header=0, index_col=0)
            self.total_deaths = pd.read_table('covid_total_deaths.tsv', header=0, index_col=0)
            self.death_rate = pd.read_table('covid_death_rate.tsv', header=0, index_col=0)
            print('CovidBot: previous records have been loaded.')
        except:
            print('CovidBot: no previous records found. Starting data collection form scratch.')

    def close_driver(self):
        self.driver.close()
    
    def get_data(self):
        try:
            page = self.driver.get('https://www.worldometers.info/coronavirus/')
            try:
                table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody[1]')
            except:
                table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
            total_counts = []
            cases_1M_pop = []
            total_deaths = []
            death_rate = []
            row_labels = []
            for name in self.names:
                try:
                    row = table.find_element_by_xpath(f"//td[contains(text(), '{name}')]")
                    row = row.find_element_by_xpath("./..")
                except:
                    row = table.find_element_by_xpath(f"//a[contains(text(), '{name}')]")
                    row = row.find_element_by_xpath("./../..")
                cases = int(row.find_element_by_xpath("*[2]").text.replace(',', ''))
                fraction = row.find_element_by_xpath("*[9]").text.replace(',', '')
                fraction = float(fraction)
                deaths = row.find_element_by_xpath("*[4]").text.replace(',', '')
                if deaths == '':
                    deaths = 0
                else:
                    deaths = int(deaths)
                total_counts.append(cases) 
                cases_1M_pop.append(fraction)
                total_deaths.append(deaths)
                death_rate.append(deaths / cases)
                row_labels.append(name)
            current_date = str(datetime.now())[:10]
            cases_1M_pop = {current_date: cases_1M_pop}
            total_counts = {current_date: total_counts}
            total_deaths = {current_date: total_deaths}
            death_rate = {current_date: death_rate}
            if hasattr(self, 'cases_1M_pop'):
                cases_1M_pop = pd.DataFrame(index=row_labels, data=cases_1M_pop)
                self.cases_1M_pop = self.cases_1M_pop.join(cases_1M_pop) 
            else:
                self.cases_1M_pop = pd.DataFrame(index=row_labels, data=cases_1M_pop)
            if hasattr(self, 'total_counts'):
                total_counts = pd.DataFrame(index=row_labels, data=total_counts)
                self.total_counts = self.total_counts.join(total_counts)
            else:
                self.total_counts = pd.DataFrame(index=row_labels, data=total_counts)
            if hasattr(self, 'total_deaths'):
                total_deaths = pd.DataFrame(index=row_labels, data=total_deaths)
                self.total_deaths = self.total_deaths.join(total_deaths)
            else:
                self.total_deaths = pd.DataFrame(index=row_labels, data=total_deaths)
            if hasattr(self, 'death_rate'):
                death_rate = pd.DataFrame(index=row_labels, data=death_rate)
                self.death_rate = self.death_rate.join(death_rate)
            else:
                self.death_rate = pd.DataFrame(index=row_labels, data=death_rate)
            print('CovidBot: fetched current data.')
        except:
            print('CovidBot: could not fetch data :(')
        
    def export_data(self, prefix='.'):
        prefix = Path(prefix)
        self.total_counts.to_csv(prefix / 'covid_total_cases.tsv', sep='\t')
        self.cases_1M_pop.to_csv(prefix / 'covid_cases_1M_pop.tsv', sep='\t')
        self.death_rate.to_csv(prefix / 'covid_death_rate.tsv', sep='\t')
        self.total_deaths.to_csv(prefix / 'covid_total_deaths.tsv', sep='\t')
        print(f'CovidBot: exported data in {prefix}/')
    
    def plot_deaths_by_day(self, country, prefix='.', context='paper'):
        plt.clf()
        sns.set(style="darkgrid")
        sns.set_context(context)
        prefix = Path(prefix)
        timepoints = list(self.total_deaths.columns)
        signal = self.total_deaths[self.total_deaths.index.isin([country])]
        day = []
        delta = []
        for i in range(1, len(timepoints)):
            day.append(timepoints[i])
            delta.append(int(signal[timepoints[i]] - signal[timepoints[i - 1]]))
        cp_data = pd.DataFrame({'Day':day, 'Confirmed Deaths':delta})
        plot=sns.catplot(x='Day', y='Confirmed Deaths', data=cp_data, kind="bar", palette=sns.color_palette(['black']), alpha=0.6)
        plt.xticks(rotation=90, horizontalalignment='right')
        plot.savefig(prefix / f"covid_deaths_{country}.svg", bbox_inches = "tight")

    def plot_cases_by_day(self, country, prefix='.', context='paper'):
        plt.clf()
        sns.set(style="darkgrid")
        sns.set_context(context)
        prefix = Path(prefix)
        timepoints = list(self.total_counts.columns)
        signal = self.total_counts[self.total_counts.index.isin([country])]
        day = []
        delta = []
        for i in range(1, len(timepoints)):
            day.append(timepoints[i])
            delta.append(int(signal[timepoints[i]] - signal[timepoints[i - 1]]))        
        cp_data = pd.DataFrame({'Day':day, 'Confirmed Cases':delta})
        plot=sns.catplot(x='Day', y='Confirmed Cases', data=cp_data, kind="bar", palette=sns.color_palette(['cyan']), alpha=0.6)
        plt.xticks(rotation=90, horizontalalignment='right')
        plot.savefig(prefix / f"covid_cases_{country}.svg", bbox_inches = "tight")

    def plot_data(self, context="paper", prefix='.'):
        prefix = Path(prefix)
        plt.clf()
        sns.set(style="darkgrid")
        sns.set_context(context)
        ## lineplot: Cases per 1M population (log2 scale)
        timepoints = list(self.cases_1M_pop.columns)
        day = []
        signal = []
        country = []
        for i in timepoints:
            for j in self.plottable_names:
                day.append(i)
                country.append(j)
                signal.append(log2(self.cases_1M_pop[i][j]))
        lp_data = pd.DataFrame({'Day':day, 'Country':country, 'Cases per 1M population (log2 scale)': signal})
        plot = sns.lineplot(x='Day', y='Cases per 1M population (log2 scale)', hue='Country', palette='Paired', data=lp_data)
        plt.xticks(rotation=90, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.5)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig(prefix / "covid_cases_1M_pop.svg", bbox_inches = "tight")
        ## lineplot: Total Cases (log2 scale)'
        plt.clf()
        timepoints = list(self.total_counts.columns)
        day = []
        signal = []
        country = []
        for i in timepoints:
            for j in self.plottable_names:
                day.append(i)
                country.append(j)
                signal.append(log2(self.total_counts[i][j]))
        lp_data = pd.DataFrame({'Day':day, 'Country':country, 'Total Cases (log2 scale)': signal})
        plot = sns.lineplot(x='Day', y='Total Cases (log2 scale)', hue='Country', palette='Paired', data=lp_data)
        plt.xticks(rotation=90, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.5)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig(prefix / "covid_total_cases.svg", bbox_inches = "tight")
        ## lineplot: Death Rate
        plt.clf()
        timepoints = list(self.death_rate.columns)
        day = []
        signal = []
        country = []
        for i in timepoints:
            for j in self.plottable_names:
                day.append(i)
                country.append(j)
                signal.append(self.death_rate[i][j])
        lp_data = pd.DataFrame({'Day':day, 'Country':country, 'Death Rate': signal})
        plot = sns.lineplot(x='Day', y='Death Rate', hue='Country', palette='Paired', data=lp_data)
        plt.xticks(rotation=90, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.5)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig(prefix / "covid_death_rate.svg", bbox_inches = "tight")
        print('CovidBot: data has been plotted.')
        ## lineplot: Total Deaths (log2 scale)
        plt.clf()
        timepoints = list(self.total_deaths.columns)
        day = []
        signal = []
        country = []
        for i in timepoints:
            for j in self.plottable_names:
                day.append(i)
                country.append(j)
                if self.total_deaths[i][j] == 0:
                    signal.append(0)
                else:
                    signal.append(log2(self.total_deaths[i][j]))
        lp_data = pd.DataFrame({'Day':day, 'Country':country, 'Total Deaths (log2 scale)': signal})
        plot = sns.lineplot(x='Day', y='Total Deaths (log2 scale)', hue='Country', palette='Paired', data=lp_data)
        plt.xticks(rotation=90, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.5)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig(prefix / "covid_total_deaths.svg", bbox_inches = "tight")

if __name__ == '__main__':
    covidbot = CovidBot()
    covidbot.get_data()
    covidbot.export_data()
    covidbot.plot_data("notebook")
    covidbot.plot_cases_by_day('Italy', context="notebook")
    covidbot.plot_deaths_by_day('Italy', context="notebook")
    covidbot.close_driver()