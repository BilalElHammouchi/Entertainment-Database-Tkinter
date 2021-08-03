from tkinter import *
import tkinter.messagebox
from tkinter import ttk
import re
from PIL import ImageTk,Image
from datetime import datetime
import os.path
import os
import configparser
from AddImages import Find_MovieImage
from AddImages import send_image_name

def Back_Movies( frame1, frame2, frame3 ):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack()

def Movies(Frame_MovieMain , root, Images_List, mydb,mycursor):
    Frame_MovieMain.pack_forget()
    EnterMovieFrameFunction(root, Images_List, Frame_MovieMain, mydb,mycursor)

def Reset_All(  Entry_MovieDir, Entry_MovieRunM, Entry_MovieRunH, listbox, frame_EnterMovie, Entry_MovieFran,
                Frame_MovieRun, Entry_MovieYear, Entry_MovieName, scrollbar_tree):
    scrollbar_tree.pack_forget()
    listbox.pack_forget()
    scrollbar_tree.pack(side = RIGHT, fill = BOTH )
    listbox.pack( side = LEFT, fill = BOTH )
    scrollbar_tree.config(command = listbox.yview)
    listbox.selection_clear(0,END)    
    Entry_MovieFran.grid_forget()
    Entry_MovieFran = Entry ( frame_EnterMovie , justify = 'center' )
    Entry_MovieFran.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieDir.grid_forget()
    Entry_MovieDir = Entry ( frame_EnterMovie , justify = 'center' )
    Entry_MovieDir.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieRunM.grid_forget()
    Entry_MovieRunM = Entry( Frame_MovieRun , width = 3 , justify = 'center' )
    Entry_MovieRunM.grid( row = 0 , column = 2 )
    Entry_MovieRunH.grid_forget()
    Entry_MovieRunH = Entry( Frame_MovieRun , width = 3 , justify = 'center' )
    Entry_MovieRunH.grid( row = 0 , column = 0 )
    Entry_MovieYear.grid_forget()
    Entry_MovieYear = Entry( frame_EnterMovie , justify = 'center')
    Entry_MovieYear.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieName.grid_forget()
    Entry_MovieName = Entry( frame_EnterMovie , justify = 'center')
    Entry_MovieName.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

def Count(Entry_MovieRunH, Entry_MovieRunM):
    hours = Entry_MovieRunH.get()
    if hours.isdigit():
        hours = int( hours )
    else:
        hours = 0
    minutes = Entry_MovieRunM.get()
    if minutes.isdigit():
        minutes = int( minutes )
    else:
        minutes = 0
    if minutes == 0 and hours == 0:
        return None
    else:
        total = hours * 60 + minutes
        return total

def List_Stop( listbox, scrollbar ):
    Choices = listbox.curselection()
    Choices2 = []
    for i in range( len(Choices) ) :
        Choices2.append( Choices[i] + 1 )
    
    if len(Choices) > 3:
        scrollbar.pack_forget()
        listbox.pack_forget()
        scrollbar.pack(side = RIGHT, fill = BOTH )
        listbox.pack( side = LEFT, fill = BOTH )
        scrollbar.config(command = listbox.yview)
        listbox.selection_clear(0,END)  
        tkinter.messagebox.showerror("Error", "Only 3 genres or under")
        return False

    return Choices2

config = configparser.ConfigParser()
config.read('configuration.ini')
if os.path.isfile("configuration.ini"):
    if config['DEFAULT']['darkmode'] == 'True':
        dark_modeMovies = True
    else:
        dark_modeMovies = False
else:
    config['DEFAULT'] = {'Darkmode': 'True' ,  'Viewmode': 'List'   }
    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)

movie_image = []
def Movie_Main( root, Frame_Entertainment, Frame_MovieView, Frame_EnterMovie, Images_List, mycursor, mydb ):
    global Frame_MovieMain, dark_modeMovies, CanvasMovies, MainMoviesPicture, MainMoviesPictureDark,EnterMovie_Button,ViewMovie_Button,BackMovie_Button
    Frame_MovieMain = Frame( root )
    if movie_image == []:
        movie_image.append(Frame_Entertainment)
    Frame_Entertainment.pack_forget()
    Frame_MovieView.pack_forget()
    Frame_EnterMovie.pack_forget()
    MainMoviesPicture = Images_List[4]
    MainMoviesPictureDark = Images_List[7]
    Frame_MovieMain.pack()
    CanvasMovies = Canvas( Frame_MovieMain , width = 960 , height = 480 )
    if dark_modeMovies is False:
        CanvasMovies.create_image( 480, 240, image = Images_List[4] )
        CanvasMovies.configure( bd =  0)
    else:
        CanvasMovies.create_image( 480, 240, image = Images_List[7] ) 
        CanvasMovies.configure( bd =  0)
    CanvasMovies.grid( row = 0 , columnspan = 3 )
    EnterMovie_Button = Button( Frame_MovieMain , text ='Enter' , font=('Orelega One','16') , command=lambda:Movies(Frame_MovieMain, root, Images_List, mydb,mycursor) )
    EnterMovie_Button.grid( row = 1 , column = 0 , pady = 10 )
    ViewMovie_Button = Button( Frame_MovieMain , text ='View' , font=('Orelega One','16') , command = lambda: Movie_View(Frame_MovieMain, mycursor,root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, None) )
    ViewMovie_Button.grid( row = 1 , column = 1 , pady = 10 )
    BackMovie_Button = Button( Frame_MovieMain , text ='Back' , font=('Orelega One','16') , command =lambda: Back_Movies(Frame_EnterMovie,Frame_MovieMain,Frame_Entertainment) )
    BackMovie_Button.grid( row = 1 , column = 2 , pady = 10 )
    dark_modeMovies = not dark_modeMovies
    darkMovies_function()
    

switch_Id=switch_Name=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Director=switch_Franchise=Edit_Or_Click=0

