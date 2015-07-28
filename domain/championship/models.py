from utils.graph import ReverseBinaryGraph

__author__ = 'msoum'


class ChampionshipModel:
    def __init__(self, team_list):
        self.graph = ReverseBinaryGraph(team_list)
