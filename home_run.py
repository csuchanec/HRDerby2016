from __future__ import print_function
from datetime import datetime
import mlbgame
import mlbgame.update

from pandas import DataFrame, Series
import pandas as pd 

#configure the set-up. Not well factored
year = 2016

mlbgame.update.run(start="04-01-2016")

season_start_date = datetime(year, 04, 03)
today_date = datetime.today()


# Crappy way to map the month around
class Month:
    def __init__(self, name, id):
        self.name = name
        self.id = id

months = [Month("April", 4), Month("May", 5), Month("June", 6), Month("July", 7),
Month("August", 8), Month("September", 9)]

months_dict = {}
for month in months:
    months_dict[month.id] = month

class Player:
    def __init__(self, first_name, last_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.hrs = [0,0,0,0,0,0] #One for each month of the game
        self.hr_total = 0
        self.hr_series = Series()
        self.hr_total_series = Series()

    def __str__(self):
        return str.format('{0} : {1}', self.id, self.last_name)

    def __repr__(self):
        return self.__str__()

    def add_hrs(self, count, date):
        self.hr_total += count
        self.hr_total_series[date] = self.hr_series.sum() + count
        if(self.hr_series.last_valid_index() == date ):
            self.hr_series[date] = count + self.hr_series[date]
        else:
            self.hr_series[date] = count


    def name(self):
        return self.first_name + " " + self.last_name

    def get_player_hr_dataframe(self):
        return self.hr_series.to_frame(self.name())

    def get_player_hr_total_dataframe(self):
        return self.hr_total_series.to_frame(self.name())

players_dict = {}

#Hand mapped in these players -  ID comes from mlb.com player ID
#No Cannonical naming in a way I could trust to write code to match based upon name.
#This is obviously annoying for the future. Probably can build the data of all players
#in a programatic way in the future (create a CSV and map that in here rather 
#than do it by hand)
players = [Player("Bryce", "Harper", 547180),
Player("Mookie", "Betts", 605141),
Player("Miguel", "Sano", 593934),
Player("Randal", "Grichuk", 545341),
Player("George", "Springer", 543807),
Player("Rougned", "Odor", 596059),
Player("Jonathan", "Schoop", 570731),
Player("Giancarlo", "Stanton", 519317),
Player("Prince", "Fielder", 425902),
Player("Mark", "Trumbo", 444432),
Player("Carlos", "Correa", 621043),
Player("Miguel", "Cabrera", 408234),
Player("Kyle", "Schwarber", 656941),
Player("Maikel", "Franco", 596748),
Player("Kris", "Bryant", 592178),
Player("Nick", "Castellanos", 592206),
Player("Adam", "Jones", 430945),
Player("Ryan", "Zimmerman", 475582),
Player("Addison", "Russell", 608365)
]


for player in players:
    players_dict[player.id] = player

def create_multiplayer_hr_dataframe(players_dataframes):
    return pd.concat(players_dataframes, axis=1).fillna(value=0)

def create_multiplayer_hr_total_dataframe(players_dataframes):
    return pd.concat(players_dataframes, axis=1).fillna(method='ffill').fillna(value=0)

class User:
    def __init__(self, name, playerIds, players_dict):
        self.name = name
        self.playerIds = playerIds
        self.players = []
        for p in self.playerIds:
            self.players.append(players_dict[p])

    def players_hr_dataframe(self):
        dataframes = map(lambda p : p.get_player_hr_dataframe(), self.players)
        return create_multiplayer_hr_dataframe(dataframes)

    def players_hr_total_dataframe(self):
        dataframes = map(lambda p : p.get_player_hr_total_dataframe(), self.players)
        return create_multiplayer_hr_total_dataframe(dataframes)


#TODO: Take this mapping and make it read from a text file
users = [User("Dave", [519317, 425902, 444432, 621043, 408234, 656941, 596748], players_dict),
User("Craig", [547180, 605141, 593934, 545341, 543807, 596059, 570731], players_dict),
User("Brian", [519317, 592178, 425902, 593934, 408234, 656941, 592206], players_dict),
User("Jason", [519317, 430945, 592178, 593934, 475582, 656941, 608365], players_dict)]



for m in months:
    month = mlbgame.games(year, m.id)

    for games in month:
        for game in games:
            #Only games in the season (pre-season games will be included without this)
            #Also don't try to pull games that have not been played yet as the record
            #will exist but the call to get the stats will fail
            if game.date > season_start_date: # and game.date < today_date:
                #Try check is here because postponed games will still come through
                #Need to figure out if there is a way to deal with this actively rather than passively
                try:
                    stats = mlbgame.player_stats(game.game_id)
                    game_stats_all = mlbgame.combine_stats(stats)
                    for game_stats in game_stats_all:

                        if hasattr(game_stats, 'hr') and game_stats.id in players_dict:
                            p = players_dict[game_stats.id]
                            p.add_hrs(game_stats.hr, Period(game.date, freq='D'))
                            p.hrs[m.id - 4] += game_stats.hr #-4 to map April to 0 index this is a shitty way to do this

                except ValueError:
                    print("Game not found:", game.game_id)

# For debugging purposes, print out player totals
#for player in players:
#    print(player.first_name, player.last_name, player.hrs, "Total:", player.hr_total)


print()

def user_month_total(user, month):
    total = 0
    for p in user.playerIds:
        player = players_dict[p]
        total += player.hrs[month]
    return total

def user_total(user):
    total = 0
    for p in user.playerIds:
        player = players_dict[p]
        total += sum(player.hrs)
    return total


for user in users:
    print()
    print(user.name, user_month_total(user,0), user_month_total(user,1), user_month_total(user,2), user_month_total(user,3), user_month_total(user,4), user_month_total(user,5), "Total:",  user_total(user))
    for p in user.players:
        player = players_dict[p]
        print(player.first_name, player.last_name, player.hrs[0], player.hrs[1], player.hrs[2], player.hrs[3], player.hrs[4], player.hrs[5], "Total:", player.hr_total)




