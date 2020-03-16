#!/usr/bin/env python3

from selenium import webdriver
from datetime import datetime
from pathlib import Path
from math import log2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CovidBot():
    
    def __init__(self):
        self.driver = webdriver.Firefox()
        print('CovidBot: deployed webdriver.')
        self.names = [  'China', 'Italy', 'Iran', 'S. Korea', 'Spain', 'Germany', \
                        'France', 'USA', 'Switzerland', 'Norway', 'UK', 'Netherlands', \
                        'Sweden', 'Belgium', 'Denmark', 'Japan', 'Malaysia', 'Qatar', \
                        'Australia', 'Canada', 'Portugal', 'Finland']
        self.plottable_names = ['Italy', 'Spain', 'Germany', 'France', 'Norway', 'UK', \
                                'Sweden', 'Finland', 'China', 'USA']
        try:
            self.total_counts = pd.read_table('covid_total_cases.tsv', header=0, index_col=0)
            self.cases_1M_pop = pd.read_table('covid_cases_1M_pop.tsv', header=0, index_col=0)
            print('CovidBot: previous records have been loaded.')
        except:
            print('CovidBot: no previous records found. Starting data collection form scratch.')
    
    def get_data(self):
        try:
            page = self.driver.get('https://www.worldometers.info/coronavirus/')
            table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody[1]')
            table = table.text
            table = table.split('\n')
            total_counts = []
            cases_1M_pop = []
            row_labels = []
            for record in table:
                for name in self.names:
                    if name in record:
                        row_labels.append(name)
                        row = record[len(name):].split(' ')[1:]
                        total_counts.append(int(row[0].replace(',', '')))
                        cases_1M_pop.append(float(row[len(row) - 1]))
            current_date = str(datetime.now())[:10]
            cases_1M_pop = {current_date: cases_1M_pop}
            total_counts = {current_date: total_counts}
            if hasattr(self, 'cases_1M_pop'):
                self.cases_1M_pop = self.cases_1M_pop.join(pd.DataFrame(index=row_labels, data=cases_1M_pop)) 
            else:
                self.cases_1M_pop = pd.DataFrame(index=row_labels, data=cases_1M_pop)
            if hasattr(self, 'total_counts'):
                self.total_counts = self.total_counts.join(pd.DataFrame(index=row_labels, data=total_counts))
            else:
                self.total_counts = pd.DataFrame(index=row_labels, data=total_counts)
            print('CovidBot: fetched current data.')
        except:
            print('CovidBot: could not fetch data :(')
        
    def export_data(self, prefix):
        prefix = Path(prefix)
        self.total_counts.to_csv(prefix / 'covid_total_cases.tsv', sep='\t')
        self.cases_1M_pop.to_csv(prefix / 'covid_cases_1M_pop.tsv', sep='\t')
        print(f'CovidBot: exported data in {prefix}/')

    def plot_data(self):
        sns.set(style="darkgrid")
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
        plot = sns.lineplot(x='Day', y='Cases per 1M population (log2 scale)', hue='Country', data=lp_data)
        plt.xticks(rotation=45, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig("covid_cases_1M_pop.svg", bbox_inches = "tight")
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
        plot = sns.lineplot(x='Day', y='Total Cases (log2 scale)', hue='Country', data=lp_data)
        plt.xticks(rotation=45, horizontalalignment='right')
        plt.legend(bbox_to_anchor=(1, 1), borderaxespad=0.)
        sns.despine(top=True, right=True, bottom=True)
        plot.figure.savefig("covid_total_cases.svg", bbox_inches = "tight")
        print('CovidBot: data has been plotted.')

if __name__ == '__main__':
    covidbot = CovidBot()
    covidbot.get_data()
    covidbot.export_data('.')
    covidbot.plot_data()