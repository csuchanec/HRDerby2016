
from pandas import DataFrame, Series, Panel
import inspect

class Player2:
    def __init__(self, first_name, last_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.batting_stats_df = DataFrame(columns=["at_bats", "avg", "hits",
            "runs", "rbi", "hr", "slg", "obp", "ops", "fldg", "batting_order",
            "bb", "sb", "cs", "e", "hbp", "so", "sac", "sf", "lob", "fly_outs",
            "put_outs", "assists", "ground_outs", "season_hits", "season_runs", "season_hr", "season_rbi",
            "season_so", "season_bb", "d", "t"])
        self.pitching_stats_df = DataFrame(columns=[ "hits", "runs",
            "hr", "bb", "so", "season_hits", "season_runs", "season_hr",
            "season_so", "season_bb", "loses", "wins", "saves",
            "er", "hold", "blown_saves", "outs_recorded", "batters_faced",
            "game_score", "era", "num_pitches", "win", "loss", "save",  "season_er",
            "season_ip", "s"])



    def __str__(self):
        return str.format('{0} : {1}', self.id, self.last_name)

    def __repr__(self):
        return self.__str__()

    def add_stats(self, stats, date):
        if(hasattr(stats, 'ab') ):
            self.add_batting_stats(stats, date)
        else :
            self.add_pitching_stats(stats, date)

    def add_pitching_stats(self, stats, date):
        win = 1 if (hasattr(stats, 'win') and  stats.win ) else 0
        loss = 1 if (hasattr(stats, 'loss') and  stats.loss ) else 0
        save = 1 if (hasattr(stats, 'save') and  stats.save ) else 0
        seaason_hr = stats.s_hr  if (hasattr(stats, 's_hr')) else 0
        note = stats.note if(hasattr(stats, 'note')) else ''

        if(not self.pitching_stats_df.empty and self.pitching_stats_df.last_valid_index() == date ):
            print('same day', date )

            self.pitching_stats_df.loc[date] = [
            stats.h + self.pitching_stats_df.loc[date, 'hits']  , stats.r + self.pitching_stats_df.loc[date, 'runs'] , 
            stats.hr + self.pitching_stats_df.loc[date, 'hr'] ,
            stats.bb + self.pitching_stats_df.loc[date, 'bb'] ,
            stats.so + self.pitching_stats_df.loc[date, 'so'] , 
            stats.s_h, stats.s_r, seaason_hr,  stats.s_so, stats.s_bb,
            stats.l, stats.w, stats.sv, stats.er + self.pitching_stats_df.loc[date, 'er'] ,
            stats.hld + self.pitching_stats_df.loc[date, 'hold'] , stats.bs + self.pitching_stats_df.loc[date, 'blown_saves'] ,
            stats.out + self.pitching_stats_df.loc[date, 'outs_recorded'] , stats.bf + self.pitching_stats_df.loc[date, 'batters_faced'] ,
            (stats.game_score + self.pitching_stats_df.loc[date, 'game_score'])/2 , stats.era,
            stats.np + self.pitching_stats_df.loc[date, 'num_pitches'] , win + self.pitching_stats_df.loc[date, 'win'] ,
            loss + self.pitching_stats_df.loc[date, 'loss'] , save + self.pitching_stats_df.loc[date, 'save'] ,
            stats.s_er, stats.s_ip, stats.s + self.pitching_stats_df.loc[date, 's'] ]
        else:
            self.pitching_stats_df.loc[date] = [stats.h, stats.r, 
            stats.hr, stats.bb, stats.so, stats.s_h, stats.s_r, seaason_hr, stats.s_so,
            stats.s_bb, stats.l, stats.w, stats.sv, stats.er, stats.hld, stats.bs,
            stats.out, stats.bf, stats.game_score, stats.era, stats.np, win, loss,
            save, stats.s_er, stats.s_ip, stats.s]

    def add_batting_stats(self, stats, date):
        go = stats.go   if (hasattr(stats, 'go')) else 0
        bo = stats.bo   if (hasattr(stats, 'bo')) else 0
        slg = stats.slg if(hasattr(stats, 'slg')) else 0
        obp = stats.obp if(hasattr(stats, 'obp')) else 0
        ops = stats.ops if(hasattr(stats, 'ops')) else 0

        if(not self.batting_stats_df.empty and self.batting_stats_df.last_valid_index() == date ):
            print('same day', date )

            self.batting_stats_df.loc[date] = [self.batting_stats_df.loc[date, 'at_bats'] + stats.ab, 
            stats.avg, stats.h + self.batting_stats_df.loc[date, 'hits']  , stats.r + self.batting_stats_df.loc[date, 'runs'] , 
            stats.rbi + self.batting_stats_df.loc[date, 'rbi'] , stats.hr + self.batting_stats_df.loc[date, 'hr'] ,
            slg, obp, ops, (stats.fldg + self.batting_stats_df.loc[date, 'fldg'])/2, bo, stats.bb + self.batting_stats_df.loc[date, 'bb'] ,
            stats.sb + self.batting_stats_df.loc[date, 'sb'] , stats.cs  + self.batting_stats_df.loc[date, 'cs'] ,
            stats.e + self.batting_stats_df.loc[date, 'e'] , stats.hbp + self.batting_stats_df.loc[date, 'hbp'] ,
            stats.so + self.batting_stats_df.loc[date, 'so'] , stats.sac + self.batting_stats_df.loc[date, 'sac'] , 
            stats.sf + self.batting_stats_df.loc[date, 'sf'] , stats.lob + self.batting_stats_df.loc[date, 'lob'], 
            stats.ao + self.batting_stats_df.loc[date, 'fly_outs'] , stats.po + self.batting_stats_df.loc[date, 'put_outs'] ,
            stats.a + self.batting_stats_df.loc[date, 'assists'] , go + self.batting_stats_df.loc[date, 'ground_outs'] ,
            stats.s_h, stats.s_r, stats.s_hr, stats.s_rbi, stats.s_so, stats.s_bb,
            stats.d + self.batting_stats_df.loc[date, 'd'] , stats.t + self.batting_stats_df.loc[date, 't'] ]
        else:
            self.batting_stats_df.loc[date] = [stats.ab, stats.avg, stats.h, stats.r, 
            stats.rbi, stats.hr, slg, obp, ops, stats.fldg, bo, stats.bb,
            stats.sb, stats.cs, stats.e, stats.hbp, stats.so, stats.sac, stats.sf, stats.lob,
            stats.ao, stats.po, stats.a, go, stats.s_h, stats.s_r, stats.s_hr, stats.s_rbi, stats.s_so,
            stats.s_bb, stats.d, stats.t]

    def name(self):
        return self.first_name + " " + self.last_name