sql_For_Images = Frame_Tree_For_Images = Frame_MovieView_For_Images = None
list_image_view = []
def Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected ):
    global tree, option2, dark_modeMovies,Frame_MovieView,Button_BackMovieMain,Button_EditMovieMain,Button_DeleteMovieMain,Frame_tree,style,scrollbar_tree
    Frame_MovieMain.pack_forget()
    Frame_MovieView.pack()
    global switch_Id,switch_Name,switch_Year,switch_Genre,switch_Run,switch_Rating,switch_Date,switch_Director,switch_Franchise,Edit_Or_Click,sql_For_Images
    global Frame_Tree_For_Images, Frame_MovieView_For_Images, list_image_view, Image_View
    Frame_MovieView_For_Images = Frame_MovieView
    option2 = Option_Selected
    if Option_Selected == 'ID' or Option_Selected is None:
        if Option_Selected is None:
            switch_Id = 0
        if switch_Id % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_id DESC"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_id"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Id += 1
            switch_Name=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Name':
        if switch_Name % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_name"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_name DESC" 
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Name += 1
            switch_Id=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Year':
        if switch_Year % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , years.year_actual , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movies.movie_franchise, movies.movie_year FROM movies LEFT JOIN years ON movies.movie_year = years.year_id ORDER BY years.year_actual DESC"
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , years.year_actual , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movies.movie_franchise, movies.movie_year FROM movies LEFT JOIN years ON movies.movie_year = years.year_id ORDER BY years.year_actual"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Year += 1
            switch_Id=switch_Name=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Genre':
        if Edit_Or_Click == 0:
            switch_Genre += 1
            switch_Id=switch_Name=switch_Year=switch_Run=switch_Rating=switch_Date=switch_Director=switch_Franchise=0
        if switch_Genre % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_genre1 DESC, movie_genre2 DESC, movie_genre3 DESC"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_genre1, movie_genre2, movie_genre3"
        mycursor.execute(sql)
    elif Option_Selected == 'Runtime':
        if switch_Run % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_runtime DESC"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_runtime"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Run += 1
            switch_Id=switch_Name=switch_Year=switch_Genre=switch_Rating=switch_Date=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Rating':
        if switch_Rating % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_rating DESC"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_rating"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Rating += 1
            switch_Id=switch_Name=switch_Year=switch_Genre=switch_Run=switch_Date=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Date added':
        if switch_Date % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_added_time DESC"
        else:
            sql = "SELECT * FROM movies ORDER BY movie_added_time"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Date += 1
            switch_Id=switch_Name=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Director=switch_Franchise=0
    elif Option_Selected == 'Director':
        if switch_Director % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, directors.director_name, movies.movie_franchise, movies.movie_director FROM movies LEFT JOIN directors ON movies.movie_director = directors.director_id ORDER BY directors.director_name"
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, directors.director_name, movies.movie_franchise, movies.movie_director FROM movies LEFT JOIN directors ON movies.movie_director = directors.director_id ORDER BY directors.director_name DESC"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Director += 1
            switch_Id=switch_Name=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Franchise=0
    elif Option_Selected == 'Franchise':
        if switch_Franchise % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movie_franchises.mf_name, movies.movie_franchise FROM movies LEFT JOIN movie_franchises ON movies.movie_franchise = movie_franchises.mf_id ORDER BY movie_franchises.mf_name"
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movie_franchises.mf_name, movies.movie_franchise FROM movies LEFT JOIN movie_franchises ON movies.movie_franchise = movie_franchises.mf_id ORDER BY movie_franchises.mf_name DESC"
        mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_Franchise += 1
            switch_Id=switch_Name=switch_Year=switch_Genre=switch_Run=switch_Rating=switch_Date=switch_Director=0

    movie_result = mycursor.fetchall()
    Frame_tree = Frame( Frame_MovieView )
    Frame_tree.grid( row = 0 , columnspan =	5 )
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Treeview', rowheight=20)
    tree = ttk.Treeview( Frame_tree , column=("c1", "c2", "c3" , "c4" , "c5" , "c6" , "c7" , "c8" , "c9"
             ) , show='headings' , yscrollcommand = TRUE , height = 20 , )
    scrollbar_tree = Scrollbar( Frame_tree )
    scrollbar_tree.pack(side = RIGHT, fill = BOTH )
    tree.config(yscrollcommand = scrollbar_tree.set)
    scrollbar_tree.config(command = tree.yview)
    all_movies = []
    for movie in movie_result:
        movie_actual = []
        movie_actual.append(movie[0])
        movie_actual.append(movie[1])
        if Option_Selected == 'Year':
            movie_actual.append(movie[2])
        else:
            movie_result_year = movie[2]
            sql2 = "SELECT year_actual FROM years WHERE year_id = %s"
            adr = ( movie_result_year , )
            mycursor.execute(sql2, adr)
            movie_result_year = mycursor.fetchall()
            if movie_result_year == []:
                movie_actual.append( None )
            else:
                movie_actual.append( movie_result_year[0][0] )
        movie_result_genre1 = movie[3]
        movie_result_genre2 = movie[4]
        movie_result_genre3 = movie[5]
        sql2 = "SELECT genre_name FROM genres WHERE genre_id = %s OR genre_id = %s OR genre_id = %s"
        adr = ( movie_result_genre1 , movie_result_genre2 , movie_result_genre3 )
        mycursor.execute(sql2, adr)
        movie_result_genre = mycursor.fetchall()
        genre_actual = ''
        for i in range(len(movie_result_genre)):
            if i == 0:
                genre_actual += movie_result_genre[0][0]
            else:
                genre_actual += '/' + movie_result_genre[i][0]
        movie_actual.append( genre_actual )
        movie_result_runtime = movie[6]
        if movie_result_runtime is not None:
            movie_result_hours = movie_result_runtime // 60
            movie_result_minutes = movie_result_runtime - movie_result_hours*60
            movie_result_runtime_actual = str(movie_result_hours) + 'h ' + str(movie_result_minutes) + 'm'
        else:
            movie_result_runtime_actual = None
        movie_actual.append( movie_result_runtime_actual )
        movie_actual.append( movie[7] )
        movie_actual.append( movie[8] )
        if Option_Selected == 'Director':
            movie_actual.append( movie[9] )
        else:
            movie_result_director = movie[9]
            sql2 = "SELECT director_name FROM directors WHERE director_id = %s"
            adr = ( movie_result_director , )
            mycursor.execute(sql2, adr)
            movie_result_director = mycursor.fetchall()
            movie_actual.append( movie_result_director[0][0] )
        if Option_Selected == 'Franchise':
            movie_actual.append( movie[10] )
        else:
            movie_result_franchise = movie[10]
            sql2 = "SELECT mf_name FROM movie_franchises WHERE mf_id = %s"
            adr = ( movie_result_franchise , )
            mycursor.execute(sql2, adr)
            movie_result_franchise = mycursor.fetchall()
            movie_actual.append( movie_result_franchise[0][0] )
        all_movies.append( movie_actual )
    for i in range(len(all_movies)):
        tree.insert("", END, values= all_movies[i], iid=str(i) )
    if list_image_view == []:
        list_image_view.append(Frame_tree)
        list_image_view.append(Frame_MovieView)
        list_image_view.append(sql)
        list_image_view.append(tree)
    tree.pack(  side = LEFT, fill = BOTH )
    Image_View = False
    Button_BackMovieMain = Button( Frame_MovieView , text = 'Back' , command =lambda:Movie_Main(root,Frame_Entertainment,Frame_MovieView,Frame_EnterMovie,Images_List,mycursor,mydb) , font=('Orelega One','16') )
    Button_BackMovieMain.grid( row = 2 , column = 2 , pady = 10 )
    Button_EditMovieMain = Button( Frame_MovieView , text = 'Edit' , command =lambda: Edit_Movie(Frame_MovieMain,Frame_MovieView, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected) , font=('Orelega One','16') )
    Button_EditMovieMain.grid( row = 2 , column = 0 , columnspan = 2)
    Button_DeleteMovieMain = Button( Frame_MovieView , text = 'Delete' , command =lambda:Delete_Movie(Frame_MovieMain,Frame_MovieView,mycursor,root,Frame_Entertainment,Frame_EnterMovie,Images_List,mydb,Option_Selected) , font=('Orelega One','16') )
    Button_DeleteMovieMain.grid( row = 2 , column = 3 , columnspan = 2)
    tree.column("#1", anchor= CENTER , width = 50 )
    tree.heading("#1", text="ID" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'ID' ) )
    tree.column("#2", anchor= CENTER , width = 300 )
    tree.heading("#2", text="Name" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Name' ) )
    tree.column("#3", anchor= CENTER , width = 50 )
    tree.heading("#3", text="Year" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Year' ) )
    tree.column("#4", anchor= CENTER)
    tree.heading("#4", text="Genre" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Genre' ) )
    tree.column("#5", anchor= CENTER , width = 70)
    tree.heading("#5", text="Runtime" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Runtime' ) )
    tree.column("#6", anchor= CENTER , width = 50)
    tree.heading("#6", text="Rating" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Rating' ) )
    tree.column("#7", anchor= CENTER , width = 150)
    tree.heading("#7", text="Date added" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Date added' ) )
    tree.column("#8", anchor= CENTER)
    tree.heading("#8", text="Director" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Director' ) )
    tree.column("#9", anchor= CENTER)
    tree.heading("#9", text="Franchise" , command = lambda : Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, 'Franchise' ) )
    dark_modeMovies = not dark_modeMovies
    darkMovies_function()

def Delete_Movie( Frame_MovieMain,Frame_MovieView, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected ):
    global tree
    for number in tree.selection():
        temp = tree.item( number )
        tree.delete( number )
        sql = "DELETE FROM movies WHERE movie_id = %s "
        add = ( temp['values'][0] , )
        mycursor.execute(sql , add )
        mydb.commit()
    Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, None )

def disable_event(root):
    global EditMovies_Window
    EditMovies_Window.withdraw()
    root.deiconify()

def MakeEditWindow(root):
    global Frame_EditMovie,EditMovies_Window
    EditMovies_Window = Toplevel( )
    EditMovies_Window.protocol( "WM_DELETE_WINDOW" , lambda:disable_event(root) )
    EditMovies_Window.title( "Edit Your Movie" )
    EditMovies_Window.withdraw()
    Frame_EditMovie = Frame( EditMovies_Window )

def Edit_Movie( Frame_MovieMain,Frame_MovieView, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected ):
    MakeEditWindow(root)
    root.withdraw()
    global Frame_EditMovie, Entry_MovieNameEdit, Entry_MovieYearEdit, listboxEdit, Entry_MovieRunHEdit, Entry_MovieRunMEdit, Entry_MovieDirEdit
    global Entry_MovieFranEdit,Frame_MovieRunEdit, Label_EnterMovieNameEdit, Label_EnterMovieYearEdit, Label_EnterMovieGenreEdit, Label_EnterMovieRunEdit
    global LabelHoursEdit, LabelMinutesEdit, Label_EnterMovieDirEdit, Label_EnterMovieRatingEdit,Label_EnterMovieFranEdit,frame_MovieButtonsEdit
    global Confirm_ButtonEdit,Reset_ButtonEdit,Frame_StarsEdit,Star1Left_ButtonEdit,Star2Left_ButtonEdit,Star3Left_ButtonEdit,Star4Left_ButtonEdit
    global Star5Left_ButtonEdit,Star1Right_ButtonEdit,Star2Right_ButtonEdit,Star3Right_ButtonEdit,Star4Right_ButtonEdit,Star5Right_ButtonEdit
    Label_EnterMovieNameEdit = Label(Frame_EditMovie , text='Enter movie name: ' , font=('Orelega One','16') )
    Label_EnterMovieNameEdit.grid( row  = 0 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieNameEdit = Entry( Frame_EditMovie )
    Entry_MovieNameEdit.configure( justify="center" )
    Entry_MovieNameEdit.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieYearEdit = Label(Frame_EditMovie , text='Enter year: ' , font=('Orelega One','16') )
    Label_EnterMovieYearEdit.grid( row  = 1 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieYearEdit = Entry( Frame_EditMovie, justify="center" )
    Entry_MovieYearEdit.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieGenreEdit = Label(Frame_EditMovie , text='Enter genre: ' , font=('Orelega One','16') )
    Label_EnterMovieGenreEdit.grid( row  = 2 , column = 0 , padx = 10 , pady = 10 )

    Frame_ListboxEdit = Frame(Frame_EditMovie)
    Frame_ListboxEdit.grid( row = 2 , column = 1)
    scrollbarEdit = Scrollbar(Frame_ListboxEdit)
    scrollbarEdit.pack(side = RIGHT, fill = BOTH )
    listboxEdit = Listbox(Frame_ListboxEdit , selectmode=MULTIPLE , selectbackground='gray' , height=10  , font=('Orelega One','12') )
    listboxEdit.config(yscrollcommand = scrollbarEdit.set)
    scrollbarEdit.config(command = listboxEdit.yview)
    listboxEdit.insert(1,"Action")  
    listboxEdit.insert(2, "Adventure")  
    listboxEdit.insert(3, "Animation")  
    listboxEdit.insert(4, "Biographical")
    listboxEdit.insert(5, "Comedy")
    listboxEdit.insert(6,"Crime Film")  
    listboxEdit.insert(7, "Disaster")  
    listboxEdit.insert(8, "Documentary")  
    listboxEdit.insert(9, "Drama")
    listboxEdit.insert(10, "Fantasy")  
    listboxEdit.insert(11,"Horror")  
    listboxEdit.insert(12, "Indie")  
    listboxEdit.insert(13, "Martial Arts")  
    listboxEdit.insert(14, "Musical")
    listboxEdit.insert(15, "Mystery")  
    listboxEdit.insert(16, "Noir")  
    listboxEdit.insert(17, "Romance")  
    listboxEdit.insert(18, "Science")  
    listboxEdit.insert(19, "Science Fiction")
    listboxEdit.insert(20, "Short")  
    listboxEdit.insert(21,"Sports")  
    listboxEdit.insert(22, "Superhero")  
    listboxEdit.insert(23, "Thriller")  
    listboxEdit.insert(24, "War")
    listboxEdit.insert(25, "Western")
    listboxEdit.pack( side = LEFT, fill = BOTH )     


    Label_EnterMovieRunEdit = Label(Frame_EditMovie , text='Enter run-time: ' , font=('Orelega One','16') )
    Label_EnterMovieRunEdit.grid( row  = 3 , column = 0 , padx = 10 , pady = 10 )

    ###### Frame_MovieRun

    Frame_MovieRunEdit = Frame( Frame_EditMovie )
    Frame_MovieRunEdit.grid( row = 3 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieRunHEdit = Entry( Frame_MovieRunEdit , width = 3, justify="center")
    Entry_MovieRunHEdit.grid( row = 0 , column = 0 )
    LabelHoursEdit = Label( Frame_MovieRunEdit, text = 'hour(s)' , font=('Orelega One','16') )
    LabelHoursEdit.grid( row = 0 , column = 1 )
    Entry_MovieRunMEdit = Entry( Frame_MovieRunEdit , width = 3, justify="center")
    Entry_MovieRunMEdit.grid( row = 0 , column = 2 )
    LabelMinutesEdit = Label( Frame_MovieRunEdit, text = 'minute(s)' , font=('Orelega One','16') )
    LabelMinutesEdit.grid( row = 0 , column = 3 )

    #######

    Label_EnterMovieDirEdit = Label(Frame_EditMovie , text='Enter Director: ' , font=('Orelega One','16') )
    Label_EnterMovieDirEdit.grid( row = 4 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieDirEdit = Entry ( Frame_EditMovie, justify="center" )
    Entry_MovieDirEdit.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieRatingEdit = Label(Frame_EditMovie , text='Choose rating: ' , font=('Orelega One','16') )
    Label_EnterMovieRatingEdit.grid( row  = 5 , column = 0 , padx = 10 , pady = 10 )

    Label_EnterMovieFranEdit = Label(Frame_EditMovie , text='Enter movie franchise: ' , font=('Orelega One','16') )
    Label_EnterMovieFranEdit.grid( row = 6 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieFranEdit = Entry ( Frame_EditMovie, justify="center" )
    Entry_MovieFranEdit.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )

    # Frame_Stars

    Frame_StarsEdit = Frame( Frame_EditMovie )
    Frame_StarsEdit.grid( row = 5 , column = 1 )

    Star1Left_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[5] , bd = 0 , command = lambda: Star_AmountEdit(0.5) , activebackground = '#F9FFB5' )
    Star1Left_ButtonEdit.grid( row = 0 ,  column = 0 )
    Star1Right_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[6] , bd = 0 , command = lambda: Star_AmountEdit(1) , activebackground = '#F9FFB5')
    Star1Right_ButtonEdit.grid( row = 0 ,  column = 1 )

    Star2Left_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[5] , bd = 0 , command = lambda: Star_AmountEdit(1.5)  , activebackground = '#F9FFB5')
    Star2Left_ButtonEdit.grid( row = 0 , column = 2 )
    Star2Right_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[6] , bd = 0 , command = lambda: Star_AmountEdit(2)  , activebackground = '#F9FFB5')
    Star2Right_ButtonEdit.grid( row = 0 , column = 3 )

    Star3Left_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[5] , bd = 0 , command = lambda: Star_AmountEdit(2.5) , activebackground = '#F9FFB5' )
    Star3Left_ButtonEdit.grid( row = 0 , column = 4 )
    Star3Right_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[6] , bd = 0 , command = lambda: Star_AmountEdit(3) , activebackground = '#F9FFB5' )
    Star3Right_ButtonEdit.grid( row = 0 , column = 5 )

    Star4Left_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[5] , bd = 0 , command = lambda: Star_AmountEdit(3.5) , activebackground = '#F9FFB5' )
    Star4Left_ButtonEdit.grid( row = 0 , column = 6 )
    Star4Right_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[6] , bd = 0 , command = lambda: Star_AmountEdit(4) , activebackground = '#F9FFB5' )
    Star4Right_ButtonEdit.grid( row = 0 , column = 7 )

    Star5Left_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[5] , bd = 0 , command = lambda: Star_AmountEdit(4.5) , activebackground = '#F9FFB5' )
    Star5Left_ButtonEdit.grid( row = 0 , column = 8 )
    Star5Right_ButtonEdit = Button(Frame_StarsEdit , image = Images_List[6] , bd = 0 , command = lambda: Star_AmountEdit(5) , activebackground = '#F9FFB5' )
    Star5Right_ButtonEdit.grid( row = 0 , column = 9 )

    # Frame_EnterMovie Buttons

    frame_MovieButtonsEdit = Frame( Frame_EditMovie )
    frame_MovieButtonsEdit.grid( row = 7 , columnspan = 2)
    Add_MoviePosterButtonEdit = Button(frame_MovieButtonsEdit, text='Add Poster', font=('Orelega One','16') , command=lambda:Find_MovieImage(Entry_MovieNameEdit) )
    Add_MoviePosterButtonEdit.grid( row = 0 , columnspan = 2, pady = 30)
    Confirm_ButtonEdit = Button(frame_MovieButtonsEdit , text = 'Confirm' , font=('Orelega One','16')  )
    Confirm_ButtonEdit.configure( command=lambda:ConfirmMovies_Edit( Frame_MovieMain,Frame_MovieView, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected ))
    Confirm_ButtonEdit.grid( row = 1 , column = 0 , padx = 30 , pady = 30 )
    Reset_ButtonEdit = Button(frame_MovieButtonsEdit , text = 'Reset' , font=('Orelega One','16'),command=Reset_AllEdit )
    Reset_ButtonEdit.grid( row = 1 , column = 1 , padx = 30 , pady = 30 )
    global EditMovies_Window
    Frame_ListboxEdit = Frame( Frame_EditMovie )
    Frame_ListboxEdit.grid( row = 2 , column  = 1 )
    EditMovies_Window.deiconify()
    Frame_EditMovie.pack()
    for number in tree.selection():
        temp = tree.item( number )
        Entry_MovieNameEdit.insert(0 , temp['values'][1] )
        Entry_MovieYearEdit.insert(0 , temp['values'][2] )
        Choices_Edit = temp['values'][3]
        Choices_Edit = Choices_Edit.split('/')
        for i in range( 0 , 25 ):
            if listboxEdit.get( i ) in Choices_Edit:
                listboxEdit.selection_set( first = i )
        test = temp['values'][4]
        test2 = re.findall(r'\d+' , test )
        if len(test2) >= 1:
            Entry_MovieRunHEdit.insert(0 , test2[0] )
            Entry_MovieRunMEdit.insert(0 , test2[1] )
        Entry_MovieDirEdit.insert(0 , temp['values'][7] )
        Entry_MovieFranEdit.insert(0 , temp['values'][8] )
    global dark_modeMovies
    dark_modeMovies = not dark_modeMovies
    darkMovies_function()

