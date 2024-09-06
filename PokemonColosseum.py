import random
import Pokemon
import PokemonMoves
import math

name_list = {}
Team_Rocket = []
Team_Player = []
option_list = []
option_list_rocket = []
print("Welcome to Pokemon Colosseum!")
player_name = input("Enter Player Name: ")
Move_user_chose = 1

#random_choice(number,Team=[]): this method is used for both Team_Player and Team_Rocket where their pokemon
#are randomly chosen from the Pokemon_list in Pokemon.py with no duplicates
def random_choice(number,Team = []):
    value = random.choice(list(Pokemon.Pokemon_list.keys()))
    if value in Pokemon.Pokemon_list:
        True_or_False = search_through_Teams(value,Team)
        if True_or_False==0: #return 0 if duplicate is found
            return random_choice(number,Team)
        name_list[number] = Pokemon.Pokemon_list[value]
        number = number + 1

#Team_pokemons(Team = []): Calls random_choice() to choose random names for the Teams and then appends them to the list (first-in-first-out)
def Team_pokemons(Team = []):
    number = 1
    for i in range(3):
        random_choice(number,Team)
        Team.append(name_list[number])
        number = number+1

#coin_toss() : holds a random coin toss that will determine if Rocket(1) or Player(2) goes first.
def coin_toss():
    coin = random.choice([1,2])
    if coin == 1:
        print("Coin toss goes to ----- Team Rocket to start the attack!")
        return coin
    else:
        print("Coin toss goes to ----- Team "+player_name+" to start the attack!")
        return coin

#move(i): passes in the number coordinated with the name of the move.
# If the move has been used, then (N\A) will be printed next to the move that is unavailable.
def move(i):
    if i in option_list:
        name = Team_Player[0].name
        Move_name = Pokemon.search_for_move(name, i)
        print(i,":",Move_name)
    else:
        name = Team_Player[0].name
        Move_name = Pokemon.search_for_move(name, i)
        print(i, ":", Move_name, "(N/A)")

#options(HP_Rocket,HP_Player): this method is incharge of printing the methods available for the user
# and resets the options_list for Rocket and the Player. The option_list has the available numbers that correlate
#with the names of the pokemons moves so moves are not repeated until all are used.
def options(HP_Rocket,HP_Player):
    print("Choose the move for "+Team_Player[0].name+":")
    i = 0
    name = Team_Player[0].name
    Length_of_options = len(Pokemon.Pokemon_list[name].moves)
    for i in range(1,Length_of_options+1):
        move(i)
        i+=1
    user_value_chosen = user_option_input()
    Move_user_chose = Pokemon.Pokemon_list[name].moves[user_value_chosen-1]  #will now store the user option. Ex: chose 1 :Mega Punch
    print(name, "cast","'"+Move_user_chose+"'","to",Team_Rocket[0].name+":")
    Damage = calculations(Move_user_chose,Team_Player, Team_Rocket)
    HP_Rocket = HP_Rocket - Damage

    if(HP_Rocket<=0):
        print("Now",Team_Rocket[0].name,"faints back to poke ball, and ", Team_Player[0].name,"has",HP_Player,"HP")
        Team_Rocket.pop(0)
        if len(Team_Rocket)==0:
            print("All of Team Rocket's Pokemon fainted, and Team",player_name,"prevails!")
            exit()
        option_list_rocket.clear()
        reset_option_list(option_list_rocket,Team_Rocket)
        HP_Rocket = int(Team_Rocket[0].hp)
        print("Next for Team Rocket,",Team_Rocket[0].name,"enters battle!")
        return HP_Rocket
    else:
        print("Now",Team_Rocket[0].name,"has", HP_Rocket,"HP, and", Team_Player[0].name,"has",HP_Player,"HP")
        return HP_Rocket

#user_option_input(): Checks to see if the users input is one of the available moves
# and not unavailable or out of range(string, negative, etc.). Once an available move is selected, the number
# will be removed from the user_option list, so it can not be called again unless necessary.
def user_option_input():
        if len(option_list) == 0:
            option_list.clear()
            reset_option_list(option_list,Team_Player)
        try:
            val = int(input("Team " + player_name+ " choice: "))
            if val>5 or val<1:
                print("Please enter a number for an available option above")
                return user_option_input()
            elif val not in option_list:
                print("Please enter a number for an available option above")
                return user_option_input()
            else:
                option_list.remove(val)
                if len(option_list) == 0:
                    option_list.clear()
                    reset_option_list(option_list, Team_Player)
                return val
        except ValueError:
            print("Please enter a number for an available option above")
            return user_option_input()

#random_move_for_rocket(Length_of_Rocket): A random move is selected for Rocket but only if the number is available in
#option_list_rocket
def random_move_for_rocket(Length_of_Rocket):
    random_move_loop = random.choice(option_list_rocket)
    if random_move_loop in option_list_rocket:
        option_list_rocket.remove(random_move_loop)
        return random_move_loop
    else:
        return random_move_for_rocket(Length_of_Rocket)

