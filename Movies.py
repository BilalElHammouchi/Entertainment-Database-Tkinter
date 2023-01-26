from email import message
import textwrap
import tkinter
from tkinter import BOTTOM, CENTER, END, INSERT, TOP, ttk, messagebox
from PIL import ImageTk,Image
import sys
import os
import requests
import json
from io import BytesIO
import math
import datetime
import time
from threading import Thread
import configparser
from Abstract import Abstract, resource_path
from tkinter import filedialog

class Movies(Abstract):
    def __init__(self,root):
        super().__init__(root)
        self.sorted_dictionary = { "id": 1, "name": 0, "year": 0, "genre": 0, "runtime": 0, "rating": 0, "added_time": 0, "actors": 0, "directors": 0, "franchise": 0 }
        if self.root.configparser['Options']['movie_view'] == "List":
            self.button_menuView.configure( command = self.view )
        else:
            self.button_menuView.configure( command = self.movie_posters )
    
    def main_image(self, width, height):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        theme = self.configparser['Options']['theme']
        if theme == "black" or theme == "equilux":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies black.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "blue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies blue.jpg") ).resize( (width,height) ) )
        elif theme == "alt" or theme == "classic" or theme == "default" or theme == "elegance" or theme == "scidblue" or theme == "scidgreen" \
            or theme == "scidgrey" or theme == "scidmint" or theme == "scidpink" or theme == "scidpurple" or theme == "scidsand":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies alt.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "clam":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies clam.jpg") ).resize( (width,height) ) )
        elif theme == "itft1":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies itft1.jpg") ).resize( (width,height) ) )
        elif theme == "keramik" or theme == "keramik_alt":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies keramik.jpg") ).resize( (width,height) ) )
        elif theme == "kroc":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies kroc.jpg") ).resize( (width,height) ) )
        elif theme == "winxpblue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies winxpblue.jpg") ).resize( (width,height) ) )
        else:
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best movies.jpg") ).resize( (width-2,height-2) ) )


    def enter(self):
        super().enter()
        self.button_enterSearch.configure( command = lambda: Thread( target = lambda: self.movie_search(None) ).start() )
        self.tree_select.bind("<Double-1>", lambda e, rating = 2.5, franchise = "": self.MovieSelectOnDoubleClick(e,rating,franchise,False,None,None) )
        self.button_enterSelect.configure( command = lambda: self.MovieSelectOnDoubleClick(None,2.5,"",False,None,None) )
        self.button_enterSelect.grid( row = 0, column = 1, pady = 10 )
        self.root.bind('<Return>', lambda e = None: Thread( target = lambda: self.movie_search(e) ).start() )
    
    def change_poster(self, e):
        filetypes = [('Images', '*.jpg *.jpeg *.png')]
        filename = filedialog.askopenfilename( title='Open the image poster', filetypes=filetypes )
        try:
            self.og_img = Image.open( filename ).resize( (500,750) )
            self.img_to_save = self.og_img
            self.img = ImageTk.PhotoImage( self.img_to_save )
            self.root.img_tempImages.append(self.img)
            self.label_movieEnterPoster.configure( image = self.img)
        except:
            messagebox.showerror("Error","Unable to open the image!")

    def enter_manually(self ):
        self.styleLabelEnter = ttk.Style()
        self.styleLabelEnter.configure( "Kim.TLabel", font = ("TkDefaultFont", ( self.root.winfo_width() + self.root.winfo_height() ) // 90 ) )
        font = ("TkDefaultFont", self.root.winfo_height()// 60 )
        for child in self.root.winfo_children():
            child.pack_forget()
        self.movie_id = None
        self.frame_movieEnterConfirm = ttk.Frame(self.root)
        self.frame_movieEnterConfirm.pack( fill = 'both', expand = True )
        self.og_img = Image.open( resource_path("lib/image-not-found.png") ).resize( (500,750) )
        self.img_to_save = self.og_img
        self.img = ImageTk.PhotoImage( self.img_to_save )
        self.root.img_tempImages.append(self.img)
        for i in range(3):
            tkinter.Grid.columnconfigure(self.frame_movieEnterConfirm, i, weight = 1)
        for i in range(9):
            tkinter.Grid.rowconfigure(self.frame_movieEnterConfirm, i, weight = 1)
        self.label_movieEnterPoster = ttk.Label(self.frame_movieEnterConfirm, image = self.img )
        self.label_movieEnterPoster.grid( row = 0, column = 0, rowspan = 9, sticky = "NSEW" )
        self.label_movieEnterPoster.bind("<Double-1>", self.change_poster )
        label_title = ttk.Label(self.frame_movieEnterConfirm, text = "Title", style = "Kim.TLabel" )
        label_title.grid( row = 0, column = 1, sticky = "E", padx = 10 )
        self.entry_title = ttk.Entry(self.frame_movieEnterConfirm, font = font )
        self.entry_title.grid( row = 0, column = 2, sticky = "W", padx = 10 )
        self.entry_title.insert(0, self.entry_enterSearch.get() )
        label_year = ttk.Label(self.frame_movieEnterConfirm, text = "Year", style = "Kim.TLabel" )
        label_year.grid( row = 1, column = 1, sticky = "E", padx = 10 )
        self.entry_year = ttk.Entry(self.frame_movieEnterConfirm, font = font )
        self.entry_year.grid( row = 1, column = 2, sticky = "W", padx = 10 )
        label_genre = ttk.Label(self.frame_movieEnterConfirm, text = "Genre", style = "Kim.TLabel" )
        label_genre.grid( row = 2, column = 1, sticky = "E", padx = 10 )
        genres = ('Action', 'Adventure', 'Animation', 'Biographical', 'Comedy', 'Crime Film', 'Disaster', 'Documentary', 'Drama', 'Fantasy', 
        'Horror', 'Indie', 'Martial Arts', 'Musical', 'Mystery', 'Noir', 'Romance', 'Science', 'Science Fiction', 'Short', 'Sports', 'Superhero', 
        'Thriller', 'War', 'Western')
        genres_var = tkinter.StringVar(value=genres)
        frame_listbox = ttk.Frame(self.frame_movieEnterConfirm)
        frame_listbox.grid( row = 2, column = 2, sticky = "W", padx = 10 )
        self.listbox_genre = tkinter.Listbox(frame_listbox, height = 10, selectmode = "multiple", listvariable=genres_var, exportselection=False, font = font )
        self.listbox_genre.pack( fill = 'both', side = 'left' )
        scrollbar = ttk.Scrollbar( frame_listbox, orient='vertical', command= self.listbox_genre.yview )
        self.listbox_genre['yscrollcommand'] = scrollbar.set
        scrollbar.pack( fill = 'both', side = 'right' )
        label_runtime = ttk.Label(self.frame_movieEnterConfirm, text = "Run-time", style = "Kim.TLabel" )
        label_runtime.grid( row = 3, column = 1, sticky = "E", padx = 10 )
        frame_runtime = ttk.Frame(self.frame_movieEnterConfirm)
        frame_runtime.grid( row = 3, column = 2, sticky = "W", padx = 10 )
        self.entry_hours = ttk.Entry(frame_runtime, width = 2, font = font )
        self.entry_hours.pack( side = 'left' )
        label_hours = ttk.Label(frame_runtime, text = "hour(s)", style = "Kim.TLabel" )
        label_hours.pack( side = 'left' )
        self.entry_minutes = ttk.Entry(frame_runtime, width = 2, font = font )
        self.entry_minutes.pack( side = 'left' )
        label_minutes = ttk.Label(frame_runtime, text = "minute(s)", style = "Kim.TLabel" )
        label_minutes.pack( side = 'left' )
        label_director = ttk.Label(self.frame_movieEnterConfirm, text = "Directors", style = "Kim.TLabel" )
        label_director.grid( row = 4, column = 1, sticky = "E", padx = 10 )
        frame_director = ttk.Frame(self.frame_movieEnterConfirm )
        frame_director.grid( row = 4, column = 2, sticky = "W", padx = (10,10) )
        scrollbar_director = ttk.Scrollbar(frame_director, orient = "vertical" )
        self.entry_director = tkinter.Text(frame_director, width = 20, height = 6, font = font, yscrollcommand = scrollbar_director.set )
        scrollbar_director.configure( command = self.entry_director.yview )
        scrollbar_director.pack( fill = 'both', side = 'right' )
        self.entry_director.pack( fill = 'both', side = 'left' )
        
        label_actor = ttk.Label(self.frame_movieEnterConfirm, text = "Actors", style = "Kim.TLabel" )
        label_actor.grid( row = 5, column = 1, sticky = "E", padx = 10 )
        frame_actor = ttk.Frame(self.frame_movieEnterConfirm )
        frame_actor.grid( row = 5, column = 2, sticky = "W", padx = (10,10) )
        scrollbar_actor = ttk.Scrollbar(frame_actor, orient = "vertical" )
        self.entry_actor = tkinter.Text(frame_actor, width = 20, height = 6, font = font, yscrollcommand = scrollbar_actor.set )
        scrollbar_actor.configure( command = self.entry_actor.yview )
        self.entry_actor.pack( fill = 'both', side = 'left' )
        scrollbar_actor.pack( fill = 'both', side = 'right' )
        label_franchise = ttk.Label(self.frame_movieEnterConfirm, text = "Franchise", style = "Kim.TLabel" )
        label_franchise.grid( row = 6, column = 1, sticky = "E", padx = 10 )
        self.entry_franchise = ttk.Entry(self.frame_movieEnterConfirm, font = font )
        self.entry_franchise.grid( row = 6, column = 2, sticky = "W", padx = 10 )
        self.label_ratingValue = ttk.Label(self.frame_movieEnterConfirm, text = "2.5 Stars", style = "Kim.TLabel" )
        self.label_ratingValue.grid( row = 7, column = 2, sticky = "W", padx = 10 )
        label_rating = ttk.Label(self.frame_movieEnterConfirm, text = "Rating", style = "Kim.TLabel" )
        label_rating.grid( row = 8, column = 1, sticky = "E", padx = 10 )
        #print(f"{rating = }")
        self.variable_rating = tkinter.DoubleVar()
        self.variable_rating.set(2.5)
        self.slider_changed(None)
        scale_rating = ttk.Scale(self.frame_movieEnterConfirm, from_= 0.0, to = 5.0, variable = self.variable_rating, command= self.slider_changed, length=200 )
        scale_rating.grid( row = 8, column = 2, sticky = "W", padx = 10 )
        frame_buttons = ttk.Frame(self.frame_movieEnterConfirm)
        frame_buttons.grid( row = 9, column = 0, columnspan= 3, sticky = "NSEW", pady = 10 )
        for i in range(3):
            tkinter.Grid.columnconfigure(frame_buttons, i, weight = 1 )
        button_back = ttk.Button(frame_buttons, text = "Back", command = self.movie_movieEnterConfirmToMovieEnter )
        button_back.grid( row = 0, column = 0 )
        button_reset = ttk.Button(frame_buttons, text = "Reset", command = lambda: self.movieEnterConfirmReset(self.entry_title,self.entry_year,
                    self.listbox_genre,self.entry_hours,self.entry_minutes,self.entry_director,self.entry_actor,self.entry_franchise,scale_rating) )
        button_reset.grid( row = 0, column = 1 )
        self.button_confirm = ttk.Button(frame_buttons, text = "Confirm", command = lambda:self.movieEnterConfirm(self.entry_title.get(), self.entry_year.get(), 
                    self.listbox_genre, self.entry_hours.get(), self.entry_minutes.get(), self.entry_director.get("1.0", "end-1c"), self.entry_actor.get("1.0", "end-1c"),
                    self.entry_franchise.get(), float(self.label_ratingValue['text'].split(' ')[0]), self.movie_id, self.og_img ) )
        self.button_confirm.grid( row = 0, column = 2 )
        self.frame_movieEnterConfirm.bind('<Configure>' , self.resize_select )
        self.root.center()


    def resize_select(self,e):
        self.root.update_idletasks()
        #print(f"{self.label_movieEnterPoster.winfo_width() = }\t{self.label_movieEnterPoster.winfo_height() = }")
        #print(f"{self.root.winfo_width() = }\t{self.root.winfo_height() = }")
        #self.img_to_save.thumbnail( ( self.label_movieEnterPoster.winfo_width(), self.label_movieEnterPoster.winfo_height() ), Image.ANTIALIAS )
        #self.img = ImageTk.PhotoImage( self.img_to_save )
        if int(self.label_movieEnterPoster.winfo_width()*1.5) <= self.root.winfo_height() - 20:
            self.img = ImageTk.PhotoImage( self.img_to_save.resize( ( self.label_movieEnterPoster.winfo_width() - 4, 
                                            int(self.label_movieEnterPoster.winfo_width()*1.5) - 4 ), Image.Resampling.LANCZOS  ) )
            self.label_movieEnterPoster.configure( image = self.img )
        else:
            self.img = ImageTk.PhotoImage( self.img_to_save.resize( ( int(self.root.winfo_height()*2/3) - 4, 
                                            self.root.winfo_height() - 24 ), Image.Resampling.LANCZOS  ) )
            self.label_movieEnterPoster.configure( image = self.img )
        font = ("TkDefaultFont", self.root.winfo_height()// 60 )
        self.styleLabelEnter.configure( "Kim.TLabel", font = font )
        self.entry_title.configure( font = font )
        self.entry_year.configure( font = font )
        self.listbox_genre.configure( font = font )
        self.entry_hours.configure( font = font )
        self.entry_minutes.configure( font = font )
        self.entry_director.configure( font = font )
        self.entry_actor.configure( font = font )
        self.entry_franchise.configure( font = font )


    def MovieSelectOnDoubleClick(self, event, rating, franchise, editMode,primary_key,movie_id):
        self.styleLabelEnter = ttk.Style()
        self.styleLabelEnter.configure( "Kim.TLabel", font = ("TkDefaultFont", 12))
        font = ("TkDefaultFont", 12 )
        if not movie_id:
            self.movie_id = self.tree_select.item( self.tree_select.selection()[0] )['values'][-1]
        else:
            self.movie_id = movie_id
        response = requests.get( f"https://api.themoviedb.org/3/movie/{self.movie_id}?api_key=8be65c3700e29a363aa7a71021169259&language=en-US" )
        movie_details = json.loads( response.text )
        for child in self.root.winfo_children():
            child.pack_forget()
        self.frame_movieEnterConfirm = ttk.Frame(self.root)
        self.frame_movieEnterConfirm.pack( fill = 'both', expand = True )
        self.image_response = requests.get( f"https://image.tmdb.org/t/p/w500{movie_details['poster_path']}" )
        try:
            self.og_img = Image.open(BytesIO(self.image_response.content))
            self.img_to_save = self.og_img
            self.img = ImageTk.PhotoImage( self.img_to_save.resize( (500,750) ) )
        except:
            self.og_img = Image.open( resource_path("lib/image-not-found.png") ).resize( (500,750) )
            self.img_to_save = self.og_img
            self.img = ImageTk.PhotoImage( self.img_to_save )
        self.root.img_tempImages.append(self.img)
        frame_buttons = ttk.Frame(self.frame_movieEnterConfirm)
        frame_buttons.pack(side='bottom', fill='x', pady=10)
        for i in range(3):
            tkinter.Grid.columnconfigure(frame_buttons, i, weight = 1)
        frame_upper = ttk.Frame(self.frame_movieEnterConfirm)
        frame_upper.pack(side='top', fill='both', expand=True)
        for i in range(10):
            tkinter.Grid.rowconfigure(frame_upper, i, weight = 1)
        self.label_movieEnterPoster = ttk.Label(frame_upper, image = self.img )
        self.label_movieEnterPoster.grid( row = 0, column = 0, rowspan = 10, sticky = "NSEW", padx=150)
        label_title = ttk.Label(frame_upper, text = "Title", style = "Kim.TLabel" )
        label_title.grid( row = 0, column = 1, sticky = "E", padx = 10 )
        self.entry_title = ttk.Entry(frame_upper, font = font, width=30, justify='center' )
        self.entry_title.grid( row = 0, column = 2, padx = 10 )
        self.entry_title.insert(0, movie_details['title'] )
        label_year = ttk.Label(frame_upper, text = "Year", style = "Kim.TLabel" )
        label_year.grid( row = 1, column = 1, sticky = "E", padx = 10 )
        self.entry_year = ttk.Entry(frame_upper, font = font, width=5, justify='center' )
        self.entry_year.grid( row = 1, column = 2, padx = 10 )
        self.entry_year.insert(0, movie_details['release_date'][0:4] )
        label_genre = ttk.Label(frame_upper, text = "Genre", style = "Kim.TLabel" )
        label_genre.grid( row = 2, column = 1, sticky = "E", padx = 10 )
        genres = ('Action', 'Adventure', 'Animation', 'Biographical', 'Comedy', 'Crime Film', 'Disaster', 'Documentary', 'Drama', 'Fantasy', 
        'Horror', 'Indie', 'Martial Arts', 'Musical', 'Mystery', 'Noir', 'Romance', 'Science', 'Science Fiction', 'Short', 'Sports', 'Superhero', 
        'Thriller', 'War', 'Western')
        genres_var = tkinter.StringVar(value=genres)
        frame_listbox = ttk.Frame(frame_upper)
        frame_listbox.grid( row = 2, column = 2, padx = 10 )
        self.listbox_genre = tkinter.Listbox(frame_listbox, height = 10, selectmode = "multiple", listvariable=genres_var, exportselection=False, font = font )
        self.listbox_genre.pack( fill = 'both', side = 'left' )
        i = 0
        for genre in movie_details['genres']:
            for j in range(len(genres)):
                if genre['name'] in genres[j]:
                    self.listbox_genre.selection_set( first = j )
                    break
            i += 1
            if i == 3:
                break
        scrollbar = ttk.Scrollbar( frame_listbox, orient='vertical', command= self.listbox_genre.yview )
        self.listbox_genre['yscrollcommand'] = scrollbar.set
        scrollbar.pack( fill = 'both', side = 'right' )
        label_runtime = ttk.Label(frame_upper, text = "Run-time", style = "Kim.TLabel" )
        label_runtime.grid( row = 3, column = 1, sticky = "E", padx = 10 )
        frame_runtime = ttk.Frame(frame_upper)
        frame_runtime.grid( row = 3, column = 2, padx = 10 )
        self.entry_hours = ttk.Entry(frame_runtime, width = 2, font = font, justify='center')
        self.entry_hours.pack( side = 'left' )
        self.entry_hours.insert(0, str(movie_details['runtime']//60) )
        label_hours = ttk.Label(frame_runtime, text = "hour(s)", style = "Kim.TLabel" )
        label_hours.pack( side = 'left' )
        self.entry_minutes = ttk.Entry(frame_runtime, width = 2, font = font, justify='center')
        self.entry_minutes.pack( side = 'left' )
        self.entry_minutes.insert(0, str(movie_details['runtime'] % 60) )
        label_minutes = ttk.Label(frame_runtime, text = "minute(s)", style = "Kim.TLabel" )
        label_minutes.pack( side = 'left' )
        response = requests.get( f"https://api.themoviedb.org/3/movie/{self.movie_id}/credits?api_key=8be65c3700e29a363aa7a71021169259&language=en-US" )
        credit = json.loads( response.text )
        label_director = ttk.Label(frame_upper, text = "Directors", style = "Kim.TLabel" )
        label_director.grid( row = 4, column = 1, sticky = "E", padx = 10 )
        frame_director = ttk.Frame(frame_upper )
        frame_director.grid( row = 4, column = 2, padx = (10,10) )
        scrollbar_director = ttk.Scrollbar(frame_director, orient = "vertical" )
        self.entry_director = tkinter.Text(frame_director, width = 20, height = 6, font = font, yscrollcommand = scrollbar_director.set )
        scrollbar_director.configure( command = self.entry_director.yview )
        scrollbar_director.pack( fill = 'both', side = 'right' )
        self.entry_director.pack( fill = 'both', side = 'left' )
        directors = ""
        for director in credit['crew']:
            if director['job'] == 'Director':
                directors += director['name'] + "\n"
        self.entry_director.insert(INSERT, directors)
        label_actor = ttk.Label(frame_upper, text = "Actors", style = "Kim.TLabel" )
        label_actor.grid( row = 5, column = 1, sticky = "E", padx = 10 )
        i = 0
        actors = ""
        for actor in credit['cast']:
            actors += actor['name'] + "\n"
            i += 1
            if i == 10:
                break
        frame_actor = ttk.Frame(frame_upper )
        frame_actor.grid( row = 5, column = 2, padx = (10,10) )
        scrollbar_actor = ttk.Scrollbar(frame_actor, orient = "vertical" )
        self.entry_actor = tkinter.Text(frame_actor, width = 20, height = 6, font = font, yscrollcommand = scrollbar_actor.set )
        scrollbar_actor.configure( command = self.entry_actor.yview )
        self.entry_actor.pack( fill = 'both', side = 'left' )
        scrollbar_actor.pack( fill = 'both', side = 'right' )
        self.entry_actor.insert(INSERT, actors)
        label_franchise = ttk.Label(frame_upper, text = "Franchise", style = "Kim.TLabel" )
        label_franchise.grid( row = 6, column = 1, sticky = "E", padx = 10 )
        self.entry_franchise = ttk.Entry(frame_upper, font = font, justify='center')
        self.entry_franchise.grid( row = 6, column = 2, padx = 10 )
        self.entry_franchise.insert(0,franchise)

        ttk.Label(frame_upper, text = "Times Viewed", style = "Kim.TLabel" ).grid(row = 7, column = 1, sticky = "E", padx = 10 )
        self.entry_timesWatched = ttk.Entry(frame_upper, font = font, justify='center', width=3 )
        self.entry_timesWatched.grid( row = 7, column = 2, padx = 10 )
        self.root.cur.execute("SELECT times_viewed FROM movies WHERE tmd_id = ?", (movie_details['id'],))
        result = self.root.cur.fetchone()
        if result:
            self.entry_timesWatched.insert(0, result[0]+1)
        else:
            self.entry_timesWatched.insert(0, '1')

        self.label_ratingValue = ttk.Label(frame_upper, text = "2.5 Stars", style = "Kim.TLabel" )
        self.label_ratingValue.grid( row = 8, column = 2, padx = 10 )
        label_rating = ttk.Label(frame_upper, text = "Rating", style = "Kim.TLabel" )
        label_rating.grid( row = 9, column = 1, sticky = "E", padx = 10 )
        self.variable_rating = tkinter.DoubleVar()
        self.variable_rating.set(rating)
        self.slider_changed(None)
        scale_rating = ttk.Scale(frame_upper, from_= 0.0, to = 5.0, variable = self.variable_rating, command= self.slider_changed, length=200 )
        scale_rating.grid( row = 9, column = 2, padx = 10 )
        button_back = ttk.Button(frame_buttons, text = "Back", command = self.movie_movieEnterConfirmToMovieEnter )
        button_back.grid( row = 0, column = 0 )
        button_reset = ttk.Button(frame_buttons, text = "Reset", command = lambda: self.movieEnterConfirmReset(self.entry_title,self.entry_year,
                    self.listbox_genre,self.entry_hours,self.entry_minutes,self.entry_director,self.entry_actor,self.entry_franchise,scale_rating) )
        button_reset.grid( row = 0, column = 1 )
        self.button_confirm = ttk.Button(frame_buttons, text = "Confirm", command = lambda:self.movieEnterConfirm(self.entry_title.get(), self.entry_year.get(), 
                    self.listbox_genre, self.entry_hours.get(), self.entry_minutes.get(), self.entry_director.get("1.0", "end-1c"), self.entry_actor.get("1.0", "end-1c"),
                    self.entry_franchise.get(), float(self.label_ratingValue['text'].split(' ')[0]), self.movie_id, self.og_img ) )
        self.button_confirm.grid( row = 0, column = 2 )
        if editMode:
            self.button_confirm.configure( command = lambda:self.edit_confirm(self.entry_title.get(), self.entry_year.get(), 
                    self.listbox_genre, self.entry_hours.get(), self.entry_minutes.get(), self.entry_director.get("1.0", "end-1c"), self.entry_actor.get("1.0", "end-1c"),
                    self.entry_franchise.get(), float(self.label_ratingValue['text'].split(' ')[0]), self.movie_id, self.og_img, primary_key ) )
            if self.root.configparser['Options']['movie_view'] == "List":
                button_back.configure( command = self.view )
            else:
                button_back.configure( command = self.movie_posters )
        self.frame_movieEnterConfirm.bind('<Configure>' , self.resize_select )
        self.root.center()
        

    def movieEnterConfirmReset(self,entry_title,entry_year,listbox_genre,entry_hours,entry_minutes,entry_director,entry_actor,entry_franchise,scale_rating):
        entry_title.delete(0,END)
        entry_year.delete(0,END)
        listbox_genre.selection_clear(0, END)
        entry_hours.delete(0,END)
        entry_minutes.delete(0,END)
        entry_director.delete('1.0', END)
        entry_actor.delete('1.0', END)
        entry_franchise.delete(0,END)
        scale_rating.set(2.5)

    def confirm_GenreFranchise(self,listbox,franchise):
        genre1 = genre2 = genre3 = None
        if len(listbox.curselection()) > 0:
            genre1 = listbox.curselection()[0] + 1
        if len(listbox.curselection()) > 1:
            genre2 = listbox.curselection()[1] + 1
        if len(listbox.curselection()) > 2:
            genre3 = listbox.curselection()[2] + 1
        franchise_id = None
        if franchise:
            self.root.cur.execute("SELECT * FROM movie_franchises WHERE name = ?", (franchise,) )
            franchise_row = self.root.cur.fetchone()
            if franchise_row:
                franchise_id = franchise_row[0]
            else:
                self.root.cur.execute("INSERT INTO movie_franchises (name) VALUES (?) ", (franchise,) )
                self.root.con.commit()
                franchise_id = self.root.cur.lastrowid
        return [genre1,genre2,genre3,franchise_id]

    def confirm_actorsDirectorsImage(self,directors,actors,img_to_save,primary_key):
        for director in directors.split('\n'):
            if director:
                self.root.cur.execute("SELECT id FROM directors WHERE name = ? ", (director,) )
                director_id = self.root.cur.fetchone()
                if not director_id:
                    self.root.cur.execute("INSERT INTO directors(name) VALUES(?) ", (director,) )
                    director_id = self.root.cur.lastrowid
                else:
                    director_id = director_id[0]
                try:
                    self.root.cur.execute("INSERT INTO movie_directing(movieid,directorid) VALUES (?,?) ", (primary_key,director_id) )
                except:
                    pass
        for actor in actors.split('\n'):
            if actor:
                self.root.cur.execute("SELECT id FROM actors WHERE name = ? ", (actor,) )
                actor_id = self.root.cur.fetchone()
                if not actor_id:
                    self.root.cur.execute("INSERT INTO actors(name) VALUES(?) ", (actor,) )
                    actor_id = self.root.cur.lastrowid
                else:
                    actor_id = actor_id[0]
                try:
                    self.root.cur.execute("INSERT INTO movie_castings(movieid,actorid) VALUES (?,?) ", (primary_key,actor_id) )
                except:
                    pass
        self.root.con.commit()
        img_to_save.save(f"Images/Movies/{primary_key}.jpg")

    def edit_confirm(self,title,year,listbox,hours,minutes,directors,actors,franchise,rating,movie_id,img_to_save,primary_key):
        results = self.confirm_GenreFranchise(listbox,franchise)
        genre1 = results[0]
        genre2 = results[1]
        genre3 = results[2]
        franchise_id = results[3]
        self.root.cur.execute("""UPDATE movies SET name = ?, year = ?, genre1 = ?, genre2 = ?, genre3 = ?, runtime = ?, rating = ?,  
                                franchise = ?, tmd_id = ? WHERE id = ?""", (title, int(year), genre1, genre2, genre3, int(hours)*60 + int(minutes),
                                rating, franchise_id, movie_id, primary_key )  )

        self.root.cur.execute("DELETE FROM movie_directing WHERE movieid = ?", (primary_key,) )
        self.root.cur.execute("DELETE FROM movie_castings WHERE movieid = ?", (primary_key,) )
        self.confirm_actorsDirectorsImage(directors,actors,img_to_save,primary_key)
        self.view()

    def movieEnterConfirm(self,title,year,listbox,hours,minutes,directors, actors, franchise, rating, movie_id, img_to_save ):
        results = self.confirm_GenreFranchise(listbox,franchise)
        genre1 = results[0]
        genre2 = results[1]
        genre3 = results[2]
        franchise_id = results[3]
        self.root.cur.execute("SELECT tmd_id FROM movies")
        results = self.root.cur.fetchall()
        if any(movie_id in sl for sl in results):
            self.root.cur.execute("""UPDATE movies SET name = ?, year = ?, genre1 = ?, genre2 = ?, genre3 = ?, Runtime = ?, Rating = ?,
                                franchise = ?, times_viewed = ? WHERE tmd_id = ?""", 
                                (title, int(year),genre1,genre2,genre3,int(hours)*60 + int(minutes), rating, 
                                franchise_id, self.entry_timesWatched.get(), movie_id) )
            self.root.con.commit()
        else:
            self.root.cur.execute("""INSERT INTO movies (name, year, genre1, genre2, genre3, runtime, rating, added_time, franchise, tmd_id, times_viewed) 
                                VALUES (?,?,?,?,?,?,?,?,?,?, ?)""", (title,int(year),genre1,genre2,genre3,int(hours)*60 + int(minutes), rating, 
                                datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), franchise_id, movie_id, self.entry_timesWatched.get()) )
            sql_id = self.root.cur.lastrowid
            self.confirm_actorsDirectorsImage(directors,actors,img_to_save,sql_id)
        self.movie_movieEnterConfirmToMovieEnter()


    def movie_movieEnterConfirmToMovieEnter(self):
        self.frame_movieEnterConfirm.pack_forget()
        self.frame_enter.pack( expand = True, fill = "both")

            
    def movie_search(self, e):
        if not self.entry_enterSearch.get():
            messagebox.showerror("Error","Please provide a name before searching!")
            return
        response = requests.get( f"https://api.themoviedb.org/3/search/movie?api_key=8be65c3700e29a363aa7a71021169259&query={self.entry_enterSearch.get()}")
        response = json.loads( response.text )['results']
        self.root.img_tempImages.clear()
        self.tree_select.delete(*self.tree_select.get_children())
        for result in response:
            try:
                release_date = datetime.datetime.strptime( result['release_date'], "%Y-%m-%d" ).strftime("%B %d, %Y")
            except:
                release_date = "TBD"
            description_result = result['overview']
            description = '\n'.join(textwrap.wrap(description_result, 150))
            self.tree_select.insert('', 'end', values= ( result['title'], release_date, description, result['id'] ) )
        for i in range(len(response)):
            Thread( target = self.movie_searchPosters(response[i], i) ).start()


    def movie_searchPosters(self, result, index):
        image_response = requests.get( f"https://image.tmdb.org/t/p/w92{result['poster_path']}" )
        try:
            img = ImageTk.PhotoImage( Image.open(BytesIO(image_response.content)) )
        except:
            img = ImageTk.PhotoImage( Image.open( resource_path("lib/image-not-found.png") ).resize( (92,92) ) )
        self.root.img_tempImages.append(img)
        item_ = self.tree_select.get_children()[index]
        self.tree_select.item(item_, image = img)


    def sort_tree(self,option,start):   # method to sort treeview when clicking on columns
        for key in self.sorted_dictionary.keys():   # Reset counter for all columns
            if key != option:
                self.sorted_dictionary[key] = 0
        if start and self.sorted_dictionary[option] == 0:
            self.sorted_dictionary[option] = 1
        elif start and self.sorted_dictionary[option] == 1:
            self.sorted_dictionary[option] = 0
        self.view_tree.delete(  *self.view_tree.get_children()  )
        sql_query = """SELECT movies.id, movies.name, year, g1.name, g2.name, g3.name, runtime, rating, added_time, movie_franchises.name, movies.tmd_id
                                    FROM movies LEFT JOIN genres g1 ON movies.genre1 = g1.id 
                                                LEFT JOIN genres g2 ON movies.genre2 = g2.id 
                                                LEFT JOIN genres g3 ON movies.genre3 = g3.id
                                                LEFT JOIN movie_franchises on movies.franchise = movie_franchises.id """
        options = [ "id", "name", "year", "runtime", "rating", "added_time" ]
        for o in options:
            if option == o and self.sorted_dictionary[o] == 0:
                self.root.cur.execute( f"{sql_query} ORDER BY movies.{o}")
                self.sorted_dictionary[o] = 1
                self.sorted_option = o
                break
            elif option == o and self.sorted_dictionary[o] == 1:
                self.root.cur.execute( f"{sql_query} ORDER BY movies.{o} DESC")
                self.sorted_dictionary[o] = 0
                self.sorted_option = o
                break
        if option == "genre" and self.sorted_dictionary["genre"] == 0:
            self.root.cur.execute( f"{sql_query} ORDER BY movies.genre1, movies.genre2, movies.genre3")
            self.sorted_dictionary["genre"] = 1
            self.sorted_option = "genre"
        elif option == "genre" and self.sorted_dictionary["genre"] == 1:
            self.root.cur.execute( f"{sql_query} ORDER BY movies.genre1 DESC, movies.genre2 DESC, movies.genre3 DESC")
            self.sorted_dictionary["genre"] = 0
            self.sorted_option = "genre"
        elif option == "franchise" and self.sorted_dictionary["franchise"] == 0:
            self.root.cur.execute( f"{sql_query} ORDER BY movie_franchises.name")
            self.sorted_dictionary["franchise"] = 1
            self.sorted_option = "franchise"
        elif option == "franchise" and self.sorted_dictionary["franchise"] == 1:
            self.root.cur.execute( f"{sql_query} ORDER BY movie_franchises.name DESC")
            self.sorted_dictionary["franchise"] = 0
            self.sorted_option = "franchise"
        self.movie_records = self.root.cur.fetchall()
        for i in range( 0, len(self.movie_records) ):
            self.select_rest(i)
            self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                    self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                    self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )

    def select_rest(self,i):
        self.genres = ""
        if self.movie_records[i][3]:
            self.genres = self.movie_records[i][3]
        if self.movie_records[i][4]:
            self.genres += ", " + self.movie_records[i][4]
        if self.movie_records[i][5]:
            self.genres += ", " + self.movie_records[i][5]
        self.runtime = ""
        if self.movie_records[i][6]//60:
            self.runtime = f"{str(self.movie_records[i][6]//60)}h"
        if self.movie_records[i][6] % 60:
            self.runtime += f" {self.movie_records[i][6] % 60}m"
        self.directors = ""
        self.root.cur.execute("""SELECT directors.name FROM movie_directing INNER JOIN directors ON movie_directing.directorid = directors.id WHERE movieid = ?""", 
                        (self.movie_records[i][0],) )
        director_result = self.root.cur.fetchall()
        for j in range( 0, len(director_result) ):
            if j == 0:
                self.directors += director_result[j][0]
            else:
                self.directors += ", " + director_result[j][0]
        self.actors = ""
        self.root.cur.execute("""SELECT actors.name FROM movie_castings INNER JOIN actors ON movie_castings.actorid = actors.id WHERE movieid = ?""", 
                        (self.movie_records[i][0],) )
        actor_result = self.root.cur.fetchall()
        for j in range( 0, len(actor_result)  ):
            if j == 0:
                self.actors += actor_result[j][0]
            else:
                self.actors += ", " + actor_result[j][0]
        self.franchise = ""
        if self.movie_records[i][9]:
            self.franchise = self.movie_records[i][9]

    def view_search(self, var, index, mode):
        #print(f"{self.var_search.get() = }\t{self.var_search2.get() = }")
        if self.var_search.get():
            self.view_tree.delete(  *self.view_tree.get_children()  )
            dictio = {"ID": 0, "Title": 1, "Year": 2, "Genre": 3, "Runtime": 4, "Rating": 7, "Date added": 8, "Actor": 9, "Director": 11, "Franchise": 10}
            self.search_filter( dictio[self.var_search2.get()] )
        else:
            try:
                self.view_tree.delete(  *self.view_tree.get_children()  )
                for i in range( 0, len(self.movie_records) ):
                    self.select_rest(i)
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                            self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                            self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            except Exception as e:
                print(e)

    def search_filter(self, column ):
        #print(f"{self.movie_records}")
        for i in range( 0, len(self.movie_records) ):
            self.select_rest(i)
            if column == 0 or column == 2 or column == 7:
                try:
                    if self.var_search.get() == self.movie_records[i][column] or float(self.var_search.get()) == self.movie_records[i][column]:
                        self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                            self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                            self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
                except:
                    pass
            elif column == 3:
                if self.var_search.get().lower() in self.genres.lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            elif column == 4:
                if self.var_search.get().lower() in self.runtime.lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            elif column == 9:
                if self.var_search.get().lower() in self.actors.lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            elif column == 11:
                if self.var_search.get().lower() in self.directors.lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            elif column == 10:
                if self.var_search.get().lower() in self.franchise.lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
            else:
                if self.var_search.get().lower() in self.movie_records[i][column].lower():
                    self.view_tree.insert("", END, values = (self.movie_records[i][0], self.movie_records[i][1], self.movie_records[i][2], 
                                                        self.genres, self.runtime, self.movie_records[i][7], self.movie_records[i][8], self.actors,
                                                        self.directors, self.franchise, self.movie_records[i][10] ), iid=str(i) )
    
    def view(self):
        super().view()
        self.root.configparser['Options'][ 'movie_view' ] = 'List'
        with open('lib/configuration.ini', 'w') as configfile:
            self.root.configparser.write(configfile)
        self.combobox_search['values'] = ('ID','Title','Year','Genre','Runtime', 'Times Viewed', 'Rating','Date added','Actor','Director','Franchise')
        self.combobox_search['state'] = "readonly"
        self.combobox_search.set("Title")
        self.view_tree.configure( column=("c1", "c2", "c3" , "c4" , "c5" , "c6" , "c7" , "c8" , "c9", "c10", ) )
        self.view_tree.column("#1", anchor= CENTER, width = 50 )
        self.view_tree.heading("#1", text="ID", command = lambda: self.sort_tree('id',False) )
        self.view_tree.column("#2", anchor= CENTER, width = 350 )
        self.view_tree.heading("#2", text="Title", command = lambda: self.sort_tree('name',False) )
        self.view_tree.column("#3", anchor= CENTER, width = 50 )
        self.view_tree.heading("#3", text="Year", command = lambda: self.sort_tree('year',False) )
        self.view_tree.column("#4", anchor= CENTER, width = 200 )
        self.view_tree.heading("#4", text="Genre", command = lambda: self.sort_tree('genre',False) )
        self.view_tree.column("#5", anchor= CENTER, width = 60 )
        self.view_tree.heading("#5", text="Runtime", command = lambda: self.sort_tree('runtime',False) )
        self.view_tree.column("#6", anchor= CENTER, width = 45 )
        self.view_tree.heading("#6", text="Rating", command = lambda: self.sort_tree('rating',False) )
        self.view_tree.column("#7", anchor= CENTER, width = 100 )
        self.view_tree.heading("#7", text="Date added", command = lambda: self.sort_tree('added_time',False) )
        self.view_tree.column("#8", anchor= CENTER, width = 50 ) 
        self.view_tree.heading("#8", text= "Actors" )
        self.view_tree.column("#9", anchor= CENTER, width = 200 )
        self.view_tree.heading("#9", text= "Director" )
        self.view_tree.column("#10", anchor= CENTER, width = 150 )
        self.view_tree.heading("#10", text="Franchise", command = lambda: self.sort_tree('franchise',False) )
        self.sort_tree( self.sorted_option, True )
        self.button_movieEdit = ttk.Button(self.frame_view, text = "Edit", command = lambda: Thread( target = self.movie_edit ).start() )
        self.button_movieEdit.grid( row = 2, column = 1, pady = 10 )
        self.button_movieDelete = ttk.Button(self.frame_view, text = "Delete", command = self.movie_delete )
        self.button_movieDelete.grid( row = 2, column = 2, pady = 10 )
        self.button_moviePosters = ttk.Button(self.frame_view, text = "Posters", command = self.movie_posters )
        self.button_moviePosters.grid( row = 2, column = 3, pady = 10 )
        self.root.center()


    def to_menu(self):
        super().to_menu()
        if self.root.configparser['Options']['movie_view'] == "List":
            self.button_menuView.configure( command = self.view )
        else:
            self.button_menuView.configure( command = self.movie_posters )


    def searchToView(self):
        self.frame_movieEnter.pack_forget()
        self.frame_movieView.pack( expand = True, fill = "both")
        self.root.center()


    def movie_edit(self):
        if self.view_tree.selection():
            for item in self.view_tree.selection():
                item_text = self.view_tree.item(item)
                if item_text['values'][10] == 'None':
                    if messagebox.askyesno("TMD",f"No connection found with the movie database, do you want to search '{item_text['values'][1]}'?"):
                        self.enter()
                        self.entry_movieEnterSearch.insert(0,item_text['values'][1])
                        self.button_movieEnterBack.configure( command = self.searchToView )
                        self.tree_select.bind("<Double-1>", lambda e, rating = item_text['values'][5], primary_key = item_text['values'][0],
                                                    franchise = item_text['values'][9]: self.MovieSelectOnDoubleClick(e,rating,franchise,True,primary_key,None) )
                        Thread( target = self.movie_search(None) ).start()
                else:
                    self.MovieSelectOnDoubleClick(None,item_text['values'][5],item_text['values'][9],True,item_text['values'][0],item_text['values'][10])
        else:
            messagebox.showerror("Error","No movie selected! Select a movie from the list first.")
    
    def movie_delete(self):
        if self.view_tree.selection():
            for item in self.view_tree.selection():
                item_text = self.view_tree.item(item)
                if messagebox.askyesno("Delete Movie",f"Are you sure you want to delete {item_text['values'][1]}?"):
                    self.root.cur.execute("DELETE FROM movies WHERE id = ?", (item_text['values'][0], ) )
                    self.root.cur.execute("DELETE FROM movie_castings WHERE movieid = ?", (item_text['values'][0], ) )
                    self.root.cur.execute("DELETE FROM movie_directing WHERE movieid = ?", (item_text['values'][0], ) )
                    self.root.con.commit()
                    os.remove(f"Images/Movies/{item_text['values'][0]}.jpg")
                    self.frame_view.pack_forget()
                    self.view()
        else:
            messagebox.showerror("Error","No movie selected! Select a movie from the list first.")

    def _on_mouse_wheel(self,e):
        self.canvas_poster.yview_scroll(-1 * int((e.delta / 120)), "units")


    def movie_posters(self):
        start = time.time()
        self.root.configparser['Options'][ 'movie_view' ] = 'Posters'
        with open('lib/configuration.ini', 'w') as configfile:
            self.root.configparser.write(configfile)
        self.root.img_tempImages.clear()
        for child in self.root.winfo_children():
            child.pack_forget()
        self.frame_poster = ttk.Frame(self.root)
        self.frame_poster.pack( expand = True, fill = "both" )
        self.frame_poster_up = ttk.Frame(self.frame_poster)
        self.frame_poster_up.pack( expand = True, fill = "both", side = "top" )
        self.frame_poster_down = ttk.Frame(self.frame_poster)
        self.frame_poster_down.pack( expand = False, fill = "x", side = "bottom", pady = 10 )
        self.canvas_poster = tkinter.Canvas(self.frame_poster_up )
        self.canvas_poster.pack( side = "left", fill = "both", expand = True)
        self.scrollbar_poster = ttk.Scrollbar(self.frame_poster_up, orient = "vertical", command = self.canvas_poster.yview )
        self.scrollbar_poster.pack( side = "right", fill = "y" )
        self.canvas_poster.configure( yscrollcommand = self.scrollbar_poster.set )
        self.canvas_poster.bind('<Configure>', lambda e: self.canvas_poster.configure( scrollregion = self.canvas_poster.bbox("all") )  )
        self.frame_poster_indented = ttk.Frame(self.canvas_poster)
        self.canvas_poster.create_window( (0,0), window = self.frame_poster_indented, anchor = "nw" )
        self.canvas_poster.bind_all("<MouseWheel>", self._on_mouse_wheel)

        for i in range(4):
            tkinter.Grid.columnconfigure(self.frame_poster_down, i, weight = 1 )
        self.button_PosterBack = ttk.Button(self.frame_poster_down, text = "Back", command = self.to_menu )
        self.button_PosterBack.grid( row = 1, column = 0, pady = 10 )
        self.button_PosterEdit = ttk.Button(self.frame_poster_down, text = "Edit", command = self.poster_edit )
        self.button_PosterEdit.grid( row = 1, column = 1, pady = 10 )
        self.button_PosterDelete = ttk.Button(self.frame_poster_down, text = "Delete", command = self.poster_delete )
        self.button_PosterDelete.grid( row = 1, column = 2, pady = 10 )
        self.button_PosterList = ttk.Button(self.frame_poster_down, text = "List", command = self.view )
        self.button_PosterList.grid( row = 1, column = 3, pady = 10 )

        i = j = 0
        try:
            self.movie_records
        except:
            self.root.cur.execute("""SELECT movies.id, movies.name, year, g1.name, g2.name, g3.name, runtime, rating, added_time, movie_franchises.name, movies.tmd_id
                                    FROM movies LEFT JOIN genres g1 ON movies.genre1 = g1.id 
                                                LEFT JOIN genres g2 ON movies.genre2 = g2.id 
                                                LEFT JOIN genres g3 ON movies.genre3 = g3.id
                                                LEFT JOIN movie_franchises on movies.franchise = movie_franchises.id ORDER BY added_time DESC""")
            self.movie_records = self.root.cur.fetchall()
        self.selected_poster = False
        styleButton = ttk.Style()
        styleButton.configure( "Kim.TButton", anchor = "center" )
        while i*6 + j < len(self.movie_records):
            b = ttk.Button(self.frame_poster_indented, text = self.parse_posters(self.movie_records[i*6 + j] ), compound = TOP,
                            command = lambda i = i, j = j: self.poster_selection(i,j), style = "Kim.TButton" )
            b.grid( row = i, column = j )
            j += 1
            if j == 6:
                i += 1
                j = 0
        self.posters_width = 260*6
        Thread( target = self.fill_images ).start()
        self.root.center()
        self.frame_poster.bind('<Configure>', self.resize_posters )
        end = time.time()
        print( "it took",end - start, "seconds")


    def parse_posters(self, movie_record):
        text = ""
        if self.root.configparser['Movie Posters']['ID'] == "1":
            text += "ID: " + str(movie_record[0]) + "\n"
        if self.root.configparser['Movie Posters']['Title'] == "1":
            text += "Title: " + movie_record[1] + "\n"
        if self.root.configparser['Movie Posters']['Year'] == "1":
            text += "Year: " + str(movie_record[2]) + "\n"
        if self.root.configparser['Movie Posters']['Genre'] == "1":
            text += "Genre: " + movie_record[3]
            if movie_record[4]:
                text += ", " + movie_record[4]
            if movie_record[5]:
                text += ", " + movie_record[5]
            text += "\n"
        if self.root.configparser['Movie Posters']['Runtime'] == "1":
            text += "Runtime: "
            if movie_record[6] //60:
                text += f"{str(movie_record[6] //60)}h"
            if movie_record[6] % 60:
                text += f" {movie_record[6] % 60}m"
            text += "\n"
        if self.root.configparser['Movie Posters']['Rating'] == "1":
            text += "Rating: " + str(movie_record[7]) + " Stars" + "\n"
        if self.root.configparser['Movie Posters']['Date added'] == "1":
            text += "Date added: " + movie_record[8] + "\n"
        if self.root.configparser['Movie Posters']['Director'] == "1":
            self.root.cur.execute("""SELECT directors.name FROM movie_directing INNER JOIN directors ON movie_directing.directorid = directors.id WHERE movieid = ?""", 
                        (movie_record[0], ) )
            director_result = self.root.cur.fetchall()
            for j in range( 0, len(director_result) ):
                if j == 0:
                    text += "Director: " + director_result[j][0]
                else:
                    text += ", " + director_result[j][0]
            text += "\n"
        if self.root.configparser['Movie Posters']['Actors'] == "1":
            self.root.cur.execute("""SELECT actors.name FROM movie_castings INNER JOIN actors ON movie_castings.actorid = actors.id WHERE movieid = ?""", 
                        (movie_record[0], ) )
            actor_result = self.root.cur.fetchall()
            for j in range( 0, len(actor_result)  ):
                if j == 0:
                    text += "Actors: " + actor_result[j][0]
                else:
                    text += ", " + actor_result[j][0]
            text += "\n"
        if self.root.configparser['Movie Posters']['Franchise'] == "1" and movie_record[9]:
            text += "Franchise: " + movie_record[9] + "\n"
        text = text[:len(text)-1]
        correct_text = ""
        a = 0
        for line in text.split('\n'):
            for word in line.split(' '):
                if a + len(word) > 37:
                    correct_text += "\n"
                    a = 0
                correct_text += word + " "
                a += len(word)
            correct_text += "\n"
            a = 0
        return correct_text[:len(correct_text)-1]


    def resize_posters(self, e ):
        if self.posters_width > self.frame_poster.winfo_width() or self.posters_width < self.frame_poster.winfo_width() - 260:
            j = i = k = 0
            self.posters_width = 0
            while self.posters_width <= self.frame_poster.winfo_width():
                self.posters_width += 260
                j += 1
            for child in self.frame_poster_indented.winfo_children():
                child.grid_configure( row = i, column = k )
                k += 1
                if k == j:
                    k = 0
                    i += 1
    
    def poster_edit(self ):
        if self.selected_poster:
            if self.selected_poster[10] == 'None':
                if messagebox.askyesno("TMD",f"No connection found with the movie database, do you want to search '{self.selected_poster[1]}'?"):
                    self.enter()
                    self.entry_movieEnterSearch.insert(0,self.selected_poster[1])
                    self.button_movieEnterBack.configure( command = self.searchToView )
                    self.tree_select.bind("<Double-1>", lambda e, rating = self.selected_poster[7], primary_key = self.selected_poster[0],
                                                franchise = self.selected_poster[9]: self.MovieSelectOnDoubleClick(e,rating,franchise,True,primary_key,None) )
                    Thread( target = self.movie_search(None) ).start()
            else:
                if self.selected_poster[9]:
                    franchise = self.selected_poster[9]
                else:
                    franchise = ""
                self.MovieSelectOnDoubleClick(None,self.selected_poster[7],franchise,True,self.selected_poster[0],self.selected_poster[10])

        else:
            messagebox.showerror("Error","No movie selected! Click on a movie poster first.")

    def poster_delete(self ):
        if self.selected_poster and messagebox.askyesno("Delete Movie",f"Are you sure you want to delete {self.selected_poster[1]}?"):
                self.root.cur.execute("DELETE FROM movies WHERE id = ?", (self.selected_poster[0], ) )
                self.root.cur.execute("DELETE FROM movie_castings WHERE movieid = ?", (self.selected_poster[0], ) )
                self.root.cur.execute("DELETE FROM movie_directing WHERE movieid = ?", (self.selected_poster[0], ) )
                self.root.con.commit()
                os.remove(f"Images/Movies/{self.selected_poster[0]}.jpg")
                self.movie_posters()
        else:
            messagebox.showerror("Error","No movie selected! Click on a movie poster first.")
    
    def fill_images(self ):
        for i in range(len(self.movie_records)):
            try:
                img = ImageTk.PhotoImage( Image.open( f"Images/Movies/{self.movie_records[i][0]}.jpg" ).resize( (260,390), Image.Resampling.LANCZOS )  )
            except:
                img = ImageTk.PhotoImage( Image.open( f"lib/image-not-found.png" ).resize( (260,390), Image.Resampling.LANCZOS )  )
            self.frame_poster_indented.winfo_children()[i].configure( image = img )
            self.root.img_tempImages.append(img)
            if i % 12 == 0:
                self.canvas_poster.configure( scrollregion = self.canvas_poster.bbox("all") )
        self.canvas_poster.configure( scrollregion = self.canvas_poster.bbox("all") )

    def poster_selection(self,i,j):
        self.selected_poster = self.movie_records[i*6 + j]