def ConfirmMovies_Edit( Frame_MovieMain,Frame_MovieView, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected ):
    global tree,Entry_MovieNameEdit, Entry_MovieYearEdit, listboxEdit, Entry_MovieRunHEdit, Entry_MovieRunMEdit, Entry_MovieDirEdit, Entry_MovieFranEdit
    Movie_IdEdit = tree.selection()[0]
    Movie_IdEdit = tree.item( Movie_IdEdit )
    Movie_IdEdit = Movie_IdEdit['values'][0]
    global EditMovies_Window
    global Entry_MovieNameEdit
    global Entry_MovieYearEdit
    Movie_NameEdit = Entry_MovieNameEdit.get()
    if Movie_NameEdit == '':
        tkinter.messagebox.showerror("Error", "You must include at least the name of the movie!")
        return 0
    global Entry_MovieYearEdit
    Movie_YearEdit = Entry_MovieYearEdit.get()
    if Movie_YearEdit.isdigit():
        Movie_YearEdit = int( Movie_YearEdit )
    else:
        Movie_YearEdit = None
    List_StopEdit( Frame_EnterMovie )
    global Movie_Genre1Edit, Movie_Genre2Edit, Movie_Genre3Edit, Choices2Edit
    Movie_Genre1Edit = Movie_Genre2Edit = Movie_Genre3Edit = None
    
    if len(Choices2Edit) == 1:
        Movie_Genre1Edit = Choices2Edit[0] 
    elif len( Choices2Edit ) == 2:
        Movie_Genre1Edit = Choices2Edit[0] 
        Movie_Genre2Edit = Choices2Edit[1]
    elif len(Choices2Edit ) == 3:
        Movie_Genre1Edit = Choices2Edit[0] 
        Movie_Genre2Edit = Choices2Edit[1]
        Movie_Genre3Edit = Choices2Edit[2]
    
    global Movie_RunEdit, Movie_StarsEdit, star_numberEdit, Image_View, Movie_DirEdit
    Movie_RunEdit = CountEdit()
    Movie_DirEdit = Entry_MovieDirEdit.get()
    if star_numberEdit == None:
        sql = "SELECT movie_rating FROM movies WHERE movie_id = %s"
        adr = ( Movie_IdEdit , )
        mycursor.execute(sql, adr)
        Movie_StarsEdit = mycursor.fetchall()
        Movie_StarsEdit = Movie_StarsEdit[0][0]
    else:
        Movie_StarsEdit = star_numberEdit
    global Movie_FranEdit
    Movie_FranEdit = Entry_MovieFranEdit.get()

    sql = "SELECT director_id FROM directors WHERE director_name = %s"
    adr = ( Movie_DirEdit , )
    mycursor.execute(sql, adr)
    dir_resultEdit = mycursor.fetchall()

    if len( dir_resultEdit ) == 0:
        sql = "INSERT INTO directors (director_name) VALUES (%s)"
        val = ( Movie_DirEdit , )
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT director_id FROM directors WHERE director_name = %s"
        adr = ( Movie_DirEdit , )
        mycursor.execute(sql, adr)
        dir_resultEdit = mycursor.fetchall()

    sql = "SELECT mf_id FROM movie_franchises WHERE mf_name = %s"
    adr = ( Movie_FranEdit , )
    mycursor.execute(sql, adr)
    fran_resultEdit = mycursor.fetchall()

    if len( fran_resultEdit ) == 0:
        sql = "INSERT INTO movie_franchises (mf_name) VALUES (%s)"
        val = ( Movie_FranEdit , )
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT mf_id FROM movie_franchises WHERE mf_name = %s"
        adr = ( Movie_FranEdit , )
        mycursor.execute(sql, adr)
        fran_resultEdit = mycursor.fetchall()


    if Movie_YearEdit is not None:
        sql = "SELECT year_id FROM years WHERE year_actual = %s"
        adr = ( Movie_YearEdit , )
        mycursor.execute(sql, adr)
        year_resultEdit = mycursor.fetchall()

        if len( year_resultEdit ) == 0:
            sql = "INSERT INTO years (year_actual) VALUES (%s)"
            val = ( Movie_YearEdit , )
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "SELECT year_id FROM years WHERE year_actual = %s"
            adr = ( Movie_YearEdit , )
            mycursor.execute(sql, adr)
            year_resultEdit = mycursor.fetchall()

        Movie_YearEdit = year_resultEdit[0][0]
    Movie_DirEdit = dir_resultEdit[0][0]
    Movie_FranEdit = fran_resultEdit[0][0]    
    image_db_name = send_image_name()
    
    sql = "UPDATE movies SET movie_name = %s, movie_year = %s, movie_genre1 = %s, movie_genre2 = %s, movie_genre3 = %s, movie_runtime = %s, movie_rating = %s, movie_director = %s, movie_franchise = %s WHERE movie_id = %s"
    val = ( Movie_NameEdit , Movie_YearEdit , Movie_Genre1Edit , Movie_Genre2Edit , Movie_Genre3Edit , Movie_RunEdit , Movie_StarsEdit , Movie_DirEdit , Movie_FranEdit  ,  Movie_IdEdit )
    mycursor.execute(sql, val)
    if image_db_name is not None:
        try:
            os.rename('Images/Movies/Native/' + image_db_name, 'Images/Movies/Native/' + str(Movie_IdEdit) + '.jpg' )
        except:
            os.remove( 'Images/Movies/Native/' + str(Movie_IdEdit) + '.jpg' )
            os.rename('Images/Movies/Native/' + image_db_name, 'Images/Movies/Native/' + str(Movie_IdEdit) + '.jpg' )
    mydb.commit()
    EditMovies_Window.withdraw()
    global option2, Edit_Or_Click
    Edit_Or_Click = 1
    if Image_View == False:
        Movie_View( Frame_MovieMain, mycursor, root, Frame_Entertainment, Frame_EnterMovie, Images_List, mydb, Option_Selected )
    else:
        changeto_images( mycursor, root, Images_List, mydb )
    root.deiconify()

