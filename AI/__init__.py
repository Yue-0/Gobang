import AI.config as cfg
from AI.search import MiniMaxSearch


class AI(MiniMaxSearch):
    def __init__(self):
        super(AI, self).__init__(cfg.depth, cfg.breadth)
