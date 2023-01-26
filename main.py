import tkinter
from tkinter import ttk
import sys
import os
from PIL import ImageTk ,Image
from ttkthemes import ThemedStyle
import sqlite3
import configparser
from Movies import Movies
from Shows import Shows
from Books import Books
from Games import Games

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class Entertainment(tkinter.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Entertainment Tracker")
        program_menu = tkinter.Menu(self)
        self.config(menu=program_menu)
        file_menu = tkinter.Menu(program_menu)
        program_menu.add_cascade(label="Theme", menu=file_menu )
        self.preferences_menu = tkinter.Menu(program_menu)
        program_menu.add_cascade(label="Preferences", menu = self.preferences_menu )
        self.configuration()
        self.protocol( "WM_DELETE_WINDOW" , self.destroy_app )
        self.theme = ThemedStyle(self)
        self.switch_theme(self.theme_found)
        self.theme_names = self.theme.theme_names()
        self.theme_names.sort()
        for theme in self.theme_names:
            file_menu.add_command(label= theme , command = lambda theme = theme:self.switch_theme(theme) )
        self.con = sqlite3.connect( "lib/EntertainmentDatabase.db" )
        self.cur = self.con.cursor()
        self.iconbitmap( default = resource_path( "lib/popcorn.ico") )
        self.img_tempImages = []
        self.preferences_menu.add_command( label = "Movie Posters", command = self.poster_preferences )
        self.main_menu()
        self.center()

    def switch_theme(self,theme):
        self.theme.set_theme(theme)
        styleButton = ttk.Style()
        styleButton.configure( "Kim.TButton", anchor = "center" )
        styleButton.configure('Poster.Treeview', rowheight = 140)
        self.configparser['Options']['theme'] = theme
        with open('lib/configuration.ini', 'w') as configfile:
            self.configparser.write(configfile)
        try:
            self.movies.main_image( self.label_movieMenuImg.winfo_width() - 4, self.label_movieMenuImg.winfo_height() - 4 )
        except:
            pass

    def configuration(self):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        if self.configparser['Options']['maximized'] == "True":
            self.state("zoomed")
        self.theme_found = self.configparser['Options']['theme']

    def main_menu(self):
        self.frame_mainMenu = ttk.Frame(self )
        self.frame_mainMenu.pack( expand = True, fill = 'both' )
        for i in range(2):
            tkinter.Grid.columnconfigure(self.frame_mainMenu, i, weight = 1 )
            tkinter.Grid.rowconfigure(self.frame_mainMenu, i, weight = 1 )
        #self.button_movie = ttk.Button(self.frame_mainMenu, image = self.img_movie, command = self.start_movies, text = "Movies", compound = BOTTOM, style = "Kim.TButton" )
        self.img_movie = ImageTk.PhotoImage( Image.open( resource_path("lib/clapperboard.png") ).resize( (150,150), Image.Resampling.LANCZOS )  )
        self.img_tv = ImageTk.PhotoImage( Image.open( resource_path("lib/tv-show.png") ).resize( (150,150), Image.Resampling.LANCZOS )  )
        self.img_game = ImageTk.PhotoImage( Image.open( resource_path("lib/console.png") ).resize( (150,150), Image.Resampling.LANCZOS )  )
        self.img_book = ImageTk.PhotoImage( Image.open( resource_path("lib/open-book.png") ).resize( (150,150), Image.Resampling.LANCZOS )  )
        self.button_movie = ttk.Button(self.frame_mainMenu, image = self.img_movie, command = self.start_movies, style = "Kim.TButton" )
        self.button_movie.grid( row = 0, column = 0, sticky = "NSEW" )
        self.button_tv = ttk.Button(self.frame_mainMenu, image = self.img_tv, text = "TV Shows", command = self.start_shows, style = "Kim.TButton" )
        self.button_tv.grid( row = 0, column = 1, sticky = "NSEW" )
        self.button_game = ttk.Button(self.frame_mainMenu, image = self.img_game, text = "Games", command = self.start_games, style = "Kim.TButton" )
        self.button_game.grid( row = 1, column = 0, sticky = "NSEW" )
        self.button_book = ttk.Button(self.frame_mainMenu, image = self.img_book, text = "Books", command = self.start_books, style = "Kim.TButton" )
        self.button_book.grid( row = 1, column = 1, sticky = "NSEW" )


    def start_games(self):
        self.games = Games(self)
        

    def start_books(self):
        self.books = Books(self)


    def start_movies(self):
        self.movies = Movies(self)


    def start_shows(self):
        self.shows = Shows(self)


    def poster_preferences(self):
        self.preferences_window = tkinter.Toplevel()
        self.preferences_frame = ttk.Frame(self.preferences_window )
        self.preferences_frame.pack( expand = True, fill = "both" )
        self.label = ttk.Label(self.preferences_frame, text = "Show: " )
        self.label.grid( row = 0, column = 0, rowspan = 2, padx = 20, pady = 10 )
        self.configparser.read('lib/configuration.ini')
        self.var_moviePosterid = tkinter.IntVar()
        self.checkbutton_id = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterid, onvalue = 1, offvalue = 0, text = "ID", command = self.write_preferences )
        self.checkbutton_id.grid( row = 0, column = 1, padx = 15, sticky = "W" )
        self.var_moviePostertitle = tkinter.IntVar()
        self.checkbutton_title = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePostertitle, onvalue = 1, offvalue = 0, text = "Title", command = self.write_preferences )
        self.checkbutton_title.grid( row = 0, column = 2, padx = 15, sticky = "W" )
        self.var_moviePosteryear = tkinter.IntVar()
        self.checkbutton_year = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosteryear, onvalue = 1, offvalue = 0, text = "Year", command = self.write_preferences )
        self.checkbutton_year.grid( row = 0, column = 3, padx = 15, sticky = "W" )
        self.var_moviePostergenre = tkinter.IntVar()
        self.checkbutton_genre = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePostergenre, onvalue = 1, offvalue = 0, text = "Genre", command = self.write_preferences )
        self.checkbutton_genre.grid( row = 0, column = 4, padx = 15, sticky = "W" )
        self.var_moviePosterruntime = tkinter.IntVar()
        self.checkbutton_runtime = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterruntime, onvalue = 1, offvalue = 0, text = "Runtime", command = self.write_preferences )
        self.checkbutton_runtime.grid( row = 0, column = 5, padx = 15, sticky = "W" )
        self.var_moviePosterrating = tkinter.IntVar()
        self.checkbutton_rating = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterrating, onvalue = 1, offvalue = 0, text = "Rating", command = self.write_preferences )
        self.checkbutton_rating.grid( row = 1, column = 1, padx = 15, sticky = "W" )
        self.var_moviePosterdate = tkinter.IntVar()
        self.checkbutton_date = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterdate, onvalue = 1, offvalue = 0, text = "Date added", command = self.write_preferences )
        self.checkbutton_date.grid( row = 1, column = 2, padx = 15, sticky = "W" )
        self.var_moviePosterdirector = tkinter.IntVar()
        self.checkbutton_director = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterdirector, onvalue = 1, offvalue = 0, text = "Director", command = self.write_preferences )
        self.checkbutton_director.grid( row = 1, column = 3, padx = 15, sticky = "W" )
        self.var_moviePosteractors = tkinter.IntVar()
        self.checkbutton_actors = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosteractors, onvalue = 1, offvalue = 0, text = "Actors", command = self.write_preferences )
        self.checkbutton_actors.grid( row = 1, column = 4, padx = 15, sticky = "W" )
        self.var_moviePosterfranchise = tkinter.IntVar()
        self.checkbutton_franchise = ttk.Checkbutton(self.preferences_frame, variable = self.var_moviePosterfranchise, onvalue = 1, offvalue = 0, text = "Franchise", command = self.write_preferences )
        self.checkbutton_franchise.grid( row = 1, column = 5, padx = 15, sticky = "W" )
        dict_ = {'ID': self.var_moviePosterid, 'Title': self.var_moviePostertitle, 'Year': self.var_moviePosteryear, 'Genre': self.var_moviePostergenre,
                'Runtime': self.var_moviePosterruntime, 'Rating': self.var_moviePosterrating, 'Date added': self.var_moviePosterdate, 'Director': self.var_moviePosterdirector,
                'Actors': self.var_moviePosteractors, 'Franchise': self.var_moviePosterfranchise }
        for i in range( 1, len(self.preferences_frame.winfo_children() ) ):
            if self.configparser['Movie Posters'][self.preferences_frame.winfo_children()[i]['text'] ] == "1":
                self.preferences_frame.winfo_children()[i].state(['!disabled','selected'])
                dict_[self.preferences_frame.winfo_children()[i]['text'] ].set(1)

    def write_preferences(self ):
        self.configparser['Movie Posters']['ID'] = str(self.var_moviePosterid.get())
        self.configparser['Movie Posters']['Title'] = str(self.var_moviePostertitle.get())
        self.configparser['Movie Posters']['Year'] = str(self.var_moviePosteryear.get())
        self.configparser['Movie Posters']['Genre'] = str(self.var_moviePostergenre.get())
        self.configparser['Movie Posters']['Runtime'] = str(self.var_moviePosterruntime.get())
        self.configparser['Movie Posters']['Rating'] = str(self.var_moviePosterrating.get())
        self.configparser['Movie Posters']['Date added'] = str(self.var_moviePosterdate.get())
        self.configparser['Movie Posters']['Director'] = str(self.var_moviePosterdirector.get())
        self.configparser['Movie Posters']['Actors'] = str(self.var_moviePosteractors.get())
        self.configparser['Movie Posters']['Franchise'] = str(self.var_moviePosterfranchise.get())
        with open('lib/configuration.ini', 'w') as configfile:
            self.configparser.write(configfile)
    
    def center(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))

    def destroy_app(self):
        self.configparser.read('lib/configuration.ini')
        if self.state() == 'zoomed':
            self.configparser['Options'][ 'maximized' ] = 'True'
        else:
            self.configparser['Options'][ 'maximized' ] = 'False'
        with open('lib/configuration.ini', 'w') as configfile:
                self.configparser.write(configfile)
        self.destroy()

if __name__ == "__main__":
    mainApp = Entertainment()
    mainApp.mainloop()