import requests 
import json 
import matplotlib.pyplot as plt
from os import path

to_be_shown_coutry=['FRA', 'ITA', 'USA', 'DEU', 'ESP']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

def plot(ax, y, country):
    if country in to_be_shown_coutry:
        x, y = arrange_data(y)
        ax.plot(x,y, label=country)

def arrange_data(daily_list):
    total_cases_list = []
    reverse_daily_cases_list = []
    total_cases = 0 
    for daily_cases in reversed(daily_list):

        total_cases += daily_cases
        if total_cases > 100:
            reverse_daily_cases_list.append(daily_cases)
            total_cases_list.append(total_cases)

    return total_cases_list, reverse_daily_cases_list

data={}
if path.exists('data.json'):
    with open('data.json', 'r') as f:
        data=json.load(f)
else: 
    response = requests.get('https://opendata.ecdc.europa.eu/covid19/casedistribution/json/')
    with open('data.json', 'w') as f:
        json.dump(response.json(), f)


current_country=data['records'][0]['countryterritoryCode']
y_cases = []
y_deaths = []

for record in data['records']:
    if current_country != record['countryterritoryCode']:
        plot(ax1, y_cases, current_country)
        plot(ax2, y_deaths, current_country)
        y_cases = []
        y_deaths = []    
        current_country=record['countryterritoryCode']
    y_cases.append(int(record['cases']))
    y_deaths.append(int(record['deaths']))


ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax1.legend()
ax2.legend()
ax1.set_xlabel('Total cases')
ax1.set_ylabel('Daily new cases')
ax2.set_xlabel('Total deaths')
ax2.set_ylabel('Daily new death')
ax1.grid()
ax2.grid()
plt.show()
