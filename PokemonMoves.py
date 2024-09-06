import csv
import ast

pokemon_filename = 'moves-data.csv'

header = []
pokemon_moves = {}

#Team_2_type matches the Defend while Team_1_type matches the Attack
Table = {'Normal':{'Normal':1,'Fire':1,'Water':1,'Electric':1,'Grass':1,'Others':1},
         'Fire':{'Normal':1,'Fire':0.5,'Water':2,'Electric':1,'Grass':0.5,'Others':1},
         'Water':{'Normal':1,'Fire':0.5,'Water':0.5,'Electric':2,'Grass':2,'Others':1},
         'Electric':{'Normal':1,'Fire':1,'Water':1,'Electric':0.5,'Grass':1,'Others':1},
         'Grass':{'Normal':1,'Fire':2,'Water':0.5,'Electric':0.5,'Grass':0.5,'Others':1}}

with open(pokemon_filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    for row in reader:
        pokemon_moves[row[0]] = dict(type=row[1], category=row[2], contest=row[3], pp=row[4], power = row[5], accuracy = row[6])

#Searches through the table to find the types match. If the attacks type is considered 'Others'(ex:Bug) it will be matched with 'Others' value
def search_for_information(Team_1_type,Team_2_type):
    if Team_1_type not in Table:
        return Table[Team_2_type]['Others']
    else:
        return Table[Team_2_type][Team_1_type]
