import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import srcs.global_var as g
from srcs.gui.utility import Point
from srcs.generate_puzzle import spiral
import os
from platform import system as platform

class npuzzleGui:
    """
    start the gui wich allow the user to see the puzle solving in a graphical windows
    """
    boxes_img = []

    def __init__(self, win, win_title, img_path, puzzle):
        self.win = win
        self.win.title(win_title)
        self.win.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.puzzle = puzzle

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

        # get image dimension and create canvas accordingly
        self.img_w, self.img_h, self.img_no_channels = self.cv_img.shape
        self.canvas = tkinter.Canvas(win, width = self.img_w, height = self.img_h)
        self.canvas.pack()
        self.canvas.configure(background='black')

        # calculate the box width
        self.box_w = int(self.img_w / self.puzzle.size)
        self.boxes = [None]*self.puzzle.size*self.puzzle.size
        self.set_boxes_img()

        self.printPuzzle()

        # key binding
        self.win.bind('<Key>', self.keyPress)

        self.centerWindows()
        if platform() == 'Darwin':  # How Mac OS X is identified by Python
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        self.win.mainloop()

    def centerWindows(self):
        """
        "center" the windows in the middle of the screen
        """
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.win.winfo_screenwidth()/2 - self.img_w/2)
        positionDown = int(self.win.winfo_screenheight()/2 - self.img_h/2)

        # Positions the window in the center of the page.
        self.win.geometry("+{}+{}".format(positionRight, positionDown))

    def printPuzzle(self):
        for i in range(1, self.puzzle.size * self.puzzle.size):
            pos = self.get_pos(i)
            img = self.boxes_img[ list(g.resolved_puzzle).index(self.puzzle[i]) ]
            self.boxes[self.puzzle[i]] = self.canvas.create_image(pos.X, pos.Y, image=img, anchor=tkinter.NW)

    def get_pos(self, i):
        x = int(i % self.puzzle.size)
        y = int(i / self.puzzle.size)
        return Point(x * self.box_w, y * self.box_w)

    def set_boxes_img(self):
        """
        crop image part coresponding to the puzzle boxes_img
        """
        for y in range(self.puzzle.size):
            for x in range(self.puzzle.size):
                # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
                box_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(
                    self.cv_img[y * self.box_w : (y + 1) * self.box_w, \
                                x * self.box_w : (x + 1) * self.box_w]
                ))
                self.boxes_img.append(box_img)

    def keyPress(self, e):
        mooved = False
        if e.keysym == "Up" or e.keysym == "w" and self.puzzle.pos0xy[0] > 0:
            self.puzzle.move('T')
            mooved = True
        elif e.keysym == "Right" or e.keysym == "d" and self.puzzle.pos0xy[1] < self.puzzle.size - 1:
            self.puzzle.move('R')
            mooved = True
        elif e.keysym == "Down" or e.keysym == "s" and self.puzzle.pos0xy[0] < self.puzzle.size - 1:
            self.puzzle.move('B')
            mooved = True
        elif e.keysym == "Left" or e.keysym == "a" and self.puzzle.pos0xy[1] > 0:
            self.puzzle.move('L')
            mooved = True

        if mooved:
            print('mooved !')


def start_gui(img_path, puzzle):
    npuzzleGui(tkinter.Tk(), "N-Puzzle", img_path, puzzle)