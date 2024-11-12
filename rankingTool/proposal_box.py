from tkinter import *

class Proposal_Box:
    """
        This class controls the item boxes of the proposals.

        Attributes:
        -----
            canvas (tkinter.Canvas): The canvas to draw the item boxes.
            reviewer (str): The name of the reviewer of the proposal.
            pos (tuple): The position of the item boxes.
            prop (str, optional): The name of the proposal.
            color (str, optional): The background color of the item box.
            dash (tuple, optional): The dash style of outline of the item box.
            outl (str, optional): The outline color of the item box.
            width (int, optional): The width of the outline of the item box.
            type (str, optional): type = "Main" suggests that the item boxes are for the main canvas.
                        Otherwise it is for the consensus ranking area.

        Methods:
        -----
            get_reviewer_prop():
                Returns the name of the reviewer and the proposal as a list.
            get_pos():
                Returns the coordinates of the item boxes.
            update_rect(color=None, dash=None, outl=None, width=None, state=None)
                Update the item boxes with the graphical attributes.
            update_text(state=None):
                Update the text on the item boxes.

    """
    def __init__(self, canvas, reviewer, pos, prop=None, color="gray90", dash=(), outl="gray90", width=3, type="main") -> None:
        self.reviewer = reviewer
        self.prop = prop
        self.pos = pos
        self.canvas = canvas
        if type == "main":
            if prop == None:
                text = reviewer
                self.rectag = (f"{reviewer}", )
                self.textag = (f"{reviewer}text", )
                font = ("Comic Sans MS", 15)
            else:
                self.rectag = (f"{reviewer}", f"{prop}")
                self.textag = (f"{reviewer}text", f"{prop}text")
                text = prop
                font = ("Times New Roman", 12)
                self.rect = self.canvas.create_rectangle(
                    pos[0], pos[2], pos[1], pos[3],
                    fill=color,
                    dash=dash,
                    #dashoff = 3,
                    #stipple='gray25',
                    outline=outl,
                    width=width,
                    tag=self.rectag
                )
            self.text = self.canvas.create_text((pos[0] + pos[1]) // 2, (pos[2] + pos[3]) // 2, font=font, text=text,tag=self.textag, fill="black")
        else:
            text = prop
            font = ("Times New Roman", 12)
            self.rect = self.canvas.create_rectangle(
                pos[0], pos[2], pos[1], pos[3],
                fill=color,
                dash=dash,
                outline=outl,
                width=width
            )
            self.text = self.canvas.create_text((pos[0] + pos[1]) // 2, (pos[2] + pos[3]) // 2, font=font, text=text, fill="black")

    def get_reviewer_prop(self):
        """
            Returns the name of the reviewer and the proposal as a list.
        """
        return (self.reviewer, self.prop)

    def get_pos(self):
        """
            Returns the coordinates of the item boxes.
        """
        return self.pos[0], self.pos[2], self.pos[1], self.pos[3],

    def update_rect(self, color=None, dash=None, outl=None, width=None, state=None):
        """
            Update the item boxes with the graphical attributes.

            Parameters:
                color (str, optional): The background color of the item box.
                dash (tuple, optional): The dash style of outline of the item box.
                outl (str, optional): The outline color of the item box.
                width (int, optional): The width of the outline of the item box.
                state (str, optional): Whether or not the box is shown.

        """
        self.canvas.itemconfig(self.rect, fill=color, dash=dash, outline=outl, width=width, state=state)
        self.canvas.update()
    
    def update_text(self,  state=None):
        """
            Update the text on the item boxes.
        """
        self.canvas.itemconfig(self.text, state=state)
        self.canvas.update()