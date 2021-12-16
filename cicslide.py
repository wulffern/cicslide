######################################################################
##        Copyright (c) 2021 Carsten Wulff Software, Norway
## ###################################################################
## Created       : wulff at 2021-3-22
## ###################################################################
##  The MIT License (MIT)
##
##  Permission is hereby granted, free of charge, to any person obtaining a copy
##  of this software and associated documentation files (the "Software"), to deal
##  in the Software without restriction, including without limitation the rights
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##  copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included in all
##  copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##  SOFTWARE.
##
######################################################################
#####################################################################

import tkinter as tk
import requests
from tkinter import *
from PIL import Image, ImageTk
import click



class cSlide(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x1000")
        self.configure(bg="black")
        self.delay = 500
        self.pausedelay = 100
        self.urlMode = False
        self.images = list()
        self.index = 0
        self.pause = False
        self.bind("<Escape>",lambda e: self.destroy())
        self.bind("p",lambda e: self.pauseToggle())
        self.bind("w",lambda e: self.incrementIndex())
        self.bind("d",lambda e: self.incrementIndex10())
        self.bind("a",lambda e: self.decrementIndex10())
        self.bind("s",lambda e: self.decrementIndex())
        self.bind("+",lambda e: self.speedUp())
        self.bind("-",lambda e: self.slowDown())

        self.persistent_image = None
        self.label = Label(self,image=self.persistent_image,bg="black")
        self.label.pack(side="top",fill = "both", expand=True)

    def pauseToggle(self):
        self.pause = not self.pause

    def incrementIndex(self):
        self.index += 1
        self.wrapIndex()

    def decrementIndex(self):
        self.index -= 1
        self.wrapIndex()

    def incrementIndex10(self):
        self.index += 10
        self.wrapIndex()

    def decrementIndex10(self):
        self.index -= 10
        self.wrapIndex()

    def wrapIndex(self):
        if(self.index > len(self.images)):
            self.index = 0

    def slowDown(self):
        self.delay += 100

    def speedUp(self):
        self.delay -= 100

    def startSlideShow(self):

        if(self.index >= len(self.images)):
            self.index = 0

            myimage = self.images[self.index]
        l_delay = self.delay
        try:
            self.nextImage(myimage)

        except Exception as e:
            print(e)
            l_delay = 10
            pass


        if(not self.pause):
            self.incrementIndex()
        else:
            l_delay = self.pausedelay


        self.after(l_delay, self.startSlideShow)


    def nextImage(self,url):

        if(self.urlMode):
            image = Image.open(requests.get(url,stream=True).raw)
        else:
            image = Image.open(url)

        img_w, img_h = image.size
        scr_w, scr_h = self.winfo_width(), self.winfo_height()

        sz = img_w/img_h

        if(img_w > img_h):
            width = scr_w
            height = img_h *scr_w/img_w
        else:
            width = img_w * scr_h/img_h
            height = scr_h


        resized = image.resize((int(width), int(height)), Image.ANTIALIAS)

        self.persistent_image = ImageTk.PhotoImage(resized)
        self.label.configure(image=self.persistent_image)



@click.group()
def cli():
    pass

@cli.command()
@click.argument("url")
@click.argument("start")
@click.argument("stop")
@click.argument("postfix")
def series(url,start,stop,postfix):
    c = cSlide()
    c.urlMode = True
    for i in range(int(start),int(stop)):
        c.images.append(url + str(i) + postfix)

    c.startSlideShow()
    c.mainloop()



@cli.command()
@click.argument("filename")
def url(filename):

    c = cSlide()
    c.urlMode = True
    with open(filename,"r") as fi:
        for line in fi:
            c.images.append(line.strip())
    c.startSlideShow()
    c.mainloop()



if __name__ == "__main__":
    cli()