#who_turn(coin_value,HP_Player,HP_Rocket): changes the turns back and forth between Team Rocket and the Players team. It
# also checks a majority of Rockets information. For example, health, resetting the option_list for Player, and checking if
#option_list_rocket needs to be reset.
def who_turn(coin_value,HP_Player,HP_Rocket):
        if coin_value == 1: #means that it is Team_Rockets turn
            name = Team_Rocket[0].name
            Length_of_Rocket = len(Pokemon.Pokemon_list[name].moves)
            if len(option_list_rocket)==0:
                reset_option_list(option_list_rocket,Team_Rocket)
            random_move = random_move_for_rocket(Length_of_Rocket)
            Move_name = Pokemon.search_for_move(name, random_move)
            print("Team Rocket's",name,"cast","'"+Move_name+"'","to",Team_Player[0].name+":")
            Damage = calculations(Move_name, Team_Rocket, Team_Player)
            HP_Player = int(HP_Player - Damage)
            coin_value = 2
            if (HP_Player <= 0):
                print("Now", Team_Rocket[0].name,"has",HP_Rocket,"HP, and",Team_Player[0].name,"faints back to poke ball.")
                Team_Player.pop(0)
                if len(Team_Player)==0:
                    print("All of Team",player_name,"Pokemon fainted, and Team Rocket prevails!")
                    exit()
                else:
                    option_list.clear()  # empties the whole list
                    reset_option_list(option_list, Team_Player)  # adds back the options for the player
                    print("Next for Team",player_name+",",Team_Player[0].name,"enters battle!")
                    health_player = int(Team_Player[0].hp)
                    who_turn(coin_value, health_player, HP_Rocket)

            else:
                print("Now", Team_Rocket[0].name, "has", HP_Rocket, "HP, and", Team_Player[0].name, "has", HP_Player,
                      "HP")
                who_turn(coin_value, HP_Player, HP_Rocket)

        else: # Means that it is Team_Player and needs to go into options
            health_rocket=options(HP_Rocket,HP_Player)  #Would pass in the rocket health since u wll be subtracting its health
            coin_value = 1
            who_turn(coin_value,HP_Player,health_rocket)

#compare_types_STAB(choice, Team = []): Compares the two teams types to see if the value will be 1.5 if the same or 1 if different.
def compare_types_STAB(choice, Team = []):
        if(Team[0].type == PokemonMoves.pokemon_moves[choice].get("type")):
            return 1.5
        else:
            return 1
#calculations(choice,Team = [], Team2 = []): calculates and returns the damage by using the Damage(M,A,B) formula
def calculations(choice,Team = [], Team2 = []):
    name = Team[0].name
    name2 = Team2[0].name
    PM = int(PokemonMoves.pokemon_moves[choice].get("power"))
    AA = int(Pokemon.Pokemon_list[name].attack)   #attack
    DB = int(Pokemon.Pokemon_list[name2].defence) #defence
    STAB = compare_types_STAB(choice,Team)
    Team_2_type = Pokemon.Pokemon_list[name2].type
    Team_1_type = PokemonMoves.pokemon_moves[choice].get("type")
    TE_M_B = PokemonMoves.search_for_information(Team_1_type,Team_2_type)
    Random = round(random.uniform(0.5,1),1)
    Damage = math.ceil(PM*(AA/DB)*STAB*TE_M_B*Random)
    print("Damage to", name2, "is", Damage, "points")
    return Damage

#reset_option_list(option = [],Team = []): resets the option list when either, using all of the options that have been chosen
# or a new pokemon is being played.
def reset_option_list(option = [],Team = []):
    i = 1
    name = Team[0].name
    Length = len(Pokemon.Pokemon_list[name].moves)
    for i in range(1,Length+1):
        option.append(i)

#search_through_Teams(value,Team): Searches through both teams to make sure there are no duplicated pokemons being played.
def search_through_Teams(value,Team):
    for key in Team_Rocket:
        if key.name == value:
            return 0
    for key in Team_Player:
        if key.name == value:
            return 0
    return 1

#main
if __name__ == "__main__":
    Team_pokemons(Team_Rocket)
    print("Team Rocket enters with",Team_Rocket[0].name+", "+Team_Rocket[1].name+", and "+Team_Rocket[2].name)
    Team_pokemons(Team_Player)
    print("Team "+player_name+" enters with",Team_Player[0].name +", "+Team_Player[1].name+", and "+Team_Player[2].name)
    print("Let the battle begin!")
    name = Team_Player[0].name
    name2 = Team_Rocket[0].name
    HP_Player = int(Pokemon.Pokemon_list[name].hp)
    HP_Rocket = int(Pokemon.Pokemon_list[name2].hp)
    reset_option_list(option_list_rocket,Team_Rocket)
    reset_option_list(option_list,Team_Player)
    coin_value = coin_toss()
    who_turn(coin_value,HP_Player,HP_Rocket)
