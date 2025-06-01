import os
from tkinter import *
from tkinter import ttk
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import pyautogui
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Summary:
    """
        A class for summarizing the model results.

        Attributes:
        ------
            root: the root (to build toplevel window upon).
            window: the consensus window.

        Methods:
        ------
            show():
                display the window.
            loadmodel(model_attr, result, rankings_name, rankings):
                Update new results computed.
            choose_model():
                Buttons for choosing models and setting parameters.
            change_base_default():
                Changing the default of the base model.
            display_plots():
                Display the results for model comparison.
            update_cursor_position():
                Capture cursor position and display the labels on the plots.
            compute_Q_matrix(ranking, census_rank, isboot=False, isrank=True):
                Compute the Q matrix sorted by the census_rank.
            compute_Q_compare():
                Compute the matrix for comparing the consensus rankings.
    """
    def __init__(self, root, window) -> None:
        self.window=window
        self.rankings_names = self.window.rankings_names
        self.result = self.window.results

        self.root2 = Toplevel(root)
        self.root2.title('Compare Model Results')
        self.root2.geometry('1200x700+200+250')
        self.root2['bg'] = 'white'
        self.Scroll = ttk.Scrollbar(self.root2, orient='horizontal')
        self.Scroll.pack(side="bottom", fill="x", expand=False)
        self.Scroll2 = ttk.Scrollbar(self.root2, orient='vertical')
        self.Scroll2.pack(side="right", fill="y", expand=False)
        #rankings = np.loadtxt(path, delimiter=',')
        self.type = self.window.type
        if self.type == "Rank":
            self.rankings = self.window.rankings
            self.rankings = self.rankings.to_numpy()
        elif self.type == "Rate":
            self.ratings = self.window.ratings
            self.ratings = self.ratings.to_numpy()
        elif self.type == "Both":
            self.rankings = self.window.rankings
            self.ratings = self.window.ratings
            self.rankings = self.rankings.to_numpy()
            self.ratings = self.ratings.to_numpy()

        self.box_width = 120
        self.box_height = 25
        self.label_entry = [[] for _ in range(len(self.result)+1)]

        self.canvas2 = Canvas(self.root2, width=1200, height=700, xscrollcommand=self.Scroll.set,
                              scrollregion=(0, 0, 2500, 1500))
        self.Scroll.config(command=self.canvas2.xview)
        self.Scroll2.config(command=self.canvas2.yview)

        self.canvas2.pack(fill='both', side='left', expand=True)

        s = ttk.Style()
        s.theme_use('clam')


    def show(self):
        """
            Show the summary window.
        """
        self.choose_model()
        self.root2.mainloop()

    def loadmodel(self, result):
        """
            Load updated model results in the comparison table.
        """
        self.result = result
        for i in range(len(self.result)+1):
            for j in range(len(self.label_entry[i])):
                self.label_entry[i][j].destroy()
        self.display_plots()

    def choose_model(self):
        """
            Buttons for choosing models to compare (including base model).
        """
        label = Label(self.canvas2, text="Choose model(s) for comparison",font=('Comic Sans MS', 15),takefocus=0)
        self.canvas2.create_window(20, 30, window=label, anchor=W)
        self.canvas2.create_line(280, 0, 280, 1500, width=1.5, fill="gray85")

        options_list = list(self.result.keys())
        options_list.append("None")
        self.model_choice = []
        self.set_models = []
        self.base = StringVar(self.canvas2)
        self.base.set("None")
        label = Label(self.canvas2, text="Base model", font=('Comic Sans MS', 15), takefocus=0)
        self.canvas2.create_window(70, 340, window=label, anchor=W)
        self.base_menu = OptionMenu(self.canvas2, self.base, *list(self.result.keys()))
        self.canvas2.create_window(80, 370, window=self.base_menu, anchor=W)

        for i in range(len(options_list)-1):
            self.model_choice.append(StringVar(self.canvas2))
            self.model_choice[-1].set("None")
            model_menu = OptionMenu(self.canvas2, self.model_choice[-1], *options_list)
            self.model_choice[-1].trace("w", lambda *args: self.change_base_default)
            self.canvas2.create_window(80, i * 40 + 80, window=model_menu, anchor=W)

        # Button for reloading model results.
        button = Button(self.canvas2, text="Reload Model Results", command=self.display_plots)
        self.canvas2.create_window(50, 500, window=button, anchor=W)

        # Button for showing model comparison
        button = Button(self.canvas2, text="Show Model Comparison", command=self.display_plots)
        self.canvas2.create_window(40, 550, window=button, anchor=W)

        # Choosing the number of bootstrap samples.
        self.nBoot = IntVar(self.canvas2)
        self.nBoot.set(50)
        label = Label(self.canvas2, text="Number of Bootstrap Samples", font=('Comic Sans MS', 15), takefocus=0)
        self.canvas2.create_window(20, 400, window=label, anchor=W)
        nbootchoice = Entry(
                self.canvas2,
                textvariable=self.nBoot,
                font=('calibre', 10, 'normal'))
        self.canvas2.create_window(50, 430, window= nbootchoice, anchor=W)

        #font = ("Times New Roman bold", 12)
        #n = len(self.rankings_names['long'])
        #for i in range(n):
        #    pos = (420 - self.box_width // 2,
        #                             420 + self.box_width // 2,
        #                             100 + i * 30 - self.box_height // 2,
        #                             100 + i * 30 + self.box_height // 2)

        #    self.canvas2.create_rectangle(pos[0], pos[2], pos[1], pos[3], fill="gray90", outline="gray90", width=3)
        #    self.canvas2.create_text( pos[0] - 30, (pos[2] + pos[3]) // 2,
        #                             font=('Comic Sans MS', 13), text=f'{i+1}',
        #                             fill="black")
        #    self.canvas2.create_text((pos[0] + pos[1]) // 2, (pos[2] + pos[3]) // 2,
        #                                             font=font,text= self.rankings_names["long"][i],
        #                                             fill="black")

    def change_base_default(self):
        """
            Change the default option for the base model.
        """
        options_list = list(self.result.keys())
        for i in range(len(options_list) - 1):
            if self.model_choice[i].get() != None:
                self.base.set(self.model_choice[i].get())

        self.base_menu['menu'].delete(0, 'end')
        new_choices = list(self.result.keys())

        for choice in new_choices:
            # Add menu items.
            self.base_menu['menu'].add_command(label=choice, command=lambda choice1=choice: self.base.set(choice1))


    def display_plots(self):
        """
            Display the plots for comparison:
                - Plots of Q matrices sorted by the consensus rankings from each model.
                - Plots of Q matrices from the consensus rankings from the bootstrap samples.
                - Plots of Q matrices for comparisons across consensus rankings.
        """
        options_list = list(self.result.keys())

        for i in range(len(options_list)):
            if self.model_choice[i].get() not in self.set_models:
                self.set_models.append(self.model_choice[i].get())

        if 'None' in self.set_models: self.set_models.remove('None')

        self.axis_label = []
        self.Q_sorted = []
        self.Q_boot = []
        self.Qcompare = None
        self.ItemLabel = [[],[],[]]
        self.plot = [[],[],[]]
        self.xpix = []
        self.ypix = []

        if len(self.set_models) >= 1:
            self.canvas2.create_text(400, 30, text="Q matrix:", font=('Comic Sans MS', 15))
            for imod in range(len(self.set_models)):
                mod = self.set_models[imod]
                self.imod = imod
                self.axis_label.append([])

                for i in range(len(self.result[mod]['ranking'])):
                    irk = self.result[mod]['ranking'][i]
                    item = self.rankings_names["short"][irk]
                    self.axis_label[imod].append(str(item))

                if self.type != "Rate":
                    self.Q_sorted.append(self.compute_Q_matrix(self.rankings, self.result[mod]['ranking']))
                elif self.type == "Rate":
                    self.Q_sorted.append(self.compute_Q_matrix(self.ratings, self.result[mod]['ranking'], isrank=False))

                fig, ax = plt.subplots(figsize=(3,3))
                fig.subplots_adjust(left=0.2, bottom=0.2)
                x = np.arange(1, len(self.result[mod]['ranking'])+1)
                cmap = plt.get_cmap("Oranges")
                cmap.set_under(color='white')
                colormesh = ax.pcolormesh(x, x, self.Q_sorted[imod],
                                        vmin=0.0001, vmax=0.5, cmap=cmap)

                cmap.set_under('white')
                ax.set_yticks(ticks = x)
                ax.set_xticklabels(self.axis_label[imod])
                ax.set_xticks(ticks = x)
                ax.set_yticklabels(self.axis_label[imod])
                ax.tick_params(axis='x', labelrotation=90)
                ax.invert_yaxis()
                ax.set_xlabel(mod)
                ax.xaxis.set_label_position('top')
                y = np.arange(0, len(self.result[mod]['ranking']) + 1)
                if imod==0:
                    xy_pixels = ax.transData.transform(np.vstack([y,y]).T)
                    xpix, ypix = xy_pixels.T
                    self.width, self.height = fig.canvas.get_width_height()
                    ypix = self.height - ypix
                    self.xpix.extend(xpix)
                    self.ypix.extend(ypix)

                figure = FigureCanvasTkAgg(fig, self.canvas2)
                window = self.canvas2.create_window(imod * 400 + 330, 50, window=figure.get_tk_widget(), anchor=NW)
                self.plot[0].append(figure)
                self.label_entry[imod].append([window])

                self.ItemLabel[0].append(Label(self.canvas2, text=" "))
                self.ItemLabel[0][imod].lift()
                window = self.canvas2.create_window(imod * 400 + 530, 130, window=self.ItemLabel[0][imod], anchor=NW)
                self.label_entry[imod].append([window])

                # Bootstrap Q matrix
                self.canvas2.create_text(400, 380, text="Bootstrap Q:", font=('Comic Sans MS', 15))

                if mod != "Borda (Rankings)" and mod != 'Borda (Ratings)':
                    bspath = self.window.generate_bootstrap(self.nBoot.get(),mod) + "/bootstrap/" + str(mod) + "/bootcentral.txt"
                elif mod == "Borda (Rankings)":
                    bspath = self.window.generate_bootstrap(self.nBoot.get(),"Borda (Rankings)") + "/bootstrap/Borda/Rank_bootcentral.txt"
                elif mod == "Borda (Ratings)":
                    bspath = self.window.generate_bootstrap(self.nBoot.get(),"Borda (Ratings)") + "/bootstrap/Borda/Rate_bootcentral.txt"

                bootmat = np.loadtxt(bspath, delimiter=',')
                self.Q_boot.append(self.compute_Q_matrix(bootmat, self.result[mod]['ranking'],isboot=True))
                fig2, ax2 = plt.subplots(figsize=(3,3))
                fig2.subplots_adjust(left=0.2, bottom=0.2)
                cmap = plt.get_cmap("Greens")
                cmap.set_under(color='white')
                colormesh = ax2.pcolormesh(x, x, self.Q_boot[imod],
                                          vmin=0.0001, vmax=1, cmap=cmap)

                cmap.set_under('white')
                ax2.set_yticks(ticks=x)
                ax2.set_yticklabels(self.axis_label[imod])
                ax2.set_xticks(ticks=x)
                ax2.set_xticklabels(self.axis_label[imod])
                ax2.tick_params(axis='x', labelrotation=90)
                ax2.invert_yaxis()
                ax2.set_xlabel(mod)
                ax2.xaxis.set_label_position('top')

                figure = FigureCanvasTkAgg(fig2, self.canvas2)
                window = self.canvas2.create_window(imod * 400 + 330, 400, window=figure.get_tk_widget(),
                                                    anchor=NW)
                self.plot[1].append(figure)
                self.label_entry[imod].append([window])

                self.ItemLabel[1].append(Label(self.canvas2, text=" "))
                self.ItemLabel[1][imod].lift()
                window = self.canvas2.create_window(imod * 400 + 530, 480, window=self.ItemLabel[1][imod], anchor=NW)
                self.label_entry[imod].append([window])

            self.xpix = np.asarray(self.xpix, dtype=np.float32)
            self.ypix = np.asarray(self.ypix, dtype=np.float32)

        if len(self.set_models) >= 2:
            self.axis_label2 = []
            self.canvas2.create_text(420, 730, text="Model Comparison:", font=('Comic Sans MS', 15))
            for i in range(len(self.rankings_names["short"])):
                irk = self.result[self.base.get()]['ranking'][i]
                item = self.rankings_names["short"][irk]
                self.axis_label2.append(str(item))
            self.Qcompare = self.compute_Q_compare()
            fig, ax = plt.subplots(figsize=(3,3))
            fig.subplots_adjust(left=0.2, bottom=0.2)
            x = np.arange(1, len(self.rankings_names["short"])+1)
            cmap = plt.get_cmap("Blues")
            cmap.set_under(color='white')
            colormesh = ax.pcolormesh(x, x, self.Qcompare,
                                    vmin=0.001, vmax=len(self.set_models), cmap=cmap)

            cmap.set_under('white')
            ax.set_yticks(ticks = x)
            ax.set_yticklabels(labels = self.axis_label2)
            ax.set_xticks(ticks = x)
            ax.set_xticklabels(self.axis_label2)
            ax.tick_params(axis='x', labelrotation=90)
            ax.invert_yaxis()
            ax.set_xlabel("Base="+self.base.get())
            ax.xaxis.set_label_position('top')

            figure = FigureCanvasTkAgg(fig, self.canvas2)
            window = self.canvas2.create_window(330, 750, window=figure.get_tk_widget(), anchor=NW)
            self.label_entry[len(self.set_models)].append([window])
            self.plot[2].append(figure)

            self.ItemLabel[2].append(Label(self.canvas2, text=" "))
            self.ItemLabel[2][0].lift()
            window = self.canvas2.create_window(530, 830, window=self.ItemLabel[2][0], anchor=NW)
            self.label_entry[len(self.set_models)].append([window])


        self.update_cursor_position()

    def update_cursor_position(self):
        """
            Capture the current cursor position and display the labels on the plots
        """
        x, y = pyautogui.position()
        winx, winy = self.canvas2.winfo_x(), self.canvas2.winfo_y()
        x = x - winx
        y = y - winy
        self.xgrid = []
        self.ygrid = []


        ## Region for each plot
        for imod in range(len(self.set_models)):
            figx = self.plot[0][imod].get_tk_widget().winfo_rootx()
            self.xgrid.append([figx, self.width + figx])

        for iy in range(len(self.plot)):
            figy = self.plot[iy][0].get_tk_widget().winfo_rooty()
            self.ygrid.append([figy, self.height + figy])

        xpos = 0
        fallsx = False
        fallsy = False

        ## Find out which plot the cursor is in
        for interval in self.xgrid:
            xpos += 1
            if interval[0] <= x <= interval[1]:
                x -= interval[0]
                fallsx = True
                break

        ypos = 0

        for interval in self.ygrid:
            ypos += 1
            if interval[0] <= y <= interval[1]:
                y -= interval[0]
                fallsy = True
                break

        try:
            ## Find out the exact position of the cursor on the plot and print out the labels.
            if fallsx and fallsy and min(self.xpix) < x < max(self.xpix) and min(self.ypix) < y < max(self.ypix):
                if ypos == 3 and self.Qcompare is None:
                    pass
                if ypos == 3 and xpos > 1:
                    pass
                whichx = sum(self.xpix <= x) - 1
                whichy = sum(self.ypix < y) - 1

                if ypos == 1:
                    Qdisplay = self.Q_sorted
                elif ypos == 2:
                    Qdisplay = self.Q_boot
                elif ypos == 3:
                    Qdisplay = []
                    Qdisplay.append(self.Qcompare)

                if whichy >= whichx:
                    self.ItemLabel[ypos-1][xpos-1].config(text="X=" + self.axis_label[xpos-1][whichx] + "\n" +
                                                    "Y=" + self.axis_label[xpos-1][whichy] + "\n" +
                                                    f"Q={round(Qdisplay[xpos-1][whichy][whichx], 2)}")


        except:
            pass

        self.ItemLabel[0][0].after(100, self.update_cursor_position)

    def compute_Q_matrix(self, ranking, census_rank, isboot=False, isrank=True):
        """
            Compute the Q matrices sorted by the consensus rankings.

            Parameters:
                ranking (df): DataFrame for the rankings (columns represent proposals).
                census_rank (list): List of the census rankings.
                isboot (bool): the sample is from bootstrap or not.
                isrank (bool): the dataset contains rankings or ratings.

            Returns:
                Qmatrix (np.array): a lower triangular Q matrix.
        """
        n = len(self.rankings_names['long'])
        Q = np.zeros((n,n))
        for irow in range(ranking.shape[0]):
            for i in range(n):
                for j in range(i+1,n):
                    if isboot:
                        if isrank:
                            Q[int(ranking[irow, i])][int(ranking[irow, j])] += 1.0 / ranking.shape[0]
                        else:
                            if ranking[irow, i] > ranking[irow, j]:
                                Q[i][j] += 1.0 / ranking.shape[0]
                    else:
                        if isrank:
                            Q[int(ranking[irow, i])-1][int(ranking[irow, j])-1] += 1.0 / ranking.shape[0]
                        else:
                            if ranking[irow, i] > ranking[irow, j]:
                                Q[i][j] += 1.0 / ranking.shape[0]

        Q = Q[:, census_rank]
        Q = Q[census_rank, :]

        np.fill_diagonal(Q, 0.0001)

        return np.tril(Q)


    def compute_Q_compare(self):
        """
            Compute the Q matrices for comparison.

            Returns:
                Q matrix (np.array)
        """
        base = self.base.get()
        modconsider = [x for x in self.set_models if x != base]
        n = len(self.rankings_names['long'])
        Q = np.zeros((n,n))
        baserank = self.result[base]['ranking']
        for imod in range(len(modconsider)):
            mod = modconsider[imod]
            cur = self.result[mod]['ranking']
            for i in range(n):
                for j in range(i+1,n):
                    Q[int(cur[i])][int(baserank[j])] += 1.0

        Q = Q[:, baserank]
        Q = Q[baserank, :]

        return Q






