import os
import cv2
import tkinter
import numpy as np
import srcs.global_var as g
from time import time, sleep
import PIL.Image, PIL.ImageTk
from srcs.gui.utility import Point
from srcs.generate_puzzle import spiral
from platform import system as platform
from srcs.solving_out import solving_out

ANIM_STEP_TIME = 25
ANIM_STEP = 5
MAX_RESOLVE_STEP_TIME = 1000
SIZE = 600

class npuzzleGui:
    """
    start the gui wich allow the user to see the puzle solving in a graphical windows
    """
    boxes_img = []

    def __init__(self, win, win_title, img_path, puzzle):
        self.win = win
        self.win.title(win_title)
        self.win.geometry(str(SIZE) + 'x' + str(SIZE))
        self.win.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.puzzle = puzzle

        # load image and scale it if necessary
        self.load_img(img_path)

        # get image dimension and create canvas accordingly
        self.img_w, self.img_h, self.img_no_channels = self.cv_img.shape
        self.canvas = tkinter.Canvas(win, width = self.img_w, height = self.img_h, bd=0, highlightthickness=0)

        self.canvas.pack()
        self.canvas.configure(background='black')

        # calculate the box width
        self.box_w = int(self.img_w / g.param['size'])
        self.boxes = [None]*g.param['size']*g.param['size']
        self.set_boxes_img()

        self.printPuzzle()

        # key binding
        self.win.bind('<Key>', self.keyPress)

        self.resolve_step_time = int(MAX_RESOLVE_STEP_TIME / 2)
        self.is_solving = False

        self.centerWindows()
        if platform() == 'Darwin':  # How Mac OS X is identified by Python
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        self.win.mainloop()

    def load_img(self, img_path):
        # load the image using OpenCV
        self.cv_img = cv2.imread(img_path)
        old_size = self.cv_img.shape[:2]

        # scale image to match SIZE
        ratio = SIZE / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        self.cv_img = cv2.resize(self.cv_img, (new_size[1], new_size[0]))

        # calculate the offset
        left = (SIZE - new_size[1]) // 2
        top = (SIZE - new_size[0]) // 2

        # create background image (used only if image is not a square)
        img = np.full((SIZE, SIZE, 3), 255, np.uint8)

        # paste the image to the background
        img[top:top + self.cv_img.shape[0], left:left + self.cv_img.shape[1]] = self.cv_img
        self.cv_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
        start0 = list(self.puzzle).index(0)
        for i in range(0, g.param['size'] * g.param['size']):
            if i != start0:
                pos = self.get_pos(i)
                img = self.boxes_img[ list(g.param['resolved_puzzle']).index(self.puzzle[i]) ]
                self.boxes[self.puzzle[i]] = self.canvas.create_image(pos.X, pos.Y, image=img, anchor=tkinter.NW)

    def get_pos(self, i):
        x = int(i % g.param['size'])
        y = int(i / g.param['size'])
        return Point(x * self.box_w, y * self.box_w)

    def set_boxes_img(self):
        """
        crop image part coresponding to the puzzle boxes_img
        """
        for y in range(g.param['size']):
            for x in range(g.param['size']):
                # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
                box_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(
                    self.cv_img[y * self.box_w : (y + 1) * self.box_w, \
                                x * self.box_w : (x + 1) * self.box_w]
                ))
                self.boxes_img.append(box_img)

    def keyPress(self, e):
        if not self.is_solving:
            # start solving key
            if (e.keysym == "Return" or e.keysym == "space"):
                self.is_solving = True
                result = solving_out(self.puzzle)
                moves = result['puzzle'].get_path()
                self.resolveAnim(list(moves))

            # move keys
            if (e.keysym == "Up" or e.keysym == "w") and self.puzzle.pos0xy[0] < g.param['size'] - 1:
                self.move('B')
            elif (e.keysym == "Right" or e.keysym == "d") and self.puzzle.pos0xy[1] > 0:
                self.move('L')
            elif (e.keysym == "Down" or e.keysym == "s") and self.puzzle.pos0xy[0] > 0:
                self.move('T')
            elif (e.keysym == "Left" or e.keysym == "a") and self.puzzle.pos0xy[1] < g.param['size'] - 1:
                self.move('R')

        # changing speed key
        if (e.keysym == "minus"):
            self.resolve_step_time = self.resolve_step_time + 10 if self.resolve_step_time + 10 <= MAX_RESOLVE_STEP_TIME else MAX_RESOLVE_STEP_TIME
        if (e.keysym == "plus"):
            self.resolve_step_time = self.resolve_step_time - 10 if self.resolve_step_time - 10 >= 0 else 0

    def resolveAnim(self, moves):
        if (len(moves) > 0):
            self.move(moves.pop(0))
            self.canvas.after(ANIM_STEP_TIME*ANIM_STEP + self.resolve_step_time, self.resolveAnim, moves)
        else:
            self.is_solving = False

    def move(self, direction):
        save = list(self.puzzle)
        self.puzzle.move(direction)

        # calculate shift length
        startI = list(self.puzzle).index(0)
        destI = save.index(0)
        shift = self.get_pos(destI) - self.get_pos(startI)

        # animate movement
        shift.Y /= ANIM_STEP
        shift.X /= ANIM_STEP
        self.moveShape(self.boxes[self.puzzle[destI]], shift, ANIM_STEP, 0)

    def moveShape(self, shape, shift, maxStep, step):
        if (step < maxStep):
            self.canvas.move(shape, shift.X, shift.Y)
            self.canvas.after(ANIM_STEP_TIME, self.moveShape, shape, shift, maxStep, step+1)

def start_gui(img_path, puzzle):
    npuzzleGui(tkinter.Tk(), "N-Puzzle", img_path, puzzle)