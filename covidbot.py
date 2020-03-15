#!/usr/bin/env python3

from selenium import webdriver
from datetime import datetime
from pathlib import Path
import pandas as pd

class CovidBot():
    
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.names = [  'China', 'Italy', 'Iran', 'S. Korea', 'Spain', 'Germany', \
                        'France', 'USA', 'Switzerland', 'Norway', 'UK', 'Netherlands', \
                        'Sweden', 'Belgium', 'Denmark', 'Japan', 'Malaysia', 'Qatar', \
                        'Australia', 'Canada', 'Portugal', 'Finland']
        try:
            self.total_counts = pd.read_table('covid_total_cases.tsv', header=0, index_col=0)
            self.cases_1M_pop = pd.read_table('covid_cases_1M_pop.tsv', header=0, index_col=0)
            print('Covid: previous records have been loaded.')
        except:
            print('Covid: no previous records found. Starting form scratch.')  
    
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
            current_date = str(datetime.now())[:9]
            cases_1M_pop = {current_date: cases_1M_pop}
            total_counts = {current_date: total_counts}
            if hasattr(self, 'cases_1M_pop'):
                self.cases_1M_pop.join(pd.DataFrame(data=cases_1M_pop)) 
            else:
                self.cases_1M_pop = pd.DataFrame(index=row_labels, data=cases_1M_pop)
            if hasattr(self, 'total_counts'):
                self.total_counts.join(pd.DataFrame(data=total_counts))
            else:
                self.total_counts = pd.DataFrame(index=row_labels, data=total_counts)
            self.export_data('.')
        except:
            print('Covid: could not fetch data :(')
        
    def export_data(self, prefix):
        prefix = Path(prefix)
        self.total_counts.to_csv(prefix / 'covid_total_cases.tsv', sep='\t')
        self.cases_1M_pop.to_csv(prefix / 'covid_cases_1M_pop.tsv', sep='\t')

if __name__ == '__main__':
    covidbot = CovidBot()
    covidbot.get_data()