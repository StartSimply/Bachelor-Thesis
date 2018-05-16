import csv
import json

project_id = 2
critical_concentration_percentage = '0.0006n2a'

maximal_distances = json.load(open('Dataset/Maximal_distances/' +
                                   str(project_id) + '/' +
                                   str(critical_concentration_percentage), 'r'))

with open('6n2a.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(maximal_distances['concentrated'])


with open('6n2a.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in spamreader:
         print(', '.join(row))