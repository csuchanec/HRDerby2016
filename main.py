from __future__ import print_function
import mlbgame
import mlbgame.update

class Player:
    def __init__(self, first_name, last_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.hrs = []
        self.hr_total = 0

    def add_hrs(hrs):
        self.hr_total += hrs

    def name():
        return first_name + " " + last_name

players_dict = {}

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
Player("Maikel", "Franko", 596748),
Player("Kris", "Bryant", 592178),
Player("Nick", "Castellanos", 592206),
Player("Adam", "Jones", 430945),
Player("Ryan", "Zimmerman", 475582),
Player("Addison", "Russell", 608365)
]


for player in players:
    players_dict[player.id] = player

print(players_dict.keys())
print('Hello World!')
mlbgame.update.run(start="01-01-2016")
print('here')


month = mlbgame.games(2016, 4)

for games in month:
    for game in games:
        try:
            stats = mlbgame.player_stats(game.game_id)
            game_stats_all = mlbgame.combine_stats(stats)
            for game_stats in game_stats_all:
                try:
                    #print(game_stats.id, game_stats.name)
                    players_dict[game_stats.id].hr_total += game_stats.hr
                except KeyError:
                    x = 1

        except AttributeError:
            print('error')
        except ValueError:
            y = 1

for player in players:
    print(player.first_name, player.last_name, ":", player.hr_total)


