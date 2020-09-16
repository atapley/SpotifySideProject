# split everything up based on year
# Average together to find trends per year
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

genre_list = ["rock", "pop", "hip-hop", "country"]
for genre in genre_list:
    csv = pd.read_csv('./data/' + genre + '.csv')
    years_list = range(2010,2020)
    sorted_csv = {}
    averages = {}

    for year in years_list:
        sorted_csv[str(year)] = {}
        averages[str(year)] = {}
        for feature in csv.keys()[5::]:
            sorted_csv[str(year)][feature] = []
            averages[str(year)][feature] = 0

    for row in csv.iterrows():
        year = row[1]['year']
        for feature in csv.keys()[5::]:
            sorted_csv[str(year)][feature].append(row[1][5::][feature])

    for year in sorted_csv.keys():
        for feature in sorted_csv[year].keys():
            avg = np.mean(sorted_csv[year][feature])
            averages[year][feature] = avg

    with open(genre + '.json', 'w') as fp:
        json.dump(averages, fp)

    fig = plt.figure(figsize=(15,15))

    for i, feature in enumerate(sorted_csv[str(year)].keys()):
        feature_list = []
        for year in years_list:
            feature_list.append(averages[str(year)][feature])
        figure = fig.add_subplot(4, 4, i + 1,)
        figure.set_title(feature)
        plt.subplots_adjust(top=.8)
        plt.scatter(years_list,feature_list)
        plt.suptitle(genre + ' Analytics')
        m,b = np.polyfit(years_list,feature_list,1)
        plt.plot(years_list, m*years_list + b)
        plt.tight_layout()

    plt.savefig(genre + '.png')