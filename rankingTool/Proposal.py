import pandas as pd

class Proposals:
    """
        Proposal details.
    """
    def __init__(self, df) -> None:
        self.df = df
    
    def get_detail(self, prop_name):
        return "NaN"