import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import srcs.global_var as g
from srcs.gui.utility import Point
from srcs.generate_puzzle import spiral

class npuzzleGui:
    """
    start the gui wich allow the user to see the puzle solving in a graphical windows
    """
    boxes = []

    def __init__(self, win, win_title, img_path, puzzle):
        self.win = win
        self.puzzle = puzzle
        self.win.title(win_title)

        # Load an image using OpenCV
        self.cv_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

        # get image dimension and create canvas accordingly
        self.img_w, self.img_h, self.img_no_channels = self.cv_img.shape
        self.canvas = tkinter.Canvas(win, width = self.img_w, height = self.img_h)
        self.canvas.pack()

        # calculate the box width
        self.box_w = int(self.img_w / self.puzzle.size)

        self.get_boxes_img()

        i = 0
        for y in range(self.puzzle.size):
            for x in range(self.puzzle.size):
                self.show_image(Point(x * self.box_w, y * self.box_w), list(g.resolved_puzzle).index(self.puzzle[i]))
                i += 1

        self.win.mainloop()

    def get_boxes_img(self):
        """
        crop image part coresponding to the puzzle boxes
        """
        for y in range(self.puzzle.size):
            for x in range(self.puzzle.size):
                # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
                box_img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(
                    self.cv_img[y * self.box_w : (y + 1) * self.box_w, \
                                x * self.box_w : (x + 1) * self.box_w]
                ))
                self.boxes.append(box_img)

    def show_image(self, pos, index):
        self.canvas.create_image(pos.X, pos.Y, image=self.boxes[index], anchor=tkinter.NW)



def start_gui(img_path, puzzle):
    npuzzleGui(tkinter.Tk(), "N-Puzzle", img_path, puzzle)