def CountEdit():
    global hoursEdit
    hoursEdit = Entry_MovieRunHEdit.get()
    if hoursEdit.isdigit():
        hoursEdit = int( hoursEdit )
    else:
        hoursEdit = 0
    global minutesEdit
    minutesEdit = Entry_MovieRunMEdit.get()
    if minutesEdit.isdigit():
        minutesEdit = int( minutesEdit )
    else:
        minutesEdit = 0
    if minutesEdit == 0 and hoursEdit == 0:
        return None
    else:
        total = hoursEdit * 60 + minutesEdit
        return total

def Reset_AllEdit():
    global Entry_MovieDirEdit,star_numberEdit,Entry_MovieRunMEdit,Entry_MovieRunHEdit,listboxEdit,Frame_ListboxEdit,scrollbarEdit,dark_modeMovies
    listboxEdit.grid_forget()
    Frame_ListboxEdit = Frame(Frame_EditMovie)
    Frame_ListboxEdit.grid( row = 2 , column = 1)
    scrollbarEdit = Scrollbar(Frame_ListboxEdit)
    scrollbarEdit.pack(side = RIGHT, fill = BOTH )
    listboxEdit = Listbox(Frame_ListboxEdit , selectmode=MULTIPLE , selectbackground='gray' , height=10  , font=('Orelega One','12') )
    listboxEdit.config(yscrollcommand = scrollbarEdit.set)
    scrollbarEdit.config(command = listboxEdit.yview)
    listboxEdit.insert(1,"Action")  
    listboxEdit.insert(2, "Adventure")  
    listboxEdit.insert(3, "Animation")  
    listboxEdit.insert(4, "Biographical")
    listboxEdit.insert(5, "Comedy")
    listboxEdit.insert(6,"Crime Film")  
    listboxEdit.insert(7, "Disaster")  
    listboxEdit.insert(8, "Documentary")  
    listboxEdit.insert(9, "Drama")
    listboxEdit.insert(10, "Fantasy")  
    listboxEdit.insert(11,"Horror")  
    listboxEdit.insert(12, "Indie")  
    listboxEdit.insert(13, "Martial Arts")  
    listboxEdit.insert(14, "Musical")
    listboxEdit.insert(15, "Mystery")  
    listboxEdit.insert(16, "Noir")  
    listboxEdit.insert(17, "Romance")  
    listboxEdit.insert(18, "Science")  
    listboxEdit.insert(19, "Science Fiction")
    listboxEdit.insert(20, "Short")  
    listboxEdit.insert(21,"Sports")  
    listboxEdit.insert(22, "Superhero")  
    listboxEdit.insert(23, "Thriller")  
    listboxEdit.insert(24, "War")
    listboxEdit.insert(25, "Western")
    listboxEdit.pack( side = LEFT, fill = BOTH )
    global Entry_MovieYearEdit,Entry_MovieNameEdit,Entry_MovieFranEdit,Frame_MovieRunEdit
    Entry_MovieFranEdit.grid_forget()
    Entry_MovieFranEdit = Entry ( Frame_EditMovie,justify="center" )
    Entry_MovieFranEdit.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieDirEdit.grid_forget()
    Entry_MovieDirEdit = Entry ( Frame_EditMovie,justify="center" )
    Entry_MovieDirEdit.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )
    star_numberEdit = None
    Entry_MovieRunMEdit.grid_forget()
    Entry_MovieRunMEdit = Entry( Frame_MovieRunEdit , width = 3,justify="center")
    Entry_MovieRunMEdit.grid( row = 0 , column = 2 )
    Entry_MovieRunHEdit.grid_forget()
    Entry_MovieRunHEdit = Entry( Frame_MovieRunEdit , width = 3,justify="center")
    Entry_MovieRunHEdit.grid( row = 0 , column = 0 )
    Entry_MovieYearEdit.grid_forget()
    Entry_MovieYearEdit = Entry( Frame_EditMovie,justify="center" )
    Entry_MovieYearEdit.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieNameEdit.grid_forget()
    Entry_MovieNameEdit = Entry( Frame_EditMovie )
    Entry_MovieNameEdit.configure( justify="center" )
    Entry_MovieNameEdit.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )
    dark_modeMovies = not dark_modeMovies
    darkMovies_function()

