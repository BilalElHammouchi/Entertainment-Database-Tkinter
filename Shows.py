import datetime
from io import BytesIO
import json
import requests
from Abstract import Abstract, resource_path
import configparser
from PIL import ImageTk,Image
from tkinter import CENTER, INSERT, messagebox, ttk
from threading import Thread
import tkinter
import textwrap
from customtkinter import *


class Shows(Abstract):
    def __init__(self,root):
        super().__init__(root)
        self.sorted_dictionary = { "ID": 1, "Title": 0, "First_airdate": 0, "Last_airdate": 0, "genres": 0, "runtime": 0, "rating": 0, 
                "added_time": 0, "actors": 0, "creators": 0, "seasons": 0, 'episodes': 0, "status": 0 }
        if self.root.configparser['Options']['show_view'] == "List":
            self.button_menuView.configure( command = self.view )
        else:
            self.button_menuView.configure( command = self.posters )


    def main_image(self, width, height):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        theme = self.configparser['Options']['theme']
        if theme == "black" or theme == "equilux":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows black.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "blue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows blue.jpg") ).resize( (width,height) ) )
        elif theme == "alt" or theme == "classic" or theme == "default" or theme == "elegance" or theme == "scidblue" or theme == "scidgreen" \
            or theme == "scidgrey" or theme == "scidmint" or theme == "scidpink" or theme == "scidpurple" or theme == "scidsand":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows alt.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "clam":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows clam.jpg") ).resize( (width,height) ) )
        elif theme == "itft1":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows itft1.jpg") ).resize( (width,height) ) )
        elif theme == "keramik" or theme == "keramik_alt":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows keramik.jpg") ).resize( (width,height) ) )
        elif theme == "kroc":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows kroc.jpg") ).resize( (width,height) ) )
        elif theme == "winxpblue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows winxpblue.jpg") ).resize( (width,height) ) )
        else:
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best shows.jpg") ).resize( (width-2,height-2) ) )


    def view(self):
        super().view()
        self.root.configparser['Options'][ 'show_view' ] = 'List'
        with open('lib/configuration.ini', 'w') as configfile:
            self.root.configparser.write(configfile)
        self.combobox_search['values'] = ('ID', 'Title', 'First Air Date', 'Last Air Date', 'Genre', 'Runtime', 'Rating', 'Date added', 
                                            'Actor', 'Creator', 'Number of Seasons', 'Number of Episodes', 'Status' )
        self.combobox_search['state'] = "readonly"
        self.combobox_search.set("Title")
        self.view_tree.configure( column=("c1", "c2", "c3" , "c4" , "c5" , "c6" , "c7" , "c8" , "c9", "c10", "c11", "c12", "c13") )
        self.view_tree.heading("#1", text="ID", command = lambda: self.sort_tree('ID',False) )
        self.view_tree.column("#1", anchor= CENTER, width = 20 )
        self.view_tree.heading("#2", text="Title", command = lambda: self.sort_tree('Title',False) )
        self.view_tree.column("#2", anchor= CENTER, width = 250 )
        self.view_tree.heading("#3", text="First Air Date", command = lambda: self.sort_tree('First_airdate',False) )
        self.view_tree.column("#3", anchor= CENTER, width = 50 )
        self.view_tree.heading("#4", text="Last Air Date", command = lambda: self.sort_tree('Last_airdate',False) )
        self.view_tree.column("#4", anchor= CENTER, width = 50 )
        self.view_tree.heading("#5", text="Genre", command = lambda: self.sort_tree('genres',False) )
        self.view_tree.column("#5", anchor= CENTER, width = 200 )
        self.view_tree.heading("#6", text="Runtime", command = lambda: self.sort_tree('runtime',False) )
        self.view_tree.column("#6", anchor= CENTER, width = 60 )
        self.view_tree.heading("#7", text="Rating", command = lambda: self.sort_tree('rating',False) )
        self.view_tree.column("#7", anchor= CENTER, width = 45 )
        self.view_tree.heading("#8", text="Date added", command = lambda: self.sort_tree('added_time',False) )
        self.view_tree.column("#8", anchor= CENTER, width = 100 )
        self.view_tree.heading("#9", text= "Actors", command = lambda: self.sort_tree('actors',False) )
        self.view_tree.column("#9", anchor= CENTER, width = 50 ) 
        self.view_tree.heading("#10", text= "Creators", command = lambda: self.sort_tree('creators',False) )
        self.view_tree.column("#10", anchor= CENTER, width = 100 )
        self.view_tree.heading("#11", text= "Seasons", command = lambda: self.sort_tree('seasons',False) )
        self.view_tree.column("#11", anchor= CENTER, width = 50 )
        self.view_tree.heading("#12", text= "Episodes", command = lambda: self.sort_tree('episodes',False) )
        self.view_tree.column("#12", anchor= CENTER, width = 50 )
        self.view_tree.heading("#13", text= "Status", command = lambda: self.sort_tree('status',False) )
        self.view_tree.column("#13", anchor= CENTER, width = 50 )
        self.sort_tree(self.sorted_option, True)

    
    def sort_tree(self, option, start):   # method to sort treeview when clicking on columns)
        for key in self.sorted_dictionary.keys():   # Reset counter for all columns
            if key != option:
                self.sorted_dictionary[key] = 0
        if start and self.sorted_dictionary[option] == 0:
            self.sorted_dictionary[option] = 1
        elif start and self.sorted_dictionary[option] == 1:
            self.sorted_dictionary[option] = 0
        self.view_tree.delete(  *self.view_tree.get_children()  )
        sql_query = """
            SELECT shows.ID, shows.Title, shows.First_airdate, shows.Last_airdate, group_concat(DISTINCT genres.name) as genres,
                shows.runtime, shows.Rating, shows.added_time, group_concat(DISTINCT actors.name) as actors,
                group_concat(DISTINCT directors.name) as creators, shows.Seasons, shows.Episodes, 
                CASE shows.status 
                WHEN 0 THEN 'Ended'
                WHEN 1 THEN 'Ongoing'
                END AS status
                FROM shows 
                JOIN show_genres ON shows.ID=show_genres.show_id 
                JOIN genres ON show_genres.genre_id=genres.id
                JOIN show_castings ON show_castings.showid=shows.ID
                JOIN actors ON show_castings.actorid=actors.id
                JOIN show_creators ON show_creators.show_id=shows.ID
                JOIN directors ON show_creators.director_id=directors.id
                GROUP BY shows.Title
        """
        options = [ "ID", "Title", "First_airdate", "Last_airdate", "runtime", "rating", "added_time", "seasons", 'episodes', "status" ]
        for o in options:
            if option == o and self.sorted_dictionary[o] == 0:
                self.root.cur.execute( f"{sql_query} ORDER BY shows.{o}")
                self.sorted_dictionary[o] = 1
                self.sorted_option = o
                break
            elif option == o and self.sorted_dictionary[o] == 1:
                self.root.cur.execute( f"{sql_query} ORDER BY shows.{o} DESC")
                self.sorted_dictionary[o] = 0
                self.sorted_option = o
                break
        if option == "genres" and self.sorted_dictionary["genres"] == 0:
            self.root.cur.execute( f"{sql_query} ORDER BY genres")
            self.sorted_dictionary["genres"] = 1
            self.sorted_option = "genres"
        elif option == "genres" and self.sorted_dictionary["genres"] == 1:
            self.root.cur.execute( f"{sql_query} ORDER BY genres DESC")
            self.sorted_dictionary["genres"] = 0
            self.sorted_option = "genres"
        elif option == "actors" and self.sorted_dictionary["actors"] == 0:
            self.root.cur.execute( f"{sql_query} ORDER BY actors")
            self.sorted_dictionary["actors"] = 1
            self.sorted_option = "actors"
        elif option == "actors" and self.sorted_dictionary["actors"] == 1:
            self.root.cur.execute( f"{sql_query} ORDER BY actors DESC")
            self.sorted_dictionary["actors"] = 0
            self.sorted_option = "actors"
        elif option == "creators" and self.sorted_dictionary["creators"] == 0:
            self.root.cur.execute( f"{sql_query} ORDER BY creators")
            self.sorted_dictionary["creators"] = 1
            self.sorted_option = "creators"
        elif option == "creators" and self.sorted_dictionary["creators"] == 1:
            self.root.cur.execute( f"{sql_query} ORDER BY creators DESC")
            self.sorted_dictionary["creators"] = 0
            self.sorted_option = "creators"
        self.show_records = self.root.cur.fetchall()
        for i in range( 0, len(self.show_records) ):
            self.view_tree.insert("", END, values = self.show_records[i], iid=str(i) )


    def show_search(self, e):
        if not self.entry_enterSearch.get():
            messagebox.showerror("Error","Please provide a name before searching!")
            return
        response = requests.get( f"https://api.themoviedb.org/3/search/tv?api_key=8be65c3700e29a363aa7a71021169259&append_to_response=images&query={self.entry_enterSearch.get()}")
        response = json.loads( response.text )['results']
        self.root.img_tempImages.clear()
        self.tree_select.delete(*self.tree_select.get_children())
        for result in response:
            try:
                first_date = datetime.datetime.strptime( result['first_air_date'], "%Y-%m-%d" ).strftime("%B %d, %Y")
            except:
                first_date = 'TBD'
            release_date = f"{first_date}"
            description_result = result['overview']
            description = '\n'.join(textwrap.wrap(description_result, 150))
            self.tree_select.insert('', 'end', values= ( result['name'], release_date, description, result['id'] ) )
        for i in range(len(response)):
            Thread( target = self.show_searchPosters(response[i], i) ).start()


    def show_searchPosters(self, result,index ):
        image_response = requests.get( f"https://image.tmdb.org/t/p/w92{result['poster_path']}" )
        try:
            img = ImageTk.PhotoImage( Image.open(BytesIO(image_response.content)) )
        except:
            img = ImageTk.PhotoImage( Image.open( resource_path("lib/image-not-found.png") ).resize( (92,92) ) )
        self.root.img_tempImages.append(img)
        item_ = self.tree_select.get_children()[index]
        self.tree_select.item(item_, image = img)


    def ShowSelectOnDoubleClick(self, event, rating, franchise, editMode,primary_key,show_id):
        self.styleLabelEnter = ttk.Style()
        self.styleLabelEnter.configure( "Kim.TLabel", font = ("TkDefaultFont", 12))
        font = ("TkDefaultFont", 12 )
        if not show_id:
            self.show_id = self.tree_select.item( self.tree_select.selection()[0] )['values'][-1]
        else:
            self.show_id = show_id
        response = requests.get( f"https://api.themoviedb.org/3/tv/{self.show_id}?api_key=8be65c3700e29a363aa7a71021169259&append_to_response=credits&language=en-US" )
        show_details = json.loads( response.text )
        #print(f"{show_details = }")
        for child in self.root.winfo_children():
            child.pack_forget()
        self.frame_showEnterConfirm = ttk.Frame(self.root)
        self.frame_showEnterConfirm.pack( fill = 'both', expand = True )
        frame_buttons = ttk.Frame(self.frame_showEnterConfirm)
        frame_buttons.pack(side='bottom', fill='x', pady=10)
        for i in range(3):
            tkinter.Grid.columnconfigure(frame_buttons, i, weight = 1)
        self.image_response = requests.get( f"https://image.tmdb.org/t/p/w500{show_details['poster_path']}" )
        try:
            self.og_img = Image.open(BytesIO(self.image_response.content))
            self.img_to_save = self.og_img
            self.img = ImageTk.PhotoImage( self.img_to_save.resize( (500,750) ) )
        except:
            self.og_img = Image.open( resource_path("lib/image-not-found.png") ).resize( (500,750) )
            self.img_to_save = self.og_img
            self.img = ImageTk.PhotoImage( self.img_to_save )
        self.root.img_tempImages.append(self.img)
        frame_upper = ttk.Frame(self.frame_showEnterConfirm)
        frame_upper.pack(side='top', fill='both', expand=True)
        for i in range(12):
            tkinter.Grid.rowconfigure(frame_upper, i, weight = 1)
        self.label_showEnterPoster = ttk.Label(frame_upper, image = self.img )
        self.label_showEnterPoster.grid( row = 0, column = 0, rowspan = 12, sticky = "NSEW", padx=150 )
        label_title = ttk.Label(frame_upper, text = "Title", style = "Kim.TLabel", anchor='e' )
        label_title.grid( row = 0, column = 1, sticky = "E", padx = 10 )
        self.entry_title = ttk.Entry(frame_upper, font = font, width=30, justify='center' )
        self.entry_title.grid( row = 0, column = 2, padx = 10 )
        self.entry_title.insert(0, show_details['name'] )
        label_year = ttk.Label(frame_upper, text = "Years active", style = "Kim.TLabel" )
        label_year.grid( row = 1, column = 1, sticky = "E", padx = 10 )
        frm = ttk.Frame(frame_upper)
        frm.grid( row = 1, column = 2, padx = 10 )
        self.entry_yearstart = ttk.Entry(frm, font = font, width=10, justify='center')
        self.entry_yearstart.pack(side='left')
        self.entry_yearstart.insert(0, show_details['first_air_date'] )
        ttk.Label(frm, text='-', style = "Kim.TLabel").pack(side='left')
        self.entry_yearend = ttk.Entry(frm, font = font, width=10, justify='center')
        self.entry_yearend.pack(side='left')
        self.entry_yearend.insert(0, show_details['last_air_date'] )
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
        for genre in show_details['genres']:
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
        self.entry_minutes = ttk.Entry(frame_runtime, width=3, font = font, justify='center' )
        self.entry_minutes.pack( side = 'left' )
        if show_details['episode_run_time']:
            self.entry_minutes.insert(0, sum(show_details['episode_run_time'])//len(show_details['episode_run_time']) )
        label_minutes = ttk.Label(frame_runtime, text = "minute(s)", style = "Kim.TLabel" )
        label_minutes.pack( side = 'left' )
        label_creator = ttk.Label(frame_upper, text = "Creators", style = "Kim.TLabel" )
        label_creator.grid( row = 4, column = 1, sticky = "E", padx = 10 )
        frame_creator = ttk.Frame(frame_upper )
        frame_creator.grid( row = 4, column = 2, padx = (10,10) )
        scrollbar_creator = ttk.Scrollbar(frame_creator, orient = "vertical" )
        self.entry_creator = tkinter.Text(frame_creator, width = 20, height = 3, font = font, yscrollcommand = scrollbar_creator.set )
        scrollbar_creator.configure( command = self.entry_creator.yview )
        scrollbar_creator.pack( fill = 'both', side = 'right' )
        self.entry_creator.pack( fill = 'both', side = 'left' )
        creators = ""
        for creator in show_details['created_by']:
            creators += creator['name'] + "\n"
        self.entry_creator.insert(INSERT, creators)
        label_actor = ttk.Label(frame_upper, text = "Actors", style = "Kim.TLabel" )
        label_actor.grid( row = 5, column = 1, sticky = "E", padx = 10 )
        i = 0
        actors = ""
        credit = show_details["credits"]
        for actor in credit['cast']:
            actors += actor['name'] + "\n"
            i += 1
            if i == 10:
                break
        frame_actor = ttk.Frame(frame_upper )
        frame_actor.grid( row = 5, column = 2, padx = (10,10) )
        scrollbar_actor = ttk.Scrollbar(frame_actor, orient = "vertical" )
        self.entry_actor = tkinter.Text(frame_actor, width = 20, height = 4, font = font, yscrollcommand = scrollbar_actor.set )
        scrollbar_actor.configure( command = self.entry_actor.yview )
        self.entry_actor.pack( fill = 'both', side = 'left' )
        scrollbar_actor.pack( fill = 'both', side = 'right' )
        self.entry_actor.insert(INSERT, actors)
        label_seasons = ttk.Label(frame_upper, text = "Seasons", style = "Kim.TLabel" )
        label_seasons.grid( row = 6, column = 1, sticky = "E", padx = 10 )
        self.entry_seasons = ttk.Entry(frame_upper, font = font, justify='center', width=3 )
        self.entry_seasons.grid( row = 6, column = 2, padx = 10 )
        self.entry_seasons.insert(0,show_details['number_of_seasons'])
        label_episodes = ttk.Label(frame_upper, text = "Episodes", style = "Kim.TLabel" )
        label_episodes.grid( row = 7, column = 1, sticky = "E", padx = 10 )
        self.entry_episodes = ttk.Entry(frame_upper, font = font, justify='center', width=3 )
        self.entry_episodes.grid( row = 7, column = 2, padx = 10 )
        self.entry_episodes.insert(0,show_details['number_of_episodes'])
        
        ttk.Label(frame_upper, text = "Times Viewed", style = "Kim.TLabel" ).grid(row = 8, column = 1, sticky = "E", padx = 10 )
        self.entry_timesWatched = ttk.Entry(frame_upper, font = font, justify='center', width=3 )
        self.entry_timesWatched.grid( row = 8, column = 2, padx = 10 )
        self.root.cur.execute("SELECT times_viewed FROM shows WHERE tmd_id = ?", (show_details['id'],))
        result = self.root.cur.fetchone()
        if result:
            self.entry_timesWatched.insert(0, result[0]+1)
        else:
            self.entry_timesWatched.insert(0, '1')
        label_status = ttk.Label(frame_upper, text = "Status", style = "Kim.TLabel" )
        label_status.grid( row = 9, column = 1, sticky = "E", padx = 10 )
        if show_details['status'] == 'Ended':
            self.var_status = IntVar(value=0)
        else:
            self.var_status = IntVar(value=1)
        self.switch_status = CTkSwitch(frame_upper, variable=self.var_status, text='Ongoing', onvalue=1, offvalue=0, font=font )
        self.switch_status.grid( row = 9, column = 2, padx = 10 )
        self.label_ratingValue = ttk.Label(frame_upper, text = "2.5 Stars", style = "Kim.TLabel" )
        self.label_ratingValue.grid( row = 10, column = 2, padx = 10 )
        label_rating = ttk.Label(frame_upper, text = "Rating", style = "Kim.TLabel" )
        label_rating.grid( row = 11, column = 1, sticky = "E", padx = 10 )
        self.variable_rating = tkinter.DoubleVar()
        self.variable_rating.set(rating)
        self.slider_changed(None)
        scale_rating = ttk.Scale(frame_upper, from_= 0.0, to = 5.0, variable = self.variable_rating, command= self.slider_changed, length=200 )
        scale_rating.grid( row = 11, column = 2, padx = 10 )
        button_back = ttk.Button(frame_buttons, text = "Back", command = self.showEnterConfirm_ToShowEnter)
        button_back.grid( row = 0, column = 0 )
        button_reset = ttk.Button(frame_buttons, text = "Reset", command = self.showEnterConfirm_Reset )
        button_reset.grid( row = 0, column = 1 )
        self.button_confirm = ttk.Button(frame_buttons, text = "Confirm", command = lambda:self.showEnterConfirm(show_details) )
        self.button_confirm.grid( row = 0, column = 2 )
        """
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
        """


    def showEnterConfirm(self, show_details):
        if not self.entry_title.get():
            messagebox.showerror('Error', 'No title to the show given!')
            return
        self.root.cur.execute("SELECT tmd_id FROM shows")
        results = self.root.cur.fetchall()
        if any(show_details['id'] in sl for sl in results):
            self.root.cur.execute("""UPDATE shows SET Title = ?, First_airdate = ?, Last_airdate = ?, Runtime = ?, Rating = ?,
                                Seasons = ?, Episodes = ?, Status = ?, times_viewed = ? WHERE tmd_id = ?""", 
                                (self.entry_title.get(), self.entry_yearstart.get(), self.entry_yearend.get(), self.entry_minutes.get(), 
                                float(self.label_ratingValue['text'].split(' ')[0]), int(self.entry_seasons.get()), int(self.entry_episodes.get()), 
                                self.var_status.get(), self.entry_timesWatched.get(), show_details['id']) )
        else:
            self.root.cur.execute("""INSERT INTO shows (Title, First_airdate, Last_airdate, Runtime, Rating, added_time, Seasons, Episodes, Status, tmd_id, times_viewed)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                                (self.entry_title.get(), self.entry_yearstart.get(), self.entry_yearend.get(), self.entry_minutes.get(), 
                                float(self.label_ratingValue['text'].split(' ')[0]), datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 
                                int(self.entry_seasons.get()), int(self.entry_episodes.get()), self.var_status.get(), show_details['id'], self.entry_timesWatched.get()) )
            show_id = self.root.cur.lastrowid
            for genre in self.listbox_genre.curselection():
                self.root.cur.execute("INSERT INTO show_genres(show_id, genre_id) VALUES (?, ?) ", (show_id,genre) )

            self.root.cur.execute("""SELECT name FROM actors""")
            results = self.root.cur.fetchall()
            db_actors = [actor for subactor in results for actor in subactor]
            actors = [item for item in self.entry_actor.get("1.0", "end-1c").split('\n') if item]
            for actor in actors:
                if actor not in db_actors:
                    self.root.cur.execute("""INSERT INTO actors(name) VALUES (?)""", (actor,))
            formatted_actors = "('" + "', '".join(actors) + "')"
            self.root.cur.execute(f"SELECT id FROM actors WHERE name IN {formatted_actors}")
            results = self.root.cur.fetchall()
            actors_id = [actor for subactor in results for actor in subactor]
            for actor_id in actors_id:
                self.root.cur.execute("INSERT INTO show_castings(showid, actorid) VALUES(?,?)", (show_id, actor_id))

            self.root.cur.execute("""SELECT name FROM directors""")
            results = self.root.cur.fetchall()
            db_creators = [creator for subcreator in results for creator in subcreator]
            creators = [item for item in self.entry_creator.get("1.0", "end-1c").split('\n') if item]
            for creator in creators:
                if creator not in db_creators:
                    self.root.cur.execute("""INSERT INTO directors(name) VALUES (?)""", (creator,))
            formatted_creators = "('" + "', '".join(creators) + "')"
            self.root.cur.execute(f"SELECT id FROM directors WHERE name IN {formatted_creators}")
            results = self.root.cur.fetchall()
            creators_id = [creator for subcreator in results for creator in subcreator]
            for creator_id in creators_id:
                self.root.cur.execute("INSERT INTO show_creators(show_id, director_id) VALUES(?,?)", (show_id, creator_id))
        self.root.con.commit()
        self.showEnterConfirm_ToShowEnter()
    

    def showEnterConfirm_Reset(self):
        self.entry_title.delete(0,END)
        self.entry_yearstart.delete(0,END)
        self.entry_yearend.delete(0,END)
        self.listbox_genre.selection_clear(0, END)
        self.entry_minutes.delete(0,END)
        self.entry_creator.delete('1.0', END)
        self.entry_actor.delete('1.0', END)
        self.entry_seasons.delete(0,END)
        self.entry_episodes.delete(0,END)
        self.var_status.set(0)
        self.variable_rating.set(2.5)
        self.label_ratingValue.configure(text='2.5 Stars')


    def showEnterConfirm_ToShowEnter(self):
        self.frame_showEnterConfirm.pack_forget()
        self.frame_enter.pack( expand = True, fill = "both")


    def enter(self):
        super().enter()
        self.button_enterSearch.configure( command = lambda: Thread( target = lambda: self.show_search(None) ).start() )
        self.tree_select.bind("<Double-1>", lambda e, rating = 2.5, franchise = "": self.ShowSelectOnDoubleClick(e,rating,franchise,False,None,None) )
        self.button_enterSelect.configure( command = lambda: self.ShowSelectOnDoubleClick(None,2.5,"",False,None,None) )
        self.button_enterSelect.grid( row = 0, column = 1, pady = 10 )
        self.root.bind('<Return>', lambda e = None: Thread( target = lambda: self.show_search(e) ).start() )