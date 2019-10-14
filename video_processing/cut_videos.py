'''
the following code is used to cut videos
input: name of the video to cut
'''
import tkinter
from tkinter import filedialog
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

currdir = os.getcwd()
file_name = filedialog.askopenfilename(initialdir = "/",title = "Select MOV file to cut",filetypes = (("MOV files","*.MOV"),("all files","*.*")))
directory, file_name = os.path.split(file_name)
os.chdir(directory)
ffmpeg_extract_subclip(file_name, 0, 5, targetname="delete1.MOV") # file name to cut, t1(s), t2(s), target name
ffmpeg_extract_subclip(file_name, 426, 791, targetname="delete2.MOV")