def List_StopEdit( Frame_EnterMovie ):
    global ChoicesEdit
    global listboxEdit
    ChoicesEdit = listboxEdit.curselection()
    global Choices2Edit
    Choices2Edit = []
    for i in range( len(ChoicesEdit) ) :
        Choices2Edit.append( ChoicesEdit[i] + 1 )
    
    if len(ChoicesEdit) > 3:
        listboxEdit.grid_forget()
        listboxEdit = Listbox(Frame_EnterMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
        listboxEdit.insert(1, "Action")  
        listboxEdit.insert(2, "Adventure")  
        listboxEdit.insert(3, "Animation")  
        listboxEdit.insert(4, "Biographical")
        listboxEdit.insert(5, "Comedy")
        listboxEdit.insert(6,"Crime Film")  
        listboxEdit.insert(7, "Disaster")  
        listboxEdit.insert(8, "Documentary")  
        listboxEdit.insert(9, "Drama")
        listboxEdit.insert(10, "Fantasy")  
        listboxEdit.insert(11,"Horror")  
        listboxEdit.insert(12, "Indie")  
        listboxEdit.insert(13, "Martial Arts")  
        listboxEdit.insert(14, "Musical")
        listboxEdit.insert(15, "Mystery")  
        listboxEdit.insert(16, "Noir")  
        listboxEdit.insert(17, "Romance")  
        listboxEdit.insert(18, "Science")  
        listboxEdit.insert(19, "Science Fiction")
        listboxEdit.insert(20, "Short")  
        listboxEdit.insert(21,"Sports")  
        listboxEdit.insert(22, "Superhero")  
        listboxEdit.insert(23, "Thriller")  
        listboxEdit.insert(24, "War")
        listboxEdit.insert(25, "Western")    
        listboxEdit.grid( row = 2 , column = 1 )
        tkinter.messagebox.showerror("Error", "Only 3 genres or under")
        return False

    return True

star_number = star_numberEdit = None
def Star_Amount( number ):
    global star_number
    star_number = None
    if number is not None:
        star_number = number

def Star_AmountEdit( number ):
    global star_numberEdit
    star_numberEdit = None
    if number is not None:
        star_numberEdit = number

def MakeMovieFrames(root):
    global Frame_EnterMovie, Frame_MovieView
    Frame_EnterMovie = Frame( root )
    Frame_MovieView = Frame( root )
    return Frame_EnterMovie, Frame_MovieView 

def EnterMovieFrameFunction(root, Images_List, Frame_MovieMain, mydb,mycursor):
    global Entry_MovieName, Entry_MovieYear, listbox, scrollbar, Entry_MovieRunH, Entry_MovieRunM, Entry_MovieDir, Entry_MovieFran, Frame_Listbox, Frame_MovieRun
    Frame_EnterMovie = MakeMovieFrames(root)[0]
    global Label_EnterMovieName, Label_EnterMovieYear,Label_EnterMovieGenre,Label_EnterMovieRun,Star1Right_Button,Star2Left_Button,frame_MovieButtons
    global LabelHours,LabelMinutes,Label_EnterMovieDir,Label_EnterMovieRating, Label_EnterMovieFran,Frame_Stars,Star1Left_Button,Confirm_Button,Back_Button
    global Star2Right_Button,Star3Left_Button,Star3Right_Button,Star4Left_Button,Star4Right_Button,Star5Left_Button,Star5Right_Button,Reset_Button, dark_modeMovies
    global Add_MoviePosterButton
    Label_EnterMovieName = Label(Frame_EnterMovie , text='Enter movie name: ' , font=('Orelega One','16') )
    Label_EnterMovieName.grid( row  = 0 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieName = Entry( Frame_EnterMovie )
    Entry_MovieName.configure( justify="center" )
    Entry_MovieName.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieYear = Label(Frame_EnterMovie , text='Enter year: ' , font=('Orelega One','16') )
    Label_EnterMovieYear.grid( row  = 1 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieYear = Entry( Frame_EnterMovie )
    Entry_MovieYear.configure( justify="center" )
    Entry_MovieYear.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieGenre = Label(Frame_EnterMovie , text='Enter genre: ' , font=('Orelega One','16') )
    Label_EnterMovieGenre.grid( row  = 2 , column = 0 , padx = 10 , pady = 10 )

    #Frame_Listbox
    Frame_Listbox = Frame(Frame_EnterMovie)
    Frame_Listbox.grid( row = 2 , column = 1)

    scrollbar = Scrollbar(Frame_Listbox)
    scrollbar.pack(side = RIGHT, fill = BOTH )
    listbox = Listbox(Frame_Listbox , selectmode=MULTIPLE , selectbackground='gray' , height=10  , font=('Orelega One','12') )
    listbox.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listbox.yview)
    listbox.insert(1,"Action")  
    listbox.insert(2, "Adventure")  
    listbox.insert(3, "Animation")  
    listbox.insert(4, "Biographical")
    listbox.insert(5, "Comedy")
    listbox.insert(6,"Crime Film")  
    listbox.insert(7, "Disaster")  
    listbox.insert(8, "Documentary")  
    listbox.insert(9, "Drama")
    listbox.insert(10, "Fantasy")  
    listbox.insert(11,"Horror")  
    listbox.insert(12, "Indie")  
    listbox.insert(13, "Martial Arts")  
    listbox.insert(14, "Musical")
    listbox.insert(15, "Mystery")  
    listbox.insert(16, "Noir")  
    listbox.insert(17, "Romance")  
    listbox.insert(18, "Science")  
    listbox.insert(19, "Science Fiction")
    listbox.insert(20, "Short")  
    listbox.insert(21,"Sports")  
    listbox.insert(22, "Superhero")  
    listbox.insert(23, "Thriller")  
    listbox.insert(24, "War")
    listbox.insert(25, "Western")     
    listbox.pack( side = LEFT, fill = BOTH )
    Label_EnterMovieRun = Label(Frame_EnterMovie , text='Enter run-time: ' , font=('Orelega One','16') )
    Label_EnterMovieRun.grid( row  = 3 , column = 0 , padx = 10 , pady = 10 )

    ###### Frame_MovieRun

    Frame_MovieRun = Frame( Frame_EnterMovie )
    Frame_MovieRun.grid( row = 3 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieRunH = Entry( Frame_MovieRun , width = 3 , justify = 'center')
    Entry_MovieRunH.grid( row = 0 , column = 0 )
    LabelHours = Label( Frame_MovieRun, text = 'hour(s)' , font=('Orelega One','16') )
    LabelHours.grid( row = 0 , column = 1 )
    Entry_MovieRunM = Entry( Frame_MovieRun , width = 3 , justify = 'center' )
    Entry_MovieRunM.grid( row = 0 , column = 2 )
    LabelMinutes = Label( Frame_MovieRun, text = 'minute(s)' , font=('Orelega One','16') )
    LabelMinutes.grid( row = 0 , column = 3 )

    #######

    Label_EnterMovieDir = Label(Frame_EnterMovie , text='Enter Director: ' , font=('Orelega One','16') )
    Label_EnterMovieDir.grid( row = 4 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieDir = Entry ( Frame_EnterMovie , justify = 'center' )
    Entry_MovieDir.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )

    Label_EnterMovieRating = Label(Frame_EnterMovie , text='Choose rating: ' , font=('Orelega One','16') )
    Label_EnterMovieRating.grid( row  = 5 , column = 0 , padx = 10 , pady = 10 )

    # Frame_Stars

    Frame_Stars = Frame( Frame_EnterMovie )
    Frame_Stars.grid( row = 5 , column = 1 )

    Star1Left_Button = Button(Frame_Stars , image = Images_List[5] , bd = 0 , command = lambda: Star_Amount(0.5) , activebackground = '#F9FFB5' )
    Star1Left_Button.grid( row = 0 ,  column = 0 )
    Star1Right_Button = Button(Frame_Stars , image = Images_List[6] , bd = 0 , command = lambda: Star_Amount(1) , activebackground = '#F9FFB5')
    Star1Right_Button.grid( row = 0 ,  column = 1 )

    Star2Left_Button = Button(Frame_Stars , image = Images_List[5] , bd = 0 , command = lambda: Star_Amount(1.5)  , activebackground = '#F9FFB5')
    Star2Left_Button.grid( row = 0 , column = 2 )
    Star2Right_Button = Button(Frame_Stars , image = Images_List[6] , bd = 0 , command = lambda: Star_Amount(2)  , activebackground = '#F9FFB5')
    Star2Right_Button.grid( row = 0 , column = 3 )

    Star3Left_Button = Button(Frame_Stars , image = Images_List[5] , bd = 0 , command = lambda: Star_Amount(2.5) , activebackground = '#F9FFB5' )
    Star3Left_Button.grid( row = 0 , column = 4 )
    Star3Right_Button = Button(Frame_Stars , image = Images_List[6] , bd = 0 , command = lambda: Star_Amount(3) , activebackground = '#F9FFB5' )
    Star3Right_Button.grid( row = 0 , column = 5 )

    Star4Left_Button = Button(Frame_Stars , image = Images_List[5] , bd = 0 , command = lambda: Star_Amount(3.5) , activebackground = '#F9FFB5' )
    Star4Left_Button.grid( row = 0 , column = 6 )
    Star4Right_Button = Button(Frame_Stars , image = Images_List[6] , bd = 0 , command = lambda: Star_Amount(4) , activebackground = '#F9FFB5' )
    Star4Right_Button.grid( row = 0 , column = 7 )

    Star5Left_Button = Button(Frame_Stars , image = Images_List[5] , bd = 0 , command = lambda: Star_Amount(4.5) , activebackground = '#F9FFB5' )
    Star5Left_Button.grid( row = 0 , column = 8 )
    Star5Right_Button = Button(Frame_Stars , image = Images_List[6] , bd = 0 , command = lambda: Star_Amount(5) , activebackground = '#F9FFB5' )
    Star5Right_Button.grid( row = 0 , column = 9 )

    Label_EnterMovieFran = Label(Frame_EnterMovie , text='Enter movie franchise: ' , font=('Orelega One','16') )
    Label_EnterMovieFran.grid( row = 6 , column = 0 , padx = 10 , pady = 10 )
    Entry_MovieFran = Entry ( Frame_EnterMovie , justify = 'center' )
    Entry_MovieFran.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )

    # Frame_EnterMovie Buttons
    frame_MovieButtons = Frame( Frame_EnterMovie )
    frame_MovieButtons.grid( row = 7 , columnspan = 2)
    Add_MoviePosterButton = Button(frame_MovieButtons, text='Add Poster', font=('Orelega One','16') , command=lambda:Find_MovieImage(Entry_MovieName) )
    Add_MoviePosterButton.grid( row = 0 , column = 1 , pady = 30)

    Confirm_Button = Button(frame_MovieButtons , text = 'Confirm' , font=('Orelega One','16') , command=lambda: Work_Movies( mydb,mycursor,Frame_EnterMovie) )
    Confirm_Button.grid( row = 1 , column = 0 , padx = 30 , pady = 10 )
    Reset_Button = Button(frame_MovieButtons , text = 'Reset' , font=('Orelega One','16') , command=lambda:Reset_All(    Entry_MovieDir, Entry_MovieRunM, Entry_MovieRunH, listbox, Frame_EnterMovie, Entry_MovieFran,
                                                                                                                                Frame_MovieRun, Entry_MovieYear, Entry_MovieName, scrollbar) )
    Reset_Button.grid( row = 1 , column = 1 , padx = 30 , pady = 10 )
    Back_Button = Button(frame_MovieButtons , text = 'Back' , font=('Orelega One','16'), command=lambda:Back_Movies(Frame_EnterMovie,Frame_EnterMovie,Frame_MovieMain) )
    Back_Button.grid( row = 1 , column = 2 , padx = 30 , pady = 10)
    dark_modeMovies = not dark_modeMovies
    darkMovies_function()
    Frame_EnterMovie.pack()

def Work_Movies( mydb,mycursor,frame_EnterMovie):
    global Entry_MovieName, Entry_MovieYear, listbox, scrollbar, Entry_MovieRunH, Entry_MovieRunM, Entry_MovieDir, Entry_MovieFran, Frame_Listbox, Frame_MovieRun
    Movie_Name = Entry_MovieName.get()
    if Movie_Name == '':
        tkinter.messagebox.showerror("Error", "You must include at least the name of the movie!")
        return 0
    Movie_Year = Entry_MovieYear.get()
    if Movie_Year.isdigit():
        Movie_Year = int( Movie_Year )
    else:
        Movie_Year = None
    Choices2 = List_Stop( listbox, scrollbar )
    if Choices2 is False:
        return 0
    Movie_Genre1 = Movie_Genre2 = Movie_Genre3 = None
    #print(Choices2)
    
    if len(Choices2) == 1:
        Movie_Genre1 = Choices2[0] 
    elif len( Choices2 ) == 2:
        Movie_Genre1 = Choices2[0] 
        Movie_Genre2 = Choices2[1]
    elif len(Choices2 ) == 3:
        Movie_Genre1 = Choices2[0] 
        Movie_Genre2 = Choices2[1]
        Movie_Genre3 = Choices2[2]
    Movie_Run = Count(Entry_MovieRunH, Entry_MovieRunM)
    Movie_Dir = Entry_MovieDir.get()
    global star_number
    Movie_Stars = star_number
    Movie_Fran = Entry_MovieFran.get()
    Movie_added = datetime.now()
    Movie_added = Movie_added.strftime("%x") + ' ' +  Movie_added.strftime("%X")

    sql = "SELECT director_id FROM directors WHERE director_name = %s"
    adr = ( Movie_Dir , )
    mycursor.execute(sql, adr)
    dir_result = mycursor.fetchall()

    if len( dir_result ) == 0:
        sql = "INSERT INTO directors (director_name) VALUES (%s)"
        val = ( Movie_Dir , )
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT director_id FROM directors WHERE director_name = %s"
        adr = ( Movie_Dir , )
        mycursor.execute(sql, adr)
        dir_result = mycursor.fetchall()

    sql = "SELECT mf_id FROM movie_franchises WHERE mf_name = %s"
    adr = ( Movie_Fran , )
    mycursor.execute(sql, adr)
    fran_result = mycursor.fetchall()

    if len( fran_result ) == 0:
        sql = "INSERT INTO movie_franchises (mf_name) VALUES (%s)"
        val = ( Movie_Fran , )
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "SELECT mf_id FROM movie_franchises WHERE mf_name = %s"
        adr = ( Movie_Fran , )
        mycursor.execute(sql, adr)
        fran_result = mycursor.fetchall()


    if Movie_Year is not None:
        sql = "SELECT year_id FROM years WHERE year_actual = %s"
        adr = ( Movie_Year , )
        mycursor.execute(sql, adr)
        year_result = mycursor.fetchall()

        if len( year_result ) == 0:
            sql = "INSERT INTO years (year_actual) VALUES (%s)"
            val = ( Movie_Year , )
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "SELECT year_id FROM years WHERE year_actual = %s"
            adr = ( Movie_Year , )
            mycursor.execute(sql, adr)
            year_result = mycursor.fetchall()

        Movie_Year = year_result[0][0]
    Movie_Dir = dir_result[0][0]
    Movie_Fran = fran_result[0][0]    

    image_db_name = send_image_name()
    sql = "INSERT INTO movies (movie_name, movie_year, movie_genre1 , movie_genre2, movie_genre3, movie_runtime, movie_rating, movie_director, movie_franchise, movie_added_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ( Movie_Name , Movie_Year , Movie_Genre1 , Movie_Genre2 , Movie_Genre3 , Movie_Run , Movie_Stars , Movie_Dir , Movie_Fran ,Movie_added )
    mycursor.execute(sql, val)
    
    mydb.commit()
    if image_db_name is not None:
        os.rename('Images/Movies/Native/' + image_db_name, 'Images/Movies/Native/' + str(mycursor.lastrowid) + '.jpg' )
    Reset_All(   Entry_MovieDir, Entry_MovieRunM, Entry_MovieRunH, listbox, frame_EnterMovie, Entry_MovieFran,
                        Frame_MovieRun, Entry_MovieYear, Entry_MovieName, scrollbar)

images = []
buttons = []
Image_View = False
def _on_mouse_wheel(event):
    global Images_Canvas
    Images_Canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

def select_image( row ):
    list_image_view[3].selection_set(str(row))

def changeto_images( mycursor, root, Images_List, mydb ):
    global Frame_Tree_For_Images, list_image_view, Image_View, images, buttons, Images_Canvas, option2, Frame_Entertainment
    list_image_view[0].grid_forget()
    Frame_Changeview = Frame(list_image_view[1] )
    Images_Canvas = Canvas( Frame_Changeview , width= 1625, height=902)
    Frame_Canvas = Frame(Images_Canvas)
    Frame_Changeview.grid( row = 0, columnspan= 5)
    Images_Canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    Images_Canvas.pack(side = LEFT, fill = BOTH, expand = 1 )
    Images_Scrollbar = Scrollbar(Frame_Changeview, orient = VERTICAL, command=Images_Canvas.yview)
    Images_Scrollbar.pack(side = LEFT, fill = Y)
    Images_Canvas.configure( yscrollcommand= Images_Scrollbar.set )
    Images_Canvas.bind('<Configure>' , lambda e: Images_Canvas.configure(scrollregion= Images_Canvas.bbox("all") ) )
    Images_Canvas.create_window( (0,0), window = Frame_Canvas, anchor = "nw" )
    mycursor.execute(list_image_view[2])
    movie_result = mycursor.fetchall()
    i = j = k = 0
    images = []
    buttons = []
    Image_View = True
    for movie in movie_result:
        try:
            filename = Image.open("Images/Movies/Optimized/" + str(movie[0]) + ".jpg" )
        except:
            try:
                filename = Image.open("Images/Movies/Native/" + str(movie[0]) + ".jpg" )
                filename.save("Images/Movies/Optimized/" + str(movie[0]) + ".jpg" , quality=95 )
                filename = Image.open("Images/Movies/Optimized/" + str(movie[0]) + ".jpg" )
            except:
                filename = Image.open("Images/image-not-found.png" )
            filename = filename.resize( (200,300) , Image.ANTIALIAS )  
        filename = ImageTk.PhotoImage( filename )
        images.append(filename)
        image_button = Button(Frame_Canvas, image = images[i+j*8], bd = 0, command=lambda k = k:select_image(k) )
        image_button.grid( row = j , column = i )
        buttons.append(image_button)
        i += 1
        k += 1
        if i == 8:
            j += 1
            i = 0

def darkMovies_function( ):
    global dark_modeMovies, Label_EnterMovieName,Entry_MovieName,Label_EnterMovieYear,Frame_MovieMain,CanvasMovies
    global Entry_MovieYear,Label_EnterMovieGenre,listbox,Label_EnterMovieRun,Frame_MovieRun,LabelHours,LabelMinutes,Label_EnterMovieDir
    global Label_EnterMovieRating,Label_EnterMovieFran,Frame_Stars,Star1Left_Button,Star1Right_Button,Star2Left_Button,Star2Right_Button
    global Star3Left_Button,Star3Right_Button,Star4Left_Button,Star4Right_Button,Star5Left_Button,Star5Right_Button,frame_MovieButtons
    global Confirm_Button,Reset_Button,Back_Button,EnterMovie_Button,ViewMovie_Button,BackMovie_Button,Frame_MovieView,tree, scrollbar_tree
    global Frame_EditMovie, Entry_MovieNameEdit, Entry_MovieYearEdit, listboxEdit, Entry_MovieRunHEdit, Entry_MovieRunMEdit, Entry_MovieDirEdit
    global Entry_MovieFranEdit,Frame_MovieRunEdit, Label_EnterMovieNameEdit, Label_EnterMovieYearEdit, Label_EnterMovieGenreEdit, Label_EnterMovieRunEdit
    global LabelHoursEdit, Label_EnterMovieDirEdit, Label_EnterMovieRatingEdit,Label_EnterMovieFranEdit,frame_MovieButtonsEdit
    global Confirm_ButtonEdit,Reset_ButtonEdit,Frame_StarsEdit, Star1Left_ButtonEdit,Star2Left_ButtonEdit,Star3Left_ButtonEdit,Star4Left_ButtonEdit
    global Star5Left_ButtonEdit,Star1Right_ButtonEdit,Star2Right_ButtonEdit,Star3Right_ButtonEdit,Star4Right_ButtonEdit,Star5Right_ButtonEdit,Add_MoviePosterButton
    if dark_modeMovies is False:
        try:
            Frame_EnterMovie.configure( bg= '#1F1B24' )
        except:
            pass
        try:
            Frame_MovieMain.configure( bg= '#1F1B24' )
            CanvasMovies.create_image( 480, 240, image = MainMoviesPictureDark )
            CanvasMovies.configure( bg= '#1F1B24' )
            EnterMovie_Button.configure( bg= '#1F1B24' , fg ='light grey')
            ViewMovie_Button.configure( bg= '#1F1B24' , fg ='light grey')
            BackMovie_Button.configure( bg= '#1F1B24' , fg ='light grey')
        except:
            pass
        try:
            Frame_MovieView.configure( bg= '#1F1B24' )
            Button_BackMovieMain.configure( bg= '#1F1B24' , fg ='light grey')
            Button_EditMovieMain.configure( bg= '#1F1B24' , fg ='light grey')
            Button_DeleteMovieMain.configure( bg= '#1F1B24' , fg ='light grey')
            style.configure("Treeview", foreground ='light gray', background = "dark gray" , fieldbackground = "#1F1B24" )
            style.configure("Treeview.Heading", background="#1F1B24" , foreground="light grey", activebackground = "#C054FF" )
            style.map('Treeview',background = [('selected' , '#C054FF')] )
            Frame_tree.configure( bg= '#1F1B24')
        except:
            pass
        try:
            Label_EnterMovieName.configure( bg= '#1F1B24' , fg='light grey')
            Entry_MovieName.configure( bg='#F0F0F0' , fg='black' , justify="center" )
            Label_EnterMovieYear.configure( bg= '#1F1B24' , fg='light grey')
            Entry_MovieYear.configure( bg='#F0F0F0' , fg='black' , justify="center" )
            Label_EnterMovieGenre.configure( bg= '#1F1B24' , fg='light grey')
            listbox.configure( bg = '#1F1B24', fg='light grey', selectbackground = '#c054ff')
            Label_EnterMovieRun.configure( bg= '#1F1B24' , fg='light grey')
            Frame_MovieRun.configure( bg = '#1F1B24' )
            LabelHours.configure( bg= '#1F1B24' , fg='light grey')
            LabelMinutes.configure( bg= '#1F1B24' , fg='light grey')
            Label_EnterMovieDir.configure( bg= '#1F1B24' , fg='light grey')
            Label_EnterMovieRating.configure( bg= '#1F1B24' , fg='light grey')
            Label_EnterMovieFran.configure( bg= '#1F1B24' , fg='light grey')
            Frame_Stars.configure( bg= '#1F1B24')
            Star1Left_Button.configure( bg = '#1F1B24' )
            Star1Right_Button.configure( bg = '#1F1B24' )
            Star2Left_Button.configure( bg = '#1F1B24' )
            Star2Right_Button.configure( bg = '#1F1B24' )
            Star3Left_Button.configure( bg = '#1F1B24' )
            Star3Right_Button.configure( bg = '#1F1B24' )
            Star4Left_Button.configure( bg = '#1F1B24' )
            Star4Right_Button.configure( bg = '#1F1B24' )
            Star5Left_Button.configure( bg = '#1F1B24' )
            Star5Right_Button.configure( bg = '#1F1B24' )
            frame_MovieButtons.configure( bg= '#1F1B24')
            Add_MoviePosterButton.configure( bg= '#1F1B24' , fg ='light grey')
            Confirm_Button.configure( bg= '#1F1B24' , fg ='light grey')
            Reset_Button.configure( bg= '#1F1B24' , fg ='light grey')
            Back_Button.configure( bg= '#1F1B24' , fg ='light grey')
        except:
            pass
        try:
            Frame_EditMovie.configure( bg= '#1F1B24')
            Label_EnterMovieNameEdit.configure( bg= '#1F1B24' , fg ='light grey' )
            Label_EnterMovieYearEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Label_EnterMovieGenreEdit.configure( bg= '#1F1B24' , fg ='light grey')
            listboxEdit.configure( bg = '#1F1B24', fg='light grey', selectbackground = '#c054ff')
            Label_EnterMovieRunEdit.configure( bg= '#1F1B24' , fg ='light grey')
            LabelHoursEdit.configure( bg= '#1F1B24' , fg ='light grey')
            LabelMinutesEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Label_EnterMovieDirEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Label_EnterMovieRatingEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Label_EnterMovieFranEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Frame_MovieRunEdit.configure( bg= '#1F1B24')
            Frame_StarsEdit.configure( bg= '#1F1B24')
            Star1Left_ButtonEdit.configure( bg= '#1F1B24')
            Star2Left_ButtonEdit.configure( bg= '#1F1B24')
            Star3Left_ButtonEdit.configure( bg= '#1F1B24')
            Star4Left_ButtonEdit.configure( bg= '#1F1B24')
            Star5Left_ButtonEdit.configure( bg= '#1F1B24')
            Star1Right_ButtonEdit.configure( bg= '#1F1B24')
            Star2Right_ButtonEdit.configure( bg= '#1F1B24')
            Star3Right_ButtonEdit.configure( bg= '#1F1B24')
            Star4Right_ButtonEdit.configure( bg= '#1F1B24')
            Star5Right_ButtonEdit.configure( bg= '#1F1B24')
            frame_MovieButtonsEdit.configure( bg= '#1F1B24')
            Confirm_ButtonEdit.configure( bg= '#1F1B24' , fg ='light grey')
            Reset_ButtonEdit.configure( bg= '#1F1B24' , fg ='light grey')
        except:
            pass
        dark_modeMovies = True
    else:
        try:
            Frame_EnterMovie.configure( bg= '#F0F0F0' )
        except:
            pass
        try:
            Frame_MovieMain.configure( bg= '#F0F0F0' )
            CanvasMovies.create_image( 480, 240, image = MainMoviesPicture )
            CanvasMovies.configure( bg= '#F0F0F0' )
            EnterMovie_Button.configure( bg= '#F0F0F0' , fg='black' )
            ViewMovie_Button.configure( bg= '#F0F0F0' , fg='black' )
            BackMovie_Button.configure( bg= '#F0F0F0' , fg='black' )
        except:
            pass
        try:
            Frame_MovieView.configure( bg= '#F0F0F0' )
            Button_BackMovieMain.configure( bg= '#F0F0F0' , fg='black' )
            Button_EditMovieMain.configure( bg= '#F0F0F0' , fg='black' )
            Button_DeleteMovieMain.configure( bg= '#F0F0F0' , fg='black' )
            style.configure("Treeview", foreground ='black', background = "white" , fieldbackground = "#F0F0F0" )
            style.configure("Treeview.Heading", background="#F0F0F0" , foreground="black" )
            style.map('Treeview',background = [('selected' , 'blue')] )
            Frame_tree.configure( bg= '#F0F0F0' )
        except:
            pass
        try:
            Label_EnterMovieName.configure( bg= '#F0F0F0' , fg='black')
            Entry_MovieName.configure( bg='white' , fg='black' , justify="center" )
            Label_EnterMovieYear.configure( bg= '#F0F0F0' , fg='black')
            Entry_MovieYear.configure(  bg='white' , fg='black' , justify="center" )
            Label_EnterMovieGenre.configure( bg= '#F0F0F0' , fg='black')
            listbox.configure( bg = 'white', fg='black', selectbackground = 'grey')
            Label_EnterMovieRun.configure( bg= '#F0F0F0' , fg='black')
            Frame_MovieRun.configure( bg = '#F0F0F0' )
            LabelHours.configure( bg= '#F0F0F0' , fg='black')
            LabelMinutes.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieDir.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieRating.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieFran.configure( bg= '#F0F0F0' , fg='black' )
            Frame_Stars.configure( bg= '#F0F0F0')
            Star1Left_Button.configure( bg= '#F0F0F0')
            Star1Right_Button.configure( bg= '#F0F0F0')
            Star2Left_Button.configure( bg= '#F0F0F0')
            Star2Right_Button.configure( bg= '#F0F0F0')
            Star3Left_Button.configure( bg= '#F0F0F0')
            Star3Right_Button.configure( bg= '#F0F0F0')
            Star4Left_Button.configure( bg= '#F0F0F0')
            Star4Right_Button.configure( bg= '#F0F0F0')
            Star5Left_Button.configure( bg= '#F0F0F0')
            Star5Right_Button.configure( bg= '#F0F0F0')
            Add_MoviePosterButton.configure( bg= '#F0F0F0' , fg='black' )
            frame_MovieButtons.configure( bg= '#F0F0F0')
            Confirm_Button.configure( bg= '#F0F0F0' , fg='black' )
            Reset_Button.configure( bg= '#F0F0F0' , fg='black' )
            Back_Button.configure( bg= '#F0F0F0' , fg='black' )
        except:
            pass
        try:
            Frame_EditMovie.configure( bg= '#F0F0F0')
            Label_EnterMovieNameEdit.configure( bg= '#F0F0F0')
            Label_EnterMovieYearEdit.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieGenreEdit.configure( bg= '#F0F0F0' , fg='black' )
            listboxEdit.configure( bg= '#F0F0F0' , fg='black' , selectbackground = 'gray')
            Label_EnterMovieRunEdit.configure( bg= '#F0F0F0' , fg='black' )
            LabelHoursEdit.configure( bg= '#F0F0F0' , fg='black' )
            LabelMinutesEdit.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieDirEdit.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieRatingEdit.configure( bg= '#F0F0F0' , fg='black' )
            Label_EnterMovieFranEdit.configure( bg= '#F0F0F0' , fg='black' )
            Frame_MovieRunEdit.configure( bg= '#F0F0F0')
            Frame_StarsEdit.configure( bg= '#F0F0F0')
            Star1Left_ButtonEdit.configure( bg= '#F0F0F0')
            Star2Left_ButtonEdit.configure( bg= '#F0F0F0')
            Star3Left_ButtonEdit.configure( bg= '#F0F0F0')
            Star4Left_ButtonEdit.configure( bg= '#F0F0F0')
            Star5Left_ButtonEdit.configure( bg= '#F0F0F0')
            Star1Right_ButtonEdit.configure( bg= '#F0F0F0')
            Star2Right_ButtonEdit.configure( bg= '#F0F0F0')
            Star3Right_ButtonEdit.configure( bg= '#F0F0F0')
            Star4Right_ButtonEdit.configure( bg= '#F0F0F0')
            Star5Right_ButtonEdit.configure( bg= '#F0F0F0')
            frame_MovieButtonsEdit.configure( bg= '#F0F0F0')
            Confirm_ButtonEdit.configure( bg= '#F0F0F0' , fg='black' )
            Reset_ButtonEdit.configure( bg= '#F0F0F0' , fg='black' )
        except:
            pass
        dark_modeMovies = False