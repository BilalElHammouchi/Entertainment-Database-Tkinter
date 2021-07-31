from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import re
from PIL import ImageTk,Image
from Movies_Functions import *
import os.path
import configparser

# Configuration Settings

config = configparser.ConfigParser()
config.read('configuration.ini')
if os.path.isfile("configuration.ini"):
    if config['DEFAULT']['Darkmode'] == 'True':
        dark_modeMenu = False
    else:
        dark_modeMenu = True
else:
    config['DEFAULT'] = {'Darkmode': 'True' ,  'Viewmode': 'List'   }
    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)

# Frames
def Frame_MainMenu(root, Images_List, mycursor, mydb):
    global Frame_Entertainment,MyLabel_Movie2,Frame_Movies,Frame_Tv,Frame_Games,Frame_Books,MyLabel_Tv2,MyLabel_Book2,MyLabel_Game2
    Frame_Entertainment = Frame(root)
    Frame_Entertainment.pack()
    Frame_Movies = Frame(Frame_Entertainment)
    Frame_Movies.grid( row = 0 , column = 0 , padx = 2 , pady = 2 )
    Frame_Tv = Frame(Frame_Entertainment)
    Frame_Tv.grid( row = 0 , column = 1 , padx = 2 , pady = 2 )
    Frame_Games = Frame(Frame_Entertainment)
    Frame_Games.grid( row = 1 , column = 0 , padx = 2 , pady = 2 )
    Frame_Books = Frame(Frame_Entertainment)
    Frame_Books.grid( row = 1 , column = 1 , padx = 2 , pady = 2 )

    # Frame_MainMenu

    Frame_MovieView = MakeMovieFrames(root)[1]
    Frame_EnterMovie = MakeMovieFrames(root)[0]
    MyLabel_Movie = Button(Frame_Movies , bd = 4 , image = Images_List[0] , bg = "#b00029" , activebackground = "#ff003b",command =lambda:Movie_Main(root,Frame_Entertainment,Frame_MovieView,Frame_EnterMovie, Images_List, mycursor, mydb) ) 
    MyLabel_Movie2 = Label(Frame_Movies , text= 'Movies' , font=('Orelega One','16' , 'italic underline') )
    MyLabel_Movie2.grid( row = 0)
    MyLabel_Movie.grid( row = 1 )


    MyLabel_Tv = Button(Frame_Tv , bd = 4 ,  image = Images_List[1] , bg = "#005bb0" , activebackground = "#0084ff")
    MyLabel_Tv2 = Label(Frame_Tv , text= 'TV Shows', font=('Orelega One','16' , 'italic underline') )
    MyLabel_Tv2.grid( row = 0 )
    MyLabel_Tv.grid( row = 1 )


    MyLabel_Book = Button(Frame_Books  , bd = 4 , image = Images_List[3] , bg = "#b3bd00" , activebackground = "#f2ff00")
    MyLabel_Book2 = Label( Frame_Books , text='Books', font=('Orelega One','16' , 'italic underline') )
    MyLabel_Book2.grid( row = 0 )
    MyLabel_Book.grid( row = 1 )


    MyLabel_Game = Button(Frame_Games , bd = 4  , image = Images_List[2] , bg = "#00b509" , activebackground = "#00ff0d")
    MyLabel_Game2 = Label( Frame_Games , text='Games', font=('Orelega One','16' , 'italic underline'))
    MyLabel_Game2.grid( row = 0 )
    MyLabel_Game.grid( row = 1 )
    darkMenu_function()

def darkMenu_function():
    global dark_modeMenu,MyLabel_Movie2,Frame_Movies,Frame_Tv,Frame_Games,Frame_Books,MyLabel_Tv2,MyLabel_Game2
    if dark_modeMenu is False:
        Frame_Entertainment.configure( bg= '#1F1B24' )
        MyLabel_Movie2.configure( bg= '#1F1B24' , fg='light grey')
        Frame_Movies.configure( bg= '#1F1B24' )
        Frame_Tv.configure( bg= '#1F1B24' )
        MyLabel_Tv2.configure( bg= '#1F1B24' , fg='light grey')
        Frame_Games.configure( bg= '#1F1B24' )
        MyLabel_Game2.configure( bg= '#1F1B24' , fg='light grey')
        Frame_Books.configure( bg= '#1F1B24' )
        MyLabel_Book2.configure( bg= '#1F1B24' , fg='light grey')
        dark_modeMenu = True
    else:
        Frame_Entertainment.configure( bg = '#F0F0F0' )
        MyLabel_Movie2.configure( bg = '#F0F0F0' , fg='black' )
        Frame_Movies.configure( bg = '#F0F0F0' )
        Frame_Tv.configure( bg = '#F0F0F0' )
        MyLabel_Tv2.configure( bg = '#F0F0F0' , fg='black' )
        Frame_Games.configure( bg = '#F0F0F0' )
        MyLabel_Game2.configure( bg = '#F0F0F0' , fg='black' )
        Frame_Books.configure( bg = '#F0F0F0' )
        MyLabel_Book2.configure( bg = '#F0F0F0' , fg='black' )
        dark_modeMenu = False