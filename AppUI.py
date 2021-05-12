#! /usr/local/bin/python3
# Author : Sunil Akella

# Healthify Updates
"""
    Upcoming Features:
      1 - 
      2 - 
     
    Revision History Updates:
      1.0 :  Healthify Tool - Initial Draft
    
"""



# Python Built-in Imports
import os
import subprocess
import platform
import sys
import json
import tkinter as tk
from time import ctime

# Python 3rd-party imports ( from pip3 )
from PIL import ImageTk, Image


# Global Variable
__HEALTHIFY_UI_VERSION__ = "1.0"

# -----------------------------------------------------------------
# Healthify - App UI Code 
# -----------------------------------------------------------------

def donothing():
    pass

def AppClose(mw):
    mw.destroy()

def CountdownTimer(mw, i, label):
    if i > 0:
        i -= 1
        label.set(i)
        mw.after(1000, lambda: CountdownTimer(mw, i, label))
    else:
        AppClose(mw)

def AddImageAndTextToUI(mw, img, txt, sx, sy, cmd=None, img_type='Button', img_dir='left'):
    '''
        Args Description:
            mw       = BMAN's MainWindow (or) Window of current context
            img      = Image that needs to be displayed
            sx       = Image Size x-axis
            sy       = Image Size y-axis
            img_type = Button / Label 
            cmd      = if img_type = Label, cmd will be None
                       if img_type = Button, cmd will be the function call
            img_dir  = Position / Direction of the Image : left, right, center 
    '''
    # Adding images
    tool_path = os.getcwd()
    image_path = os.path.join(tool_path, 'images')
    AddImage = Image.open(os.path.join(image_path, img))
    AddResized = AddImage.resize((sx, sy), Image.ANTIALIAS)
    AddPhoto = ImageTk.PhotoImage(AddResized)
    if img_type == 'Button':
        AddButton = tk.Button(mw, image=AddPhoto, command=cmd, bg='white')
        if img_dir == 'left':
            AddButton.pack(side=tk.LEFT, padx=10, pady=10)
        elif img_dir == 'center':
            AddButton.pack(anchor=tk.CENTER)
        AddButton.image = AddPhoto
    elif img_type == 'Label':
        label = tk.Label(mw, image=AddPhoto, bg='white')
        label.image = AddPhoto # keep a reference!
        label.pack(side=tk.LEFT)
        tk.Label(mw, justify='left', padx=70, text=txt, font="Helvetica 18 bold", fg='black', bg='white').pack()


def clear(mw):
    # Fetching Month and Year ( This output is parsed based on Platform : MacOS / Darwin / Windows)
    day, month, date, time, year = ctime().split()
    tool_path = os.getcwd()
    items = mw.pack_slaves()
    for i in items:
        i.destroy()
    title = "Healthify - Your Health First App"
    header_label = tk.Label(mw, justify='left', padx=70, text=title, font="Helvetica 18 bold", fg='blue', bg='white').pack()
    header_label = tk.Label(mw, justify='left', padx=70, text='%s %s %s     (Version - %s)' % (date, month, year, __HEALTHIFY_UI_VERSION__), font="Helvetica 12 bold", bg='white').pack()


def HealthifyUI(tc_dict, img_name, img_msg):
    mw = tc_dict['mainWindow']
    counter = tc_dict['auto_close_counter']
    # Deleting Existing Object
    clear(mw)
    # Adding Image
    AddImageAndTextToUI(mw, img_name, img_msg, 230, 200, cmd=None, img_type='Label')
    tk.Label(mw, text="\n\nThis application will auto-close in another %s seconds" % counter, justify='center', padx=20, bg='white', fg='red').pack()
    auto_close_counter = int(counter)
    button_label = tk.StringVar()
    button_label.set(auto_close_counter)
    tk.Button(mw, textvariable=button_label, command=donothing).pack()
    CountdownTimer(mw, auto_close_counter, button_label)




def run_app(img_name, img_msg):
    # Adding images
    tool_path = os.getcwd()
    tool_data_path = os.path.join(tool_path, 'data')
    tc_dict = json.loads(open(os.path.join(tool_data_path, 'app_controls.JSON')).read())
    # Creating the Main Window
    mainWindow = tk.Tk()
    tc_dict['mainWindow'] = mainWindow
    mainWindow.title(tc_dict['title'])
    mainWindow.geometry(tc_dict['geometry'])
    mainWindow.resizable(0, 0)
    mainWindow.configure(background=tc_dict['bg'])
    mainWindow.attributes('-topmost', True)
    mainWindow.lift()

    # App UI Invoke
    HealthifyUI(tc_dict, img_name, img_msg)

    # Wish Console Mainloop
    mainWindow.mainloop()

