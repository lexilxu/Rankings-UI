import math
import pandas as pd
import numpy as np

class Rankings:
    """
        This class retrieves information from the ratings and rankings dataset.

        Attributes:
        -----
            rating_df (df): dataframe contains all ratings.
            ranking (df): dataframe contains all rankings.
            ties
            rating_names (list): list of the names of all sub ratings.
            onlyranks (bool): if true, only rankings data are included.
            reviewer_col_name (str): column name for reviewer names. Default is "Reviewer Name".
            prop_col_name (str): column name for proposal names. Default is "Proposal Name".
            overall_col_name (str): column name for the overall ratings. Default is "Overall Score".

        Methods:
        -----
            get_rating_df(rat_name):
                Returns the df that contains the overall rating.
            updated_pairs(dict, yesno, topk):
                Returns the
            get_name(email):
                Returns the name of the reviewer with the email.
            get_sub_rating(rat_name, reviewer, prop):
                Returns the sub rating of an item.
            get_all_sub_ratings():
                Returns the list of all the names of the sub ratings.
            get_columns():
                Returns the proposal names.
            get_all_rankings(topk=None):
                Returns the rankings for the topk items.
            get_op_rankings():
                Returns the overall rankings as dictionary and the maximum length of the rankings.


    """
    def __init__(self, rating_df, ranking, ties, rating_names, onlyranks=False, reviewer_col_name="Reviewer Name", prop_col_name="Proposal Name", overall_col_name="Overall Score"):
        self.scores = rating_df
        self.ranking = ranking
        self.ties = ties
        self.rating_names = rating_names
        self.reviewer_col_name = reviewer_col_name
        self.overall_col_name = overall_col_name
        self.proposal_col_name = prop_col_name
        self.index = list(self.scores[self.reviewer_col_name].unique())
        self.columns = list(self.scores[self.proposal_col_name].unique())
        self.num_papers = len(self.columns)
        if onlyranks:
            self.overall_col_name = "OP"


    def get_rating_df(self, rat_name):
        """
            Returns the df that contains the overall rating.

            Parameters:
                rat_name (str): Name of the sub rating.

            Returns:
                df (pandas.DataFrame): Dataframe containing the overall rating.
        """
        df = pd.DataFrame(index=self.scores[self.reviewer_col_name].unique(), columns=self.scores[self.proposal_col_name].unique())
        for index in self.index:
            for column in self.columns:
                df.loc[index, column] = self.get_sub_rating(rat_name, index, column)
        return df

    def updated_pairs(self, dict, yesno, topk):
        """

        """
        df = self.scores.copy()
        if dict is not None:
            for key in dict.keys():
                df = df[(dict[key][0] <= df[key]) & (df[key] <= dict[key][1])]
        if yesno is not None:
            for key in yesno.keys():
                df = df[(df[key] == yesno[key])]
        df = df[[self.reviewer_col_name, self.proposal_col_name]]
        dict_r = self.get_all_rankings(topk=topk)
        rank_list = [(i,x) for i in dict_r for x in dict_r[i]]
        filter_list = list(df.itertuples(index=False, name=None))
        return list(set(rank_list).intersection(set(filter_list)))


    # seems not used
    def get_name(self, email):
        """
            Returns the name of the reviewer with the email.
        """
        return self.scores.loc[self.scores["Reviewer Email"] == email, self.reviewer_col_name].iloc[0]

    def get_sub_rating(self, rat_name, reviewer, prop):
        """
            Returns the sub rating of an item as a string.
        """
        l = self.scores.loc[(self.scores[self.reviewer_col_name] == reviewer) & (self.scores[self.proposal_col_name] == prop), rat_name].tolist()
        if l:
            return str(math.floor(l[0]))
        else:
            return np.nan

    def get_all_sub_ratings(self):
        """
            Returns the list of all the names of the sub ratings.
        """
        return list(self.rating_names)

    def get_columns(self):
        """
            Returns the proposal names.
        """
        return list(self.index)

    def get_all_rankings(self, topk=None):
        """
            Returns the rankings for the topk items.

            Parameters:
                topk (int, optional): number of top items included.
        """
        ranking = self.ranking.copy()
        for key in self.index:
            papers = ranking[key]
            temp = papers
            for i in range(len(papers)):
                temp[i] = self.columns[int(papers[i])]
            ranking[key] = temp
        ret = {}
        for key in self.index:
            papers = self.ranking[key]
            selected = papers
            if topk is not None:
                selected = papers[:topk]
                if self.ties is not None:
                    for tie in self.ties[key]:
                        for i in range(len(tie)):
                            if selected[-1] == tie[i]:
                                for other in tie:
                                    if other not in selected:
                                        selected.append(other)
                                break
            ret[key] = selected
        return ret

    def get_op_rankings(self):
        """
            Returns the overall rankings as dictionary and the maximum length of the rankings.
        """
        df_op = self.get_rating_df(self.overall_col_name)
        ret = {}
        rows = list(self.index)
        props = list(self.columns)
        maxi = 0
        for reviewer in rows:
            ret[reviewer] = {}
            for prop in props:
                rate = df_op.loc[reviewer, prop]
                if not pd.isna(rate):
                    if rate not in ret[reviewer]:
                        ret[reviewer][rate] = [prop]
                    else:
                        ret[reviewer][rate].append(prop)
                        if len(ret[reviewer][rate]) > maxi:
                            maxi = len(ret[reviewer][rate])
        return ret, maxi