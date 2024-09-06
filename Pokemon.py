import csv
import ast
pokemon_filename = 'pokemon-data.csv'

header = []
pokemon_moves = {}
Pokemon_list = {}
list = []

class Pokemon:
    def __init__(pokemon,name,type,hp,attack,defence,moves):
        pokemon.name = name
        pokemon.type = type
        pokemon.hp = hp
        pokemon.attack = attack
        pokemon.defence = defence
        pokemon.moves = moves

with open(pokemon_filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    for row in reader:
        moves=''
        end_of_moves=False
        for s in row:
            if s[0]=='[':
                end_of_moves = True
                moves = s
            elif end_of_moves == True:
                moves += ','+s
                if s[-1] == ']':
                    end_of_moves = False
        pokemon_moves= ast.literal_eval(moves)
        Pokemon_list[row[0]] = Pokemon(row[0],row[1],row[2],row[3],row[4],pokemon_moves)  #this will store each of the pokemons values and results.


#search_for_move(value,option): compares the names in Pokemon_list to the name parsed in(value) to find the moves.
def search_for_move(value,option):
    for name in Pokemon_list:
            if name == value:
                Result = Pokemon_list[name]
                return (Result.moves[option - 1])
                if option>=1:
                    return(Result.moves[option-1])

