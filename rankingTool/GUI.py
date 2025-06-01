import tkinter

from .proposal_box import Proposal_Box
from .legend_window import legend_window
from .Census import census_window
from .filter import filter_window
from .Ranking import Rankings
from .Review import Reviews
from .Reviewer import Reviewers
from .Summary import Summary
from .Proposal import Proposals
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys
import numpy as np
import toml
import pandas as pd

class GUI:
    """
        A class to represent a GUI.

        ...
        Attributes
        ----------
        configs_path (str):
            Path to the configuration file (toml format).

        Methods
        -------
        load_data_window():
            Window for loading the data
        load_excel_data(path):
            Load Excel file/.csv files from the path the user selected.
        show_results():
            Organize data with modules Rankings, Reviews, Reviewers, Proposals.
            Then display the UI with the items.
        show_performance_summary():
            Open the performance summary window.
        update_summary():
            Update the results to the summary window.
        show_average_rankings():
            Show a column of average rankings for item next to the concensus rankings results.
        display_rankings_window():
            Open the window to compute consensus rankings.
        hide_rankings_window():
            Hide the window temporarily with the results saved.
        init_tied_rect():
            Deal with tied items by drawing black rectangles.
        init_number():
            Draw lines on the initial canvas.
        get_all_pos():
            Get coordinates for item boxes.
        get_central_pos():
            Get coordinates for concensus rankings.
        display_rankings():
            Display concensus rankings computed by the most recent model.
        get_dash(reviewer, prop):
            Get the corresponding dash type for an item box (reviewer, prop).
        get_outline(reviewer, prop):
            Get the outline type for an item box (reviewer, prop).
        get_width(reviewer, prop):
            Get the width of the outline for an item box (reviewer, prop).
        initial_canvas():
            Draw the initial canvas with item boxes.
        selectItem(event):
            Single click an item and boxes of the same candidate will darken.
        swap_left(event):
            Swap the column with the column on its left.
        get_box_color(reviewer, prop):
            Get the background color for an item box (reviewer, prop).
        closeWindow():
            Destroy the root upon closing the window.
        do_popup(event):
            Open menu opend when right-clicking an item box.
        legend_sub():
            Window for the legend.
        update_all_rects(res):
            Update items when assignments of the attributes are changed.
        filter_ratings(filter_dict, yesno_dict, topk):
            Filter the items and change the canvas when the filter is employed.
        change_attribute():
            Window for changing the assignments of the attributes.
        filter_rect():
            Window for the filter.
        rating_detail(reviewer, prop):
            Show all the sub-ratings for an item.
        proposal_detail(prop):
            Show the details of a proposal.
        child_window_prop(title, text):
            Pop-up window for details of the proposal.
        show_width(event):
            Show the position of the mouse relative to the item.
        child_window_ratings(name, reviewer, proposal):
            Pop-up window for sub ratings.
        review_text(reviewer, proposal_name):
            Display the window for reviews.
        child_window_review(title, list_reviews, list_review_titles):
            Open the window for text review details.
        set_up():
            Set up all commands on the main canvas.
        ret_colors():
            Color the selected proposal boxes.
        show():
            Display the GUI.
    """

    def __init__(self, configs_path):
        """
            Initialize the GUI

            Retrieve the configurations from the configs_path file.
            Initialize the canvas, scrollbar.
            Open the window for loading data.

                Parameters:
                    configs_path (str):
                        Path to the configuration file (toml format).
        """

        configs = toml.load(configs_path)
        self.name = configs["default"]["name"]
        self.attr_to_rat = configs["graphic_to_rating"]
        self.rat_min = configs["default"]["rat_min"]
        self.rat_max = configs["default"]["rat_max"]
        self.LEN_SHORT_NAME = configs["default"]["num_str"]
        self.default_grap_attr = configs["default_graphic_attributes"]
        self.box_color_dict = configs['box_graph_attributes']["color"]
        self.outline_dict = configs['box_graph_attributes']["outline"]
        self.width_dict = configs['box_graph_attributes']["width"]
        self.dash_dict = configs['box_graph_attributes']["dash"]
        self.box_width = configs["box_size"]["box_width"]
        self.box_height = configs["box_size"]["box_height"]
        self.box_distance_x = configs["box_size"]["box_distance_x"]
        self.box_distance_y = configs["box_size"]["box_distance_y"]
        self.yesno_list = configs["filter"]["yesno_list"]
        self.overall_merit_max = configs["default"]["overall_merit_max"]
        self.overall_merit_min = configs["default"]["overall_merit_min"]
        self.ranking_area_x = configs["box_size"]["ranking_area_x"]


        self.root = Tk()
        self.root.title(self.name)
        screen_height = self.root.winfo_screenheight()
        y = int(round((screen_height/2) - (700/2)))
        self.root.geometry(f'800x700+100+{str(y)}')
        self.root['bg'] = '#AC99F2' # Background Color of the entire UI
        s = ttk.Style()
        s.theme_use('clam')

        # Set Scroll Bar
        self.scrlbar2 = ttk.Scrollbar(self.root)
        self.scrlbar2.pack(side="right", fill="y")
        self.scrlbar = ttk.Scrollbar(self.root, orient ='horizontal')
        self.scrlbar.pack(side="bottom", fill="x")


        # Update Scroll region later
        self.canvas = Canvas(self.root, width=1600, height=700, bg="white", yscrollcommand=self.scrlbar2.set,
                             xscrollcommand=self.scrlbar.set,confine=False, scrollregion=(0,0,2000,1000))
        self.rate_range = range(self.rat_min, self.rat_max+1)
        self.filter_dict = {}
        self.tied_rect = []

        self.scrlbar2.config(command=self.canvas.yview)
        self.scrlbar.config(command=self.canvas.xview)
        self.canvas.pack()

        self.set_up()
        self.census = None

        self.load_data_window()


    def load_data_window(self):
        """
            Window for loading data in to the GUI.

            Open the window. Add the menu for selecting file type and data type.
            Button for browsing the computer and selecting file path.

            Methods
            -------
            browsefunc():
                Function for browsing the computer for path selection.
        """
        def browsefunc():
            """
                Widget for browsing files and selecting file(s) for loading.
            """
            w = 400
            dy = 40
            if self.filetype.get() == ".xlsx/.xls":
                filename = filedialog.askopenfilename(title="Select a file",
                                                      filetypes=[("Excel files", ".xlsx .xls")])
            else:
                filename = filedialog.askdirectory(title="Select a directory for .csv files")

            self.input_path.set(filename)

            self.sub1_canvas.create_text((w // 2, 50 + 2 * dy), text="Data Selected!")
            # filepathText = Label(self.sub1_canvas, textvariable=self.input_path, width=int(w/4*3))
            # self.sub1_canvas.create_window((w // 2, 50 + 3 * dy), window=filepathText)

        self.root.withdraw()
        self.panel = Toplevel(self.root)
        self.panel.title('Please load data')
        self.panel.geometry('400x300+750+250')
        w = 400
        h = 300
        dy = 40

        self.sub1_canvas = Canvas(self.panel, width=w, height=h, bg="grey90")


        self.input_path = StringVar(self.sub1_canvas)
        self.filetype = StringVar(self.sub1_canvas)

        # Option menu for file type.
        self.filetype.set(".xlsx/.xls")
        select_filetype = OptionMenu(self.sub1_canvas, self.filetype,
                                   *[".xlsx/.xls", ".csv"])
        select_filetype.config(bg='grey90')
        self.sub1_canvas.create_window((w // 2, 50), window=select_filetype)

        # Button for selecting data file(s).
        loaddata_button = Button(self.sub1_canvas, text="Select data file(s)", command=browsefunc, highlightbackground='grey90')
        self.sub1_canvas.create_window((w // 2, 50 + dy), window=loaddata_button)

        # Option menu for data type ("Rankings only", "Ratings only", "Ratings and Rankings").
        self.datatype = StringVar(self.sub1_canvas)
        self.datatype.set("Ratings and Rankings")
        datatype_menu = OptionMenu(self.sub1_canvas, self.datatype,
                                   *["Rankings only", "Ratings only", "Ratings and Rankings"])
        datatype_menu.config(bg='grey90')
        self.sub1_canvas.create_window((w // 2, 50 + 3 * dy), window=datatype_menu)

        # Button for loading data -- leading to show_results.
        self.rankings_button = Button(self.sub1_canvas, text="Load data", command=self.show_results, highlightbackground='grey90')

        self.sub1_canvas.create_window((w // 2, 50 + 5 * dy), window=self.rankings_button)

        self.sub1_canvas.pack()



    def load_excel_data(self,path):
        """
            Organize the data into different dataframes for defining modules later.

            Parameters:
                path (string): path of the excel file (for ".xlsx/.xls" data type) or the directory for .csv files.

            Returns:
                score (df): dataframe with all the ratings. Columns include "Reviewer Name", "Proposal Name" and "OP" (overall ranking).
                props (df): dataframe with reviewer names and proposal names.
                reviewers (df): dataframe containing all the reviewer names.
                reviews (df): dataframe with all the text reviews. Columns include "Reviewer Name" and "Proposal Name".
                rankings_name: a dictionary of the names of the proposals, include two lists "long" and "short".
                rank_dict: a dictionary of the rankings using indices. Keys are each reviewer.
        """
        rankings_name = {}
        if self.filetype.get() == ".xlsx/.xls":
            xls = pd.ExcelFile(path)
            if self.datatype.get() == "Rankings only":
                rankings = pd.read_excel(xls, 'Rankings', index_col=None)
                rankings.columns = list(map(str,rankings.columns))
                scores = None
            elif self.datatype.get() == "Ratings only":
                rankings = None
                scores = pd.read_excel(xls, 'Scores', index_col=None)
            elif self.datatype.get() == "Ratings and Rankings":
                rankings = pd.read_excel(xls, 'Rankings', index_col=None)
                rankings.columns = list(map(str,rankings.columns))
                scores = pd.read_excel(xls, 'Scores', index_col=None)
            try:
                attributes = pd.read_excel(xls, 'Attributes', index_col=None)
            except:
                pass
        else:
            if self.datatype.get() == "Rankings only":
                rankings = pd.read_csv(path + 'Rankings.csv')
                scores = None
            elif self.datatype.get() == "Ratings only":
                scores = pd.read_csv(path + 'Scores.csv')
                rankings = None
            elif self.datatype.get() == "Ratings and Rankings":
                rankings = pd.read_csv(path + 'Rankings.csv')
                scores = pd.read_csv(path + 'Scores.csv')
            try:
                attributes = pd.read_csv(path + 'Attributes.csv')
            except:
                pass

        self.op_feature = True
        self.feature_names = {}
        self.info_names = {}
        review = {}

        if self.datatype.get() != "Rankings only":
            reviewer_names = list(scores.iloc[:, 1].unique())
            rankings_name['long'] = list(scores.iloc[:, 0].unique())
            reviewer_names = list(map(str, reviewer_names))
            rankings_name['long'] = list(map(str, rankings_name['long']))

            self.feature_names = attributes['Categories'][(attributes['Type'] == 'Ratings')]
            score = pd.DataFrame(columns=self.feature_names)
            score["OP"] = 0
            score["Reviewer Name"] = 0
            score["Proposal Name"] = 0
            ratings = {}
            N = len(reviewer_names)
            n = len(rankings_name['long'])
            # ratings - contain dataframes for each sub-rating
            for feature in self.feature_names:
                ratings[feature] = pd.DataFrame(columns=rankings_name['long'], index=reviewer_names)
                temp = scores[feature]
                for i in range(N):
                    ratings[feature].iloc[i] = temp.iloc[(i * n):((i + 1) * n)]

            self.op_feature = attributes['Categories'][(attributes['Type'] == 'Main')]
            for review_name in reviewer_names:
                for rank_name in rankings_name['long']:
                    dict = {}
                    for feature in self.feature_names:
                        dict.update({feature: ratings[feature].loc[review_name][rank_name]})
                    for feature in self.op_feature:
                        op_df = pd.DataFrame(columns=rankings_name['long'], index=reviewer_names)
                        temp = scores[feature]
                        for i in range(N):
                            op_df.iloc[i] = temp.iloc[(i * n):((i + 1) * n)]
                        dict.update({"OP": op_df.loc[review_name][rank_name]})
                    dict.update({"Reviewer Name": review_name})
                    dict.update({"Proposal Name": rank_name})
                    score = pd.concat([score, pd.DataFrame([dict])], ignore_index=True)

            props = score[["Reviewer Name", "Proposal Name"]].copy()
            reviewers = score[["Reviewer Name"]].copy()

            self.info_names = attributes['Categories'][attributes['Type'] == 'Text'].to_list()
            infos = {}
            review = pd.DataFrame(columns=self.info_names)
            review["Reviewer Name"] = 0
            review["Proposal Name"] = 0
            for feature in self.info_names:
                infos[feature] = pd.DataFrame(columns=rankings_name['long'], index=reviewer_names)
                temp = scores[feature]
                for i in range(N):
                    infos[feature].iloc[i] = temp.iloc[(i * n):((i + 1) * n)]

                for review_name in reviewer_names:
                    for rank_name in rankings_name['long']:
                        dict = {}
                        for feature in self.info_names:
                            dict.update({feature: infos[feature].loc[review_name][rank_name]})
                        dict.update({"Reviewer Name": review_name})
                        dict.update({"Proposal Name": rank_name})
                        review = pd.concat([review, pd.DataFrame([dict])], ignore_index=True)
        else:
            reviewer_names = rankings.columns.tolist()
            reviewer_names = list(map(str, reviewer_names))
            rankings_name['long'] = list(rankings.iloc[:, 0].unique())
            rankings_name['long'] = list(map(str, rankings_name['long']))
            N = len(reviewer_names)
            n = len(rankings_name['long'])
            props = pd.DataFrame(columns=["Reviewer Name", "Proposal Name"])
            reviewers = pd.DataFrame(columns=["Reviewer Name"])


            score = pd.DataFrame(columns=["Reviewer Name","Proposal Name","OP"])

            for review_name in reviewer_names:
                for rank_name in rankings_name['long']:
                    dict = {}
                    props = pd.concat([pd.DataFrame([[review_name, rank_name]], columns=props.columns), props],
                                      ignore_index=True)
                    reviewers = pd.concat([pd.DataFrame([[review_name]], columns=reviewers.columns), reviewers],
                                          ignore_index=True)
                    dict.update({"Reviewer Name": review_name})
                    dict.update({"Proposal Name": rank_name})
                    rank = rankings[review_name][rankings[review_name]==rank_name].index[0]
                    dict.update({"OP":rank})

                    score = pd.concat([score, pd.DataFrame([dict])], ignore_index=True)


        if self.datatype.get() != "Ratings only":
            rank_dict = {}
            for reviewer_name in reviewer_names:
                ordered_list = [None] * n
                for j in range(n):
                    ordered_list[j] = rankings_name['long'].index(rankings[reviewer_name][j])
                rank_dict[reviewer_name] = ordered_list

        else:
            rank_dict = {}

        rankings_name['short'] = [elem[:5] for elem in rankings_name['long']]
        return score, props, reviewers, review, rankings_name, rank_dict, None


    def show_results(self):
        """
            Load into modules Rankings, Reviews, Reviewers, Proposals and add buttons to the canvas.
        """
        score, props, reviewers, reviews, rankings_name, ret, ties = self.load_excel_data(self.input_path.get())
        if self.datatype.get() == "Rankings only":
            ranks = Rankings(score, ret, ties, rating_names=self.feature_names, onlyranks=True,overall_col_name="OP")
        else:
            ranks = Rankings(score, ret, ties, rating_names=self.feature_names, onlyranks=False,overall_col_name="OP")
        self.op_ratings = None
        self.op_rankings = None
        if self.datatype.get() == "Rankings only":
            self.op_rankings = pd.DataFrame.from_dict(ret,orient='index')
            self.op_rankings = self.op_rankings.add(1)
        else:
            reviewers = Reviewers(reviewers)
            reviews = Reviews(reviews, self.info_names)
            props = Proposals(props)
            self.reviewers = reviewers
            self.reviews = reviews
            self.props = props
            self.op_ratings = ranks.get_rating_df(ranks.overall_col_name)
            if self.datatype.get() == "Ratings and Rankings":
                self.op_rankings = pd.DataFrame.from_dict(ret,orient='index')
                self.op_rankings = self.op_rankings.add(1)

        self.rankings = ranks
        self.rankings_name = rankings_name
        self.columns = self.rankings.get_columns()
        self.ties = self.rankings.ties
        self.default_filter = {
            "topk": len(self.rankings.columns)
        }
        for rating in self.rankings.get_all_sub_ratings():
            self.filter_dict[rating] = self.rate_range
            self.default_filter[rating] = self.rate_range
        for yesno in self.yesno_list:
            self.default_filter[yesno] = "Yes"

        self.initial_canvas()
        self.init_number()
        self.init_tied_rect()

        yshift = 70

        # Buttons on canvas.
        self.rankings_button = ttk.Button(self.canvas, text="Compute consensus rankings",
                                      command=self.display_rankings_window)
        self.canvas.create_window(self.ranking_area_x // 3, yshift, window=self.rankings_button)
        self.rankings_hide_button = ttk.Button(self.canvas, text="Hide rankings window",
                                          command=self.hide_rankings_window)
        self.canvas.create_window(self.ranking_area_x * 2 // 3, yshift, window=self.rankings_hide_button)
        self.average_rankings_button = ttk.Button(self.canvas, text="Average ranking",
                                          command=self.show_average_rankings)
        self.canvas.create_window(self.ranking_area_x // 3, yshift + 50, window=self.average_rankings_button)
        self.performance_button = ttk.Button(self.canvas, text="Performance summary",
                                                  command=self.show_performance_summary)
        self.canvas.create_window(self.ranking_area_x * 2 // 3, yshift + 50, window=self.performance_button)

        if self.datatype.get() != "Rankings only":
            self.legend_sub()

        self.root.deiconify()
        self.panel.withdraw()


    def show_performance_summary(self):
        """
            Open the performance summary window.
        """
        self.summary = Summary(self.root, self.census)
        self.summary.show()

    def update_summary(self):
        """
            Update performance summary if new models are computed in the consensus rankings window.
        """
        self.summary.loadmodel( self.census.results)

    def show_average_rankings(self):
        """
            Show average ranking column on the main canvas (next to the consensus rankings window).
        """
        df = pd.read_csv(self.census.rankings_path.get(), header=None)
        average_rankings = df.mean(axis=0)
        min_ranking = df.min(axis=0)
        max_ranking = df.max(axis=0)

        self.get_central_pos()
        self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 - 10,
                                2.5 * self.box_height + 110,
                                text='Aver', font=("Comic Sans MS", 13))
        self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 + 40,
                                2.5 * self.box_height + 110,
                                text='Min ', font=("Comic Sans MS", 13))
        self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 + 90,
                                2.5 * self.box_height + 110,
                                text='Max ', font=("Comic Sans MS", 13))

        for i in range(len(self.cen_rankings)):
            self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 - 10,
                                    2.5 * self.box_height + 140 + i * (self.box_height + self.box_distance_y * 2),
                                    text=f"{round(average_rankings[self.rankings_name['long'].index(self.cen_rankings[i])],2)}", font=("Comic Sans MS", 13))
            self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 + 40,
                                    2.5 * self.box_height + 140 + i * (self.box_height + self.box_distance_y * 2),
                                    text=f"{round(min_ranking[self.rankings_name['long'].index(self.cen_rankings[i])], 2)}",
                                    font=("Comic Sans MS", 13))
            self.canvas.create_text(self.ranking_area_x // 3 + 5 * self.box_width // 8 + 90,
                                    2.5 * self.box_height + 140 + i * (self.box_height + self.box_distance_y * 2),
                                    text=f"{round(max_ranking[self.rankings_name['long'].index(self.cen_rankings[i])], 2)}",
                                    font=("Comic Sans MS", 13))


    def display_rankings_window(self):
        """
            Open the consensus rankings window.
        """
        if self.census is None:
            self.census = census_window(self.root, self, self.rankings_name,ratings=self.op_ratings, rankings=self.op_rankings)
            self.census.show()
        else:
            self.census.reshow()

    def hide_rankings_window(self):
        """
            Hide the consensus rankings window (temporarily).
        """
        if self.census is not None:
            self.census.hide()

    def init_tied_rect(self):
        """
            Draw black boxes around items that are tied in overall rating.
        """
        if self.ties is not None:
            for reviewer in self.ties.keys():
                for tie in self.ties[reviewer]:
                    y0_f = np.inf
                    y1_f = -np.inf
                    x0_f = 0
                    x1_f = 0
                    for paper in tie:
                        x0_f, x1_f, y0, y1 = self.pos[(reviewer, paper)]
                        if y0 < y0_f:
                            y0_f = y0
                        if y1 > y1_f:
                            y1_f = y1
                    self.canvas.create_rectangle(self.ranking_area_x + x0_f-self.box_distance_x*1/3, y0_f-self.box_distance_y*1/3, self.ranking_area_x + x1_f+self.box_distance_x*1/3, y1_f+self.box_distance_y*1/3, tag=(f"{reviewer}tie", ), outline="black")

    def init_number(self):
        """
            Draw lines on initial canvas and add texts.
        """
        self.canvas.create_text(self.ranking_area_x // 2, 12, text="consensus ranking", font=("Comic Sans MS", 15), fill="black")
        if self.datatype.get() == "Rankings only":
            self.canvas.create_text(self.ranking_area_x + 20, 12, text="Rankings", font=("Comic Sans MS", 15),fill="black")
        else:
            self.canvas.create_text(self.ranking_area_x + 20, 12, text="Ratings", font=("Comic Sans MS", 15),fill="black")

        for i in range(self.overall_merit_max - self.overall_merit_min + 1):
            y0 = self.lines_pos[i][1]
            y1 = self.lines_pos[i+1][1]
            self.canvas.create_text(self.ranking_area_x + 15,(y0+y1)//2, text=str(self.overall_merit_max-i), font=("Comic Sans MS", 25),fill="black")

        #self.canvas.create_text(15,(y0+y1)//2,  text="Ranking", font=("Comic Sans MS", 15), fill="black")


    def get_all_pos(self):
        """
            Get the coordinates for all item boxes.
        """
        op_dict, num_most = self.rankings.get_op_rankings()
        self.pos = {}
        self.rankpos = {}
        keys = list(op_dict.keys())
        delta_x = 0
        for i in range(len(keys)):
            rates = list(op_dict[keys[i]].keys())
            for j in range(len(rates)):
                rate = int(rates[j])
                self.rankpos[keys[i]] = (self.ranking_area_x + 50 + i*self.box_width+i*self.box_distance_x+delta_x, self.ranking_area_x + 50+(i+1)*self.box_width+i*self.box_distance_x+delta_x,
                                          2 * self.box_height + (self.overall_merit_max - rate) * (self.box_height + self.box_distance_y) * num_most + (len(op_dict[keys[i]][rates[j]]) + 1) * (self.box_height + self.box_distance_y) + (self.overall_merit_max - rate) * self.box_distance_y,
                                          3 * self.box_height + (self.overall_merit_max - rate) * (self.box_height + self.box_distance_y) * num_most + (len(op_dict[keys[i]][rates[j]]) + 1) * (self.box_height + self.box_distance_y) + (self.overall_merit_max - rate) * self.box_distance_y)
                for k in range(len(op_dict[keys[i]][rates[j]])):
                    self.pos[keys[i], op_dict[keys[i]][rates[j]][k]] = (self.ranking_area_x + 50+i*self.box_width+i*self.box_distance_x+delta_x, self.ranking_area_x + 50+(i+1)*self.box_width+i*self.box_distance_x+delta_x,
                                2*self.box_height+(self.overall_merit_max-rate)*(self.box_height+self.box_distance_y)*num_most+k*(self.box_height+self.box_distance_y)+(self.overall_merit_max-rate)*self.box_distance_y,
                                3*self.box_height+(self.overall_merit_max-rate)*(self.box_height+self.box_distance_y)*num_most+k*(self.box_height+self.box_distance_y)+(self.overall_merit_max-rate)*self.box_distance_y)

        self.lines_pos = []
        self.ver_lin_pos = []
        for rate in range(self.overall_merit_max-self.overall_merit_min+2):
            self.lines_pos.append((self.ranking_area_x, self.box_distance_y+self.box_height+rate*(self.box_height+self.box_distance_y)*num_most+rate*self.box_distance_y, self.ranking_area_x + len(keys)*270, self.box_distance_y+self.box_height+rate*(self.box_height+self.box_distance_y)*num_most+rate*self.box_distance_y))
            
        for i in range(len(self.columns)):
            self.ver_lin_pos.append((self.ranking_area_x + i*self.box_width+50+i*self.box_distance_x, 0, self.ranking_area_x + i*self.box_width+50+i*self.box_distance_x, 2200))
            self.ver_lin_pos.append((self.ranking_area_x + (i+1)*self.box_width+50+i*self.box_distance_x, 0, self.ranking_area_x + (i+1)*self.box_width+50+i*self.box_distance_x, 2200))

    def get_central_pos(self):
        """
            Get the coordinates for the concensus rankings boxes.
        """
        self.central_pos = []
        for i in range(len(self.cen_rankings)):
                self.central_pos.append((self.ranking_area_x // 3 - self.box_width // 2 - 30,
                               self.ranking_area_x // 3 + self.box_width // 2 - 30,
                               2 * self.box_height + 140 + i * (
                                self.box_height + self.box_distance_y*2),
                               3 * self.box_height + 140 + i * (
                                self.box_height + self.box_distance_y*2)))

    def display_rankings(self):
        """
            Display the consensus rankings from the most recent model computed.
        """
        self.get_central_pos()
        for i in range(len(self.cen_rankings)):
            #self.canvas.create_text(self.ranking_area_x // 2 - 5 * self.box_width // 8 - 30,
            #                        2.5 * self.box_height + 100 + i * (self.box_height + self.box_distance_y*2),
            #                        text = f'{i+1}', font=("Comic Sans MS", 13))
            Proposal_Box(self.canvas, reviewer=None, pos=self.central_pos[i], prop=self.cen_rankings[i], type="central")

    def get_dash(self, reviewer, prop):
        """
            Get the corresponding dash type for an item.

            Parameters:
                reviewer (str): name of reviewer.
                prop (str): name of proposal.

            Returns:
                str: dash type
        """
        if self.attr_to_rat["Dash"] == "None" or self.datatype.get() == "Rankings only":
            return self.default_grap_attr["dash"]
        rating = self.rankings.get_sub_rating(self.attr_to_rat["Dash"], reviewer, prop)
        return self.dash_dict[rating]

    def get_outline(self, reviewer, prop):
        """
            Get the corresponding outline color for an item (from configurations).

            Parameters:
                reviewer (str): name of reviewer.
                prop (str): name of proposal.

            Returns:
                str: outline color
        """
        if self.attr_to_rat["Outline"] == "None" or self.datatype.get() == "Rankings only":
            return self.default_grap_attr["outline"]
        rating = self.rankings.get_sub_rating(self.attr_to_rat["Outline"], reviewer, prop)
        return self.outline_dict[rating]

    def get_width(self, reviewer, prop):
        """
            Get the corresponding outline width for an item (from configurations).

            Parameters:
                reviewer (str): name of reviewer.
                prop (str): name of proposal.

            Returns:
                str: outline width
        """
        if self.attr_to_rat["Width"] == "None" or self.datatype.get() == "Rankings only":
            return self.default_grap_attr["width"]
        rating = self.rankings.get_sub_rating(self.attr_to_rat["Width"], reviewer, prop)
        return self.width_dict[rating]

    def get_box_color(self, reviewer, proposal):
        """
            returns the color of a given proposal box based on its FQ ranking (from configurations).

            Parameters:
                reviewer (str): name of reviewer.
                prop (str): name of proposal.

            Returns:
                str: box color.
        """
        if not self.attr_to_rat["Box_Background_Color"] or self.datatype.get() == "Rankings only":
            return self.default_grap_attr["color"]
        return self.box_color_dict[self.rankings.get_sub_rating(self.attr_to_rat["Box_Background_Color"],reviewer, proposal)]

    def initial_canvas(self):
        """
            Draws the initial canvas with all the items using Proposal_Box.
            Including the background colors.
        """
        if self.datatype.get() == "Rankings only":
            self.overall_merit_max = len(self.columns)
            self.overall_merit_min = 1
        else:
            col_name = self.rankings.overall_col_name
            main = self.rankings.get_rating_df(col_name)
            self.overall_merit_max = main.to_numpy().max()
            self.overall_merit_min = main.to_numpy().min()
            self.overall_merit_max = int(self.overall_merit_max)
            self.overall_merit_min = int(self.overall_merit_min)
        self.get_all_pos()
        self.prop_boxes = []
        k = 0
        blockcolor = ["azure", "ghost white"]
        for line in self.lines_pos:
            self.canvas.create_line(line[0], line[1], line[2], line[3], width=1.5, fill="gray90")
            if k != 0:
                self.canvas.create_rectangle(line[0], line[1], oline[2], oline[3], fill = blockcolor[k % 2], outline='')
            else:
                self.canvas.create_rectangle(0, 0, line[2], line[3], fill="gray90", outline='')
            oline = line
            k += 1

        for i in range(len(self.columns)):
            box = Proposal_Box(self.canvas, reviewer=self.columns[i], pos=(self.ranking_area_x + i*self.box_width+50+i*self.box_distance_x, self.ranking_area_x + (i+1)*self.box_width+50+i*self.box_distance_x, 0, self.box_height))
        for pair in self.pos.keys():   
            color = self.get_box_color(pair[0], pair[1])
            dash = self.get_dash(pair[0], pair[1])
            outline = self.get_outline(pair[0], pair[1])
            width = self.get_width(pair[0], pair[1])
            box = Proposal_Box(self.canvas, pair[0], self.pos[pair], pair[1], color, dash, outline, width)
            self.prop_boxes.append(box)



    def selectItem(self, event):
        """
            Select item boxes of the same proposal and darken them.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        item = self.canvas.find_closest(x, y)
        _type = self.canvas.type(item)
        if _type != "rectangle":
            item  = (item[0]-1, )
        tags = self.canvas.gettags(item)
        if len(tags) >= 2 and tags[1] != "current":
            prop = tags[1]
            self.canvas.itemconfig(prop, fill='Slategray4')

    def swap_left(self, event):
        """
            Swap the entire selected column (for each reviewer) with the column on its left.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if y <= self.box_height:
            item = self.canvas.find_closest(x, y, halo=2)
            _type = self.canvas.type(item)
            if _type != "rectangle":
                item  = (item[0]-1, )
            tags = self.canvas.gettags(item)
            cur_rev = tags[0]
            index = self.columns.index(cur_rev)
            if index != 0:  
                left_rev = self.columns[index-1]
                self.canvas.move(left_rev, self.box_width+self.box_distance_x, 0)
                self.canvas.move(cur_rev+"text", -(self.box_width+self.box_distance_x), 0)
                self.canvas.move(left_rev+"text", self.box_width+self.box_distance_x, 0)
                self.canvas.move(cur_rev, -(self.box_width+self.box_distance_x), 0)
                self.canvas.move(cur_rev+"tie", -(self.box_width+self.box_distance_x), 0)
                self.canvas.move(left_rev+"tie", self.box_width+self.box_distance_x, 0)
                self.columns[index] = left_rev
                self.columns[index-1] = cur_rev

    def do_popup(self, event):
        """
            Pop out a menu when right-clicking an item with
                Filter: filtering for items;
                Rating Details: show sub-ratings of the item;
                Review Text: show review text of the item;
                Proposal Details: show details of the proposal;
                Exit: close the window.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        item = self.canvas.find_closest(x, y, halo=2)
        _type = self.canvas.type(item)
        if _type != "rectangle":
            item  = (item[0]-1, )
        tags = self.canvas.gettags(item)

        self.popup = Menu(self.root, tearoff=0)
        
        self.popup.add_command(label="Filter", command=lambda: self.filter_rect())
        self.popup.add_separator()
        if len(tags) >= 2 and self.datatype.get()!="Rankings only":
            reviewer = tags[0]
            prop = tags[1]
            self.popup.add_command(label="Rating Details", command=lambda: self.rating_detail(reviewer, prop))
            self.popup.add_command(label="Review Text", command=lambda: self.review_text(reviewer, prop))
            self.popup.add_command(label="Proposal Details", command=lambda: self.proposal_detail(prop))

        self.popup.add_separator()
        self.popup.add_command(label="Exit", command=lambda: self.closeWindow())
        try:
            self.popup.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup.grab_release()


    def legend_sub(self):
        """
            Legend window for the main canvas.
        """
        win2 = Toplevel(self.root)
        win2.title('Legends')
        win2.geometry('400x300+1250+250')
        w = 400
        h = 300
        x1 = 100
        x2 = 300
        dy = 30
        ini_y = 50
        self.sub_canvas = Canvas(win2, width=w, height=h, bg="white")
        keys = list(self.attr_to_rat.keys())
        self.sub_canvas.create_text(x1, ini_y, text="Graphical Attributes", font=("bold", 13), fill="black")
        self.sub_canvas.create_text(x2, ini_y, text="Ratings", font=("bold", 13), fill="black")
        for i in range(len(keys)):
            self.sub_canvas.create_text(x1, (i+1)*dy+ini_y, text=keys[i], tags=(f"{keys[i]}"), fill="black")
            self.sub_canvas.create_text(x2, (i+1)*dy+ini_y, text=self.attr_to_rat[keys[i]], tags=(f"{keys[i]}"), fill="black")
        # Button Change Graphical Attributes
        change_button = Button(win2, text="Change Graphical Attributes",  command=self.change_attribute)
        change_button.pack()
        self.sub_canvas.pack()


        def legend_subsub(event):
            """
                Show details for each attribute.(sub-window)
            """
            x = self.sub_canvas.canvasx(event.x)
            y = self.sub_canvas.canvasy(event.y)
            item = self.sub_canvas.find_closest(x, y)
            grap_attr = self.sub_canvas.gettags(item)[0]
            if grap_attr == "Bands":
                title = grap_attr       
                dic = {}         
                for i in range(self.rat_max, self.rat_min-1, -1):
                    dic[i] = f"Vertical Separate Bands Of {i}"
                win3 = Toplevel(self.root)
                win3.title(title)
                win3.geometry('400x300+1400+250')
                w = 400
                h = 300
                x1 = 50
                x2 = 150
                dy = 30
                ini_y = 15
                sub2_canvas = Canvas(win3, width=w, height=h, bg="white")
                for i in range(self.rat_max, self.rat_min-1, -1):
                    sub2_canvas.create_text(x1, (i+1)*dy+ini_y, text=i, fill="black")
                    sub2_canvas.create_text(x2, (i+1)*dy+ini_y, text=dic[i], fill="black")
                sub2_canvas.pack()
            else:
                title = grap_attr
                win3 = Toplevel(self.root)
                win3.title(title)
                win3.geometry('400x300')
                w = 400
                h = 300
                x1 = 50
                x2 = 150
                dy = 30
                ini_y = 15
                sub2_canvas = Canvas(win3, width=w, height=h, bg="white")
                fill = {}
                dash = {}
                outline = {}
                width = {}
                for i in range(self.rat_min, self.rat_max+1):
                    fill[str(i)] = None
                    dash[str(i)] = None
                    outline[str(i)] = None
                    width[str(i)] = None
                if grap_attr == "Box_Background_Color":
                    fill = self.box_color_dict
                elif grap_attr == "Dash":
                    dash = self.dash_dict
                elif grap_attr == "Outline":
                    outline = self.outline_dict
                elif grap_attr == "Width":
                    width = self.width_dict
                for i in range(self.rat_max, self.rat_min-1, -1):
                    sub2_canvas.create_text(x1, (i+1)*dy+ini_y, text=i, fill="black")
                    sub2_canvas.create_rectangle(x2, (i+1)*dy+ini_y, x2+0.4*self.box_width, (i+1)*dy+ini_y+self.box_height, 
                                                fill=fill[str(i)], dash=dash[str(i)], outline=outline[str(i)], width=width[str(i)])
                    #sub2_canvas.create_text(x2, (i+1)*dy+ini_y, text=dic[i])
                sub2_canvas.pack()
        self.sub_canvas.bind('<Double-1>', legend_subsub) 

    def update_all_rects(self, res):
        """
            Update all items on the canvas according to selected attributes.

            Parameters:
                res (dict): (updated) attributes to each item.
        """
        self.attr_to_rat = res
        for box in self.prop_boxes:
            reviewer, prop = box.get_reviewer_prop()
            color = self.get_box_color(reviewer, prop)
            dash = self.get_dash(reviewer, prop)
            outline = self.get_outline(reviewer, prop)
            width = self.get_width(reviewer, prop)
            box.update_rect(color, dash, outline, width)

    def filter_ratings(self, filter_dict, yesno_dict, topk):
        """
            Update items on the canvas according to the filter.

            Parameters:
                filter_dict (dict): dictionary of .
                yesno_dict (dict): dictionary of .
                topk (int): number of top items to display.
        """
        for rating in filter_dict:
            self.default_filter[rating] = filter_dict[rating]
        for yesno in yesno_dict:
            self.default_filter[yesno] = yesno_dict[yesno]
        self.default_filter["topk"] = topk
        show_rects = self.rankings.updated_pairs(filter_dict, yesno_dict, topk)

        for box in self.prop_boxes:
            reviewer, prop = box.get_reviewer_prop()
            state = "hidden"
            for i in range(len(show_rects)):
                if show_rects[i][0] == reviewer and show_rects[i][1] == prop:
                    state = "normal"
                    break
            box.update_rect(state=state)
            box.update_text(state=state)

    def change_attribute(self):
        """
            Open a window for changing the attributes.
        """
        dic = {i:self.attr_to_rat[i] for i in self.attr_to_rat if i!="Bands"}
        self.window = legend_window(dic, self, self.rankings.get_all_sub_ratings())
        self.window.show()

    def filter_rect(self):
        """
            Show filter window.
        """
        self.filter = filter_window(self, self.filter_dict, self.yesno_list, self.rate_range, len(self.rankings.columns),self.default_filter)
        self.filter.show()

    def rating_detail(self, reviewer, prop):
        """
            Show rating details.
        """
        self.child_window_ratings("Rating Details", reviewer, prop)

    def proposal_detail(self, prop):
        """
            Show proposal details.
        """
        text = self.props.get_detail(prop)
        self.child_window_prop(f"Details of {prop}", text)

    def child_window_prop(self, title, text):
        """
            Pop-up window with proposal details.

            Parameters:
                title (str): Title of the window.
                text (str): Text to be displayed.
        """
        win3 = Toplevel(self.root)
        win3.title('Proposal Details')
        T = Text(win3, height=20, width=52)
        T.insert("1.0", text)
        # Create label
        l = Label(win3, text=title)
        l.pack()
        T.pack()
        l.config(font =("Times", "24", "bold"))
        T.config(font =("Times", "16"))

    def show_width(self, event):
        """
            Show distance of the mouse to an item.
        """
        self.canvas.itemconfigure("event", text="event.width: %s" % event.width)
        self.canvas.itemconfigure("cget", text="winfo_width: %s" % event.widget.winfo_width())



    def child_window_ratings(self, name, reviewer, proposal):
        """
            Display ratings window for proposal.

            Parameters:
                name (str): Title of the window.
                reviewer (str): Name of the reviewer.
                proposal (str): Name of the proposal.
        """
        win2 = Toplevel(self.root)
        win2.geometry('1000x300')
        win2.title('Ratings Details')
        Label(win2, text=name).pack()

        col_names = self.rankings.get_all_sub_ratings()
    
        s = ttk.Style()
        s.theme_use('clam')

        # Add the rowheight
        s.configure('Treeview', rowheight=100)
        tree = ttk.Treeview(win2, columns=col_names, selectmode="extended", show="headings")
        treeScroll = ttk.Scrollbar(win2, orient="horizontal", command=tree.xview)
        treeScroll.pack(side=BOTTOM, fill=X)
        tree.configure(xscrollcommand=treeScroll.set)
        rating = []
        reviews = self.reviews.get_reviews_in_order(reviewer, proposal, col_names)
        for rate_name in col_names:
            rating.append(self.rankings.get_sub_rating(rate_name, reviewer, proposal))
            tree.heading(rate_name, text=rate_name)
        tree.insert('', 'end', iid='line1', values=tuple(rating))
        if len(reviews) != 0:
            tree.insert('', 'end', iid='line2', values=tuple(reviews))
        tree.pack(side=LEFT, fill=BOTH)

    def review_text(self, reviewer, proposal_name):
        """
            Display window for reviews.
            Parameters:
                reviewer (str): name of the reviewer.
                proposal_name (str): name of the proposal.
        """
        list_reviews = self.reviews.get_all_review_sub(reviewer, proposal_name)
        self.child_window_review(f"The Review of {proposal_name} by {reviewer}", list_reviews, list_review_titles=self.reviews.review_titles)

    def child_window_review(self, title, list_reviews, list_review_titles):
        """
            Window for displaying the text reviews.

            Parameters:
                title (str): title of the window.
                list_reviews (list): list of reviews.
                list_review_titles (list): list of the names of the attributes for the text reviews.
        """
        win2 = Toplevel(self.root)
        win2.title('Review Details')

        canvas = Canvas(win2, width=500, height=300)
        container = ttk.Frame(canvas)
        scroll = ttk.Scrollbar(win2, orient="vertical", command=canvas.yview)
        
        l = Label(container, text=title)
        l.pack()
        l.config(font =("Times", "18", "bold"))
        for i in range(len(list_reviews)):
            T = Text(container, height=8, width=52, font =("Times", "12"))
            L = Label(container, text=list_review_titles[i], font=("Times", "16", "bold"))
            L.pack()
            T.pack()
            T.insert(END, list_reviews[i])

        canvas.create_window(0, 0, anchor=CENTER, window=container)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), 
                        yscrollcommand=scroll.set)
        canvas.pack(fill='both', expand=False, side='left')
        scroll.pack(side=RIGHT, fill=Y, expand=False)

    def set_up(self):
        """
            Set up the commands on main canvas.

            Right-click: open an option menu.
            Press and hold: select all item boxes for the same proposal and darken them.
            Left-click: shift the entire column to its left.
        """
        self.canvas.pack(fill="both", expand=False)
        self.canvas.bind("<Configure>", self.show_width)
        self.canvas.bind("<Button-2>", self.do_popup)
        self.canvas.bind("<ButtonRelease-1>",self.ret_colors)
        self.canvas.bind('<Double-1>', self.swap_left) 
        self.canvas.bind('<ButtonPress-1>', self.selectItem)

    def ret_colors(self, event):
        """
            Color the selected proposal boxes.
        """
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        item = self.canvas.find_closest(x, y, halo=2)

        _type = self.canvas.type(item)
        if _type != "rectangle":
            item = (item[0]-1, )
        tags = self.canvas.gettags(item)
        if len(tags) >= 2 and tags[1] != "current":
            prop = tags[1]
            all_items = self.canvas.find_withtag(prop)
            for item in all_items:
                reviewer = self.canvas.gettags(item)[0]
                self.canvas.itemconfig(item, fill=self.get_box_color(reviewer, prop))


    def show(self):
        """
            Run and show the GUI.
        """
        self.root.mainloop()

    def closeWindow(self):
        """
            Destroy the root upon closing the window.
        """
        self.root.destroy()
        sys.exit()
