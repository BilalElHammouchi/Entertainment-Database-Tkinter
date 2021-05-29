from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.messagebox
import mysql.connector
from datetime import datetime
import re

# MySQL set-up

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database="entertainment"
)

mycursor = mydb.cursor()

# root and icon

root = Tk()
root.title("App")
root.iconbitmap("popcorn.ico")

# Images

movie_img = ImageTk.PhotoImage( Image.open("clapperboard.png")  )
show_img = ImageTk.PhotoImage( Image.open("tv-show.png")  )
game_img = ImageTk.PhotoImage( Image.open("console.png")  )
book_img = ImageTk.PhotoImage( Image.open("open-book.png")  )
MovieMain_img = ImageTk.PhotoImage( Image.open("best movies2.jpg"))

#############################################################################################################
#                                                                                                           #
#                                            MOVIES                                                         #
#                                                                                                           #
#############################################################################################################


def Back_Movies():
    frame_EnterMovie.pack_forget()
    Frame_MovieMain.pack_forget()
    frame_entertainment.pack()

def Movies():
    Frame_MovieMain.pack_forget()
    frame_EnterMovie.pack()

star_number = None

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

def Reset_All():
    global Entry_MovieDir
    global star_number
    global Entry_MovieRunM
    global Entry_MovieRunH
    global listbox
    listbox.grid_forget()
    listbox = Listbox(frame_EnterMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
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
    listbox.grid( row = 2 , column = 1 )
    global Entry_MovieYear
    global Entry_MovieName
    global Entry_MovieFran
    Entry_MovieFran.grid_forget()
    Entry_MovieFran = Entry ( frame_EnterMovie )
    Entry_MovieFran.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieDir.grid_forget()
    Entry_MovieDir = Entry ( frame_EnterMovie )
    Entry_MovieDir.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )
    star_number = None
    Entry_MovieRunM.grid_forget()
    Entry_MovieRunM = Entry( Frame_MovieRun , width = 3)
    Entry_MovieRunM.grid( row = 0 , column = 2 )
    Entry_MovieRunH.grid_forget()
    Entry_MovieRunH = Entry( Frame_MovieRun , width = 3)
    Entry_MovieRunH.grid( row = 0 , column = 0 )
    Entry_MovieYear.grid_forget()
    Entry_MovieYear = Entry( frame_EnterMovie )
    Entry_MovieYear.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieName.grid_forget()
    Entry_MovieName = Entry( frame_EnterMovie )
    Entry_MovieName.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

def Reset_AllEdit():
    global Entry_MovieDirEdit
    global star_numberEdit
    global Entry_MovieRunMEdit
    global Entry_MovieRunHEdit
    global listboxEdit
    listboxEdit.grid_forget()
    listboxEdit = Listbox(frame_EditMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
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
    listboxEdit.grid( row = 2 , column = 1 )
    global Entry_MovieYearEdit
    global Entry_MovieNameEdit
    global Entry_MovieFranEdit
    Entry_MovieFranEdit.grid_forget()
    Entry_MovieFranEdit = Entry ( frame_EditMovie )
    Entry_MovieFranEdit.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieDirEdit.grid_forget()
    Entry_MovieDirEdit = Entry ( frame_EditMovie )
    Entry_MovieDirEdit.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )
    star_numberEdit = None
    Entry_MovieRunMEdit.grid_forget()
    Entry_MovieRunMEdit = Entry( Frame_MovieRunEdit , width = 3)
    Entry_MovieRunMEdit.grid( row = 0 , column = 2 )
    Entry_MovieRunHEdit.grid_forget()
    Entry_MovieRunHEdit = Entry( Frame_MovieRunEdit , width = 3)
    Entry_MovieRunHEdit.grid( row = 0 , column = 0 )
    Entry_MovieYearEdit.grid_forget()
    Entry_MovieYearEdit = Entry( frame_EditMovie )
    Entry_MovieYearEdit.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )
    Entry_MovieNameEdit.grid_forget()
    Entry_MovieNameEdit = Entry( frame_EditMovie )
    Entry_MovieNameEdit.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )


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

def Count():
    global hours
    hours = Entry_MovieRunH.get()
    if hours.isdigit():
        hours = int( hours )
    else:
        hours = 0
    global minutes
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

def List_Stop( ):
    global Choices
    global listbox
    Choices = listbox.curselection()
    global Choices2
    Choices2 = []
    for i in range( len(Choices) ) :
        Choices2.append( Choices[i] + 1 )
    
    if len(Choices) > 3:
        listbox.grid_forget()
        listbox = Listbox(frame_EnterMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
        listbox.insert(1, "Action")  
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
        listbox.grid( row = 2 , column = 1 )
        tkinter.messagebox.showerror("Error", "Only 3 genres or under")
        return False

    return True

def List_StopEdit( ):
    global ChoicesEdit
    global listboxEdit
    ChoicesEdit = listboxEdit.curselection()
    global Choices2Edit
    Choices2Edit = []
    for i in range( len(ChoicesEdit) ) :
        Choices2Edit.append( ChoicesEdit[i] + 1 )
    
    if len(ChoicesEdit) > 3:
        listboxEdit.grid_forget()
        listboxEdit = Listbox(frame_EnterMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
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

# Frame_MainMovies

Frame_MovieMain = Frame( root )
def Movie_Main():
    global Tree_variable
    Tree_variable = 0
    frame_entertainment.pack_forget()
    Frame_MovieView.pack_forget()
    frame_EnterMovie.pack_forget()

    Frame_MovieMain.pack()
    CanvasMovies = Canvas( Frame_MovieMain , width = 960 , height = 480 )
    CanvasMovies.create_image( 480, 240, image = MovieMain_img ) 
    CanvasMovies.grid( row = 0 , columnspan = 3 )
    EnterMovie_Button = Button( Frame_MovieMain , text ='Enter' , font=('Orelega One','16') , command = Movies )
    EnterMovie_Button.grid( row = 1 , column = 0 , pady = 10 )
    ViewMovie_Button = Button( Frame_MovieMain , text ='View' , font=('Orelega One','16') , command = lambda: Movie_View(None) )
    ViewMovie_Button.grid( row = 1 , column = 1 , pady = 10 )
    BackMovie_Button = Button( Frame_MovieMain , text ='Back' , font=('Orelega One','16') , command = Back_Movies )
    BackMovie_Button.grid( row = 1 , column = 2 , pady = 10 )

def Work_Movies( ):
    global Movie_Name
    Movie_Name = Entry_MovieName.get()
    if Movie_Name == '':
        tkinter.messagebox.showerror("Error", "You must include at least the name of the movie!")
        return 0
    global Movie_Year
    Movie_Year = Entry_MovieYear.get()
    if Movie_Year.isdigit():
        Movie_Year = int( Movie_Year )
    else:
        Movie_Year = None
    List_Stop()
    global Movie_Genre1
    global Movie_Genre2
    global Movie_Genre3
    global Choices2
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
    
    global Movie_Run
    Movie_Run = Count()
    global Movie_Dir
    Movie_Dir = Entry_MovieDir.get()
    global Movie_Stars
    global star_number
    Movie_Stars = star_number
    global Movie_Fran
    Movie_Fran = Entry_MovieFran.get()
    global Movie_added
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

    sql = "INSERT INTO movies (movie_name, movie_year, movie_genre1 , movie_genre2, movie_genre3, movie_runtime, movie_rating, movie_director, movie_franchise, movie_added_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ( Movie_Name , Movie_Year , Movie_Genre1 , Movie_Genre2 , Movie_Genre3 , Movie_Run , Movie_Stars , Movie_Dir , Movie_Fran ,Movie_added )
    mycursor.execute(sql, val)
    
    mydb.commit()
    Reset_All()
    

# Frame_EnterMovie

frame_EnterMovie = Frame( root )

Label_EnterMovieName = Label(frame_EnterMovie , text='Enter movie name: ' , font=('Orelega One','16') )
Label_EnterMovieName.grid( row  = 0 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieName = Entry( frame_EnterMovie )
Entry_MovieName.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieYear = Label(frame_EnterMovie , text='Enter year: ' , font=('Orelega One','16') )
Label_EnterMovieYear.grid( row  = 1 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieYear = Entry( frame_EnterMovie )
Entry_MovieYear.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieGenre = Label(frame_EnterMovie , text='Enter genre: ' , font=('Orelega One','16') )
Label_EnterMovieGenre.grid( row  = 2 , column = 0 , padx = 10 , pady = 10 )

listbox = Listbox(frame_EnterMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
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
listbox.grid( row = 2 , column = 1 )


Label_EnterMovieRun = Label(frame_EnterMovie , text='Enter run-time: ' , font=('Orelega One','16') )
Label_EnterMovieRun.grid( row  = 3 , column = 0 , padx = 10 , pady = 10 )

###### Frame_MovieRun

Frame_MovieRun = Frame( frame_EnterMovie )
Frame_MovieRun.grid( row = 3 , column = 1 , padx = 10 , pady = 10 )
Entry_MovieRunH = Entry( Frame_MovieRun , width = 3)
Entry_MovieRunH.grid( row = 0 , column = 0 )
LabelHours = Label( Frame_MovieRun, text = 'hour(s)' , font=('Orelega One','16') )
LabelHours.grid( row = 0 , column = 1 )
Entry_MovieRunM = Entry( Frame_MovieRun , width = 3)
Entry_MovieRunM.grid( row = 0 , column = 2 )
LabelMinutes = Label( Frame_MovieRun, text = 'minute(s)' , font=('Orelega One','16') )
LabelMinutes.grid( row = 0 , column = 3 )

#######

Label_EnterMovieDir = Label(frame_EnterMovie , text='Enter Director: ' , font=('Orelega One','16') )
Label_EnterMovieDir.grid( row = 4 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieDir = Entry ( frame_EnterMovie )
Entry_MovieDir.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieRating = Label(frame_EnterMovie , text='Choose rating: ' , font=('Orelega One','16') )
Label_EnterMovieRating.grid( row  = 5 , column = 0 , padx = 10 , pady = 10 )

Label_EnterMovieFran = Label(frame_EnterMovie , text='Enter movie franchise: ' , font=('Orelega One','16') )
Label_EnterMovieFran.grid( row = 6 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieFran = Entry ( frame_EnterMovie )
Entry_MovieFran.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )

# Frame_Stars

Frame_Stars = Frame( frame_EnterMovie )
Frame_Stars.grid( row = 5 , column = 1 )

starleft_img = ImageTk.PhotoImage( Image.open("star_left.png")  )
starright_img = ImageTk.PhotoImage( Image.open("star_right.png")  )

Star1Left_Button = Button(Frame_Stars , image = starleft_img , bd = 0 , command = lambda: Star_Amount(0.5) , activebackground = '#F9FFB5' )
Star1Left_Button.grid( row = 0 ,  column = 0 )
Star1Right_Button = Button(Frame_Stars , image = starright_img , bd = 0 , command = lambda: Star_Amount(1) , activebackground = '#F9FFB5')
Star1Right_Button.grid( row = 0 ,  column = 1 )

Star2Left_Button = Button(Frame_Stars , image = starleft_img , bd = 0 , command = lambda: Star_Amount(1.5)  , activebackground = '#F9FFB5')
Star2Left_Button.grid( row = 0 , column = 2 )
Star2Right_Button = Button(Frame_Stars , image = starright_img , bd = 0 , command = lambda: Star_Amount(2)  , activebackground = '#F9FFB5')
Star2Right_Button.grid( row = 0 , column = 3 )

Star3Left_Button = Button(Frame_Stars , image = starleft_img , bd = 0 , command = lambda: Star_Amount(2.5) , activebackground = '#F9FFB5' )
Star3Left_Button.grid( row = 0 , column = 4 )
Star3Right_Button = Button(Frame_Stars , image = starright_img , bd = 0 , command = lambda: Star_Amount(3) , activebackground = '#F9FFB5' )
Star3Right_Button.grid( row = 0 , column = 5 )

Star4Left_Button = Button(Frame_Stars , image = starleft_img , bd = 0 , command = lambda: Star_Amount(3.5) , activebackground = '#F9FFB5' )
Star4Left_Button.grid( row = 0 , column = 6 )
Star4Right_Button = Button(Frame_Stars , image = starright_img , bd = 0 , command = lambda: Star_Amount(4) , activebackground = '#F9FFB5' )
Star4Right_Button.grid( row = 0 , column = 7 )

Star5Left_Button = Button(Frame_Stars , image = starleft_img , bd = 0 , command = lambda: Star_Amount(4.5) , activebackground = '#F9FFB5' )
Star5Left_Button.grid( row = 0 , column = 8 )
Star5Right_Button = Button(Frame_Stars , image = starright_img , bd = 0 , command = lambda: Star_Amount(5) , activebackground = '#F9FFB5' )
Star5Right_Button.grid( row = 0 , column = 9 )

# Frame_EnterMovie Buttons

frame_MovieButtons = Frame( frame_EnterMovie )
frame_MovieButtons.grid( row = 7 , columnspan = 2)

Confirm_Button = Button(frame_MovieButtons , text = 'Confirm' , font=('Orelega One','16') , command = Work_Movies )
Confirm_Button.grid( row = 0 , column = 0 , padx = 30 , pady = 30 )
Reset_Button = Button(frame_MovieButtons , text = 'Reset' , font=('Orelega One','16') , command = Reset_All )
Reset_Button.grid( row = 0 , column = 1 , padx = 30 , pady = 30 )
Back_Button = Button(frame_MovieButtons , text = 'Back' , font=('Orelega One','16') , command = Movie_Main )
Back_Button.grid( row = 0 , column = 2 , padx = 30 , pady = 30)

# Frames

frame_entertainment = Frame(root)
frame_entertainment.pack()
frame_movies = Frame(frame_entertainment)
frame_movies.grid( row = 0 , column = 0 , padx = 2 , pady = 2 )
frame_tv = Frame(frame_entertainment)
frame_tv.grid( row = 0 , column = 1 , padx = 2 , pady = 2 )
frame_games = Frame(frame_entertainment)
frame_games.grid( row = 1 , column = 0 , padx = 2 , pady = 2 )
frame_books = Frame(frame_entertainment)
frame_books.grid( row = 1 , column = 1 , padx = 2 , pady = 2 )


# Frame_ViewMovies
Frame_MovieView = Frame( root )

switch_MovieId = 0
switch_MovieName = 0
switch_MovieYear = 0
switch_MovieGenre = 0
switch_MovieRun = 0
switch_MovieRating = 0
switch_MovieDate = 0
switch_MovieDirector = 0
switch_MovieFranchise = 0
Edit_Or_Click = 0

def Movie_View( option ):
    Frame_MovieMain.pack_forget()
    Frame_MovieView.pack()
    global option2
    option2 = option
    global tree
    global Edit_Or_Click
    global switch_MovieId
    global switch_MovieName
    global switch_MovieYear
    global switch_MovieGenre
    global switch_MovieRun
    global switch_MovieRating
    global switch_MovieDate
    global switch_MovieDirector
    global switch_MovieFranchise
    if option == 'ID' or option is None:
        if switch_MovieId % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_id"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_id DESC"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieId += 1
    elif option == 'Name':
        if switch_MovieName % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_name DESC"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_name" 
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieName += 1
    elif option == 'Year':
        if switch_MovieYear % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , years.year_actual , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movies.movie_franchise, movies.movie_year FROM movies LEFT JOIN years ON movies.movie_year = years.year_id ORDER BY years.year_actual"
            mycursor.execute(sql)
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , years.year_actual , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movies.movie_franchise, movies.movie_year FROM movies LEFT JOIN years ON movies.movie_year = years.year_id ORDER BY years.year_actual DESC"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieYear += 1
    elif option == 'Genre':
        if Edit_Or_Click == 0:
            switch_MovieGenre += 1
        if switch_MovieGenre % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_genre1, movie_genre2, movie_genre3"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_genre1 DESC, movie_genre2 DESC, movie_genre3 DESC"
            mycursor.execute(sql)
    elif option == 'Runtime':
        if switch_MovieRun % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_runtime"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_runtime DESC"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieRun += 1
    elif option == 'Rating':
        if switch_MovieRating % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_rating"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_rating DESC"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieRating += 1
    elif option == 'Date added':
        if switch_MovieDate % 2 == 0:
            sql = "SELECT * FROM movies ORDER BY movie_added_time"
            mycursor.execute(sql)
        else:
            sql = "SELECT * FROM movies ORDER BY movie_added_time DESC"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieDate += 1
    elif option == 'Director':
        if switch_MovieDirector % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, directors.director_name, movies.movie_franchise, movies.movie_director FROM movies LEFT JOIN directors ON movies.movie_director = directors.director_id ORDER BY directors.director_name DESC"
            mycursor.execute(sql)
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, directors.director_name, movies.movie_franchise, movies.movie_director FROM movies LEFT JOIN directors ON movies.movie_director = directors.director_id ORDER BY directors.director_name"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieDirector += 1
    elif option == 'Franchise':
        if switch_MovieFranchise % 2 == 0:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movie_franchises.mf_name, movies.movie_franchise FROM movies LEFT JOIN movie_franchises ON movies.movie_franchise = movie_franchises.mf_id ORDER BY movie_franchises.mf_name DESC"
            mycursor.execute(sql)
        else:
            sql = "SELECT movies.movie_id, movies.movie_name , movies.movie_year , movies.movie_genre1, movies.movie_genre2, movies.movie_genre3, movies.movie_runtime, movies.movie_rating, movies.movie_added_time, movies.movie_director, movie_franchises.mf_name, movies.movie_franchise FROM movies LEFT JOIN movie_franchises ON movies.movie_franchise = movie_franchises.mf_id ORDER BY movie_franchises.mf_name"
            mycursor.execute(sql)
        if Edit_Or_Click == 0:
            switch_MovieFranchise += 1
    Edit_Or_Click = 0

    movie_result = mycursor.fetchall()
    tree = ttk.Treeview(Frame_MovieView, column=("c1", "c2", "c3" , "c4" , "c5" , "c6" , "c7" , "c8" , "c9"
             ) , show='headings' , yscrollcommand = TRUE , height = 20 , )
    tree.column("#1", anchor= CENTER , width = 50 )
    tree.heading("#1", text="ID" , command = lambda : Movie_View('ID') )
    tree.column("#2", anchor= CENTER , width = 300 )
    tree.heading("#2", text="Name" , command = lambda : Movie_View('Name') )
    tree.column("#3", anchor= CENTER , width = 50 )
    tree.heading("#3", text="Year" , command = lambda : Movie_View('Year') )
    tree.column("#4", anchor= CENTER)
    tree.heading("#4", text="Genre" , command = lambda : Movie_View('Genre') )
    tree.column("#5", anchor= CENTER , width = 70)
    tree.heading("#5", text="Runtime" , command = lambda : Movie_View('Runtime') )
    tree.column("#6", anchor= CENTER , width = 50)
    tree.heading("#6", text="Rating" , command = lambda : Movie_View('Rating') )
    tree.column("#7", anchor= CENTER , width = 150)
    tree.heading("#7", text="Date added" , command = lambda : Movie_View('Date added') )
    tree.column("#8", anchor= CENTER)
    tree.heading("#8", text="Director" , command = lambda : Movie_View('Director') )
    tree.column("#9", anchor= CENTER)
    tree.heading("#9", text="Franchise" , command = lambda : Movie_View('Franchise') )
    global all_movies
    all_movies = []
    for movie in movie_result:
        movie_actual = []
        movie_actual.append(movie[0])
        movie_actual.append(movie[1])
        if option == 'Year':
            movie_actual.append(movie[2])
        else:
            movie_result_year = movie[2]
            sql = "SELECT year_actual FROM years WHERE year_id = %s"
            adr = ( movie_result_year , )
            mycursor.execute(sql, adr)
            movie_result_year = mycursor.fetchall()
            if movie_result_year == []:
                movie_actual.append( None )
            else:
                movie_actual.append( movie_result_year[0][0] )
        movie_result_genre1 = movie[3]
        movie_result_genre2 = movie[4]
        movie_result_genre3 = movie[5]
        sql = "SELECT genre_name FROM genres WHERE genre_id = %s OR genre_id = %s OR genre_id = %s"
        adr = ( movie_result_genre1 , movie_result_genre2 , movie_result_genre3 )
        mycursor.execute(sql, adr)
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
        if option == 'Director':
            movie_actual.append( movie[9] )
        else:
            movie_result_director = movie[9]
            sql = "SELECT director_name FROM directors WHERE director_id = %s"
            adr = ( movie_result_director , )
            mycursor.execute(sql, adr)
            movie_result_director = mycursor.fetchall()
            movie_actual.append( movie_result_director[0][0] )
        if option == 'Franchise':
            movie_actual.append( movie[10] )
        else:
            movie_result_franchise = movie[10]
            sql = "SELECT mf_name FROM movie_franchises WHERE mf_id = %s"
            adr = ( movie_result_franchise , )
            mycursor.execute(sql, adr)
            movie_result_franchise = mycursor.fetchall()
            movie_actual.append( movie_result_franchise[0][0] )
        all_movies.append( movie_actual )
    all_movies.reverse()
    for i in range(20):
        tree.insert("", END, values= all_movies[i] )
    tree.grid( row = 0 , columnspan = 5 )
    Button_BackMovieMain = Button( Frame_MovieView , text = 'Back' , command = Movie_Main , font=('Orelega One','16') )
    Button_BackMovieMain.grid( row = 2 , column = 2 , pady = 10 )
    global Button_LeftMovieMain
    Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') , state = DISABLED )
    Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
    global Button_RightMovieMain
    Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16') )
    Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )
    global Button_LeftMaxMovieMain
    Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') , state = DISABLED )
    Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
    global Button_RightMaxMovieMain
    Button_RightMaxMovieMain = Button( Frame_MovieView , text = '>>>' , command =lambda: TreeMovies('right_max') , font=('Orelega One','16') )
    Button_RightMaxMovieMain.grid( row = 1 , column = 4 , pady = 10 )
    Button_EditMovieMain = Button( Frame_MovieView , text = 'Edit' , command = Edit_Movie , font=('Orelega One','16') )
    Button_EditMovieMain.grid( row = 2 , column = 0 , columnspan = 2)
    Button_DeleteMovieMain = Button( Frame_MovieView , text = 'Delete' , command = Delete_Movie , font=('Orelega One','16') )
    Button_DeleteMovieMain.grid( row = 2 , column = 3 , columnspan = 2)

Tree_variable = 0
Tree_variable_max = 0

def TreeMovies( turn ):
    global Tree_variable
    global tree
    global all_movies
    global Button_RightMovieMain
    global Button_LeftMovieMain
    global Button_RightMaxMovieMain
    global Button_LeftMaxMovieMain
    global Tree_variable_max
    Tree_variable_max = len( all_movies ) // 20 + 1
    if turn == 'right' :
        Tree_variable += 1
        if Tree_variable > 0:
            Button_LeftMovieMain.grid_forget()
            Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') )
            Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
            Button_LeftMaxMovieMain.grid_forget()
            Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') )
            Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
        else:
            Button_LeftMovieMain.grid_forget()
            Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') , state = DISABLED )
            Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
        for record in tree.get_children():
                tree.delete( record )
        for i in range( Tree_variable*20 , (Tree_variable + 1 )*20 ):
            try:
                tree.insert("", END, values= all_movies[i] )
            except:
                Button_RightMovieMain.grid_forget()
                Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16') , state = DISABLED )
                Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )

    if turn == 'left':
        Tree_variable -= 1
        if Tree_variable == 0:
            Button_LeftMaxMovieMain.grid_forget()
            Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') , state = DISABLED )
            Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
            Button_LeftMovieMain.grid_forget()
            Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') , state = DISABLED )
            Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
        if Tree_variable < Tree_variable_max:
            Button_RightMovieMain.grid_forget()
            Button_RightMaxMovieMain.grid_forget()
            Button_RightMaxMovieMain = Button( Frame_MovieView , text = '>>>' , command =lambda: TreeMovies('right_max') , font=('Orelega One','16') )
            Button_RightMaxMovieMain.grid( row = 1 , column = 4 , pady = 10 )
            Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16') )
            Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )
        for record in tree.get_children():
            tree.delete( record )
        for i in range( Tree_variable*20 , (Tree_variable + 1 )*20 ):
            tree.insert("", END, values= all_movies[i] )
    if turn == 'right_max' :
        for record in tree.get_children():
            tree.delete( record )
        for i in range( (Tree_variable_max - 1)*20 , (Tree_variable_max )*20 ):
            try:
                tree.insert("", END, values= all_movies[i] )
            except:
                Button_LeftMovieMain.grid_forget()
                Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') )
                Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
                Button_RightMovieMain.grid_forget()
                Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16') , state = DISABLED )
                Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )
                Button_RightMaxMovieMain.grid_forget()
                Button_RightMaxMovieMain = Button( Frame_MovieView , text = '>>>' , command =lambda: TreeMovies('right_max') , font=('Orelega One','16') , state = DISABLED )
                Button_RightMaxMovieMain.grid( row = 1 , column = 4 , pady = 10 )
                Button_LeftMaxMovieMain.grid_forget()
                Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') )
                Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
        Tree_variable = Tree_variable_max - 1
    if turn == 'left_max' :
        for record in tree.get_children():
            tree.delete( record )
        for i in range( 20 ):
            try:
                tree.insert("", END, values= all_movies[i] )
                Button_LeftMovieMain.grid_forget()
                Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') , state = DISABLED )
                Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
                Button_RightMovieMain.grid_forget()
                Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16')  )
                Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )
                Button_RightMaxMovieMain.grid_forget()
                Button_RightMaxMovieMain = Button( Frame_MovieView , text = '>>>' , command =lambda: TreeMovies('right_max') , font=('Orelega One','16') )
                Button_RightMaxMovieMain.grid( row = 1 , column = 4 , pady = 10 )
                Button_LeftMaxMovieMain.grid_forget()
                Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') , state = DISABLED )
                Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
            except:
                Button_LeftMovieMain.grid_forget()
                Button_LeftMovieMain = Button( Frame_MovieView , text = '<<' , command =lambda: TreeMovies('left') , font=('Orelega One','16') )
                Button_LeftMovieMain.grid( row = 1 , column = 1 , pady = 10 )
                Button_RightMovieMain.grid_forget()
                Button_RightMovieMain = Button( Frame_MovieView , text = '>>' , command =lambda: TreeMovies('right') , font=('Orelega One','16') , state = DISABLED )
                Button_RightMovieMain.grid( row = 1 , column = 3 , pady = 10 )
                Button_RightMaxMovieMain.grid_forget()
                Button_RightMaxMovieMain = Button( Frame_MovieView , text = '>>>' , command =lambda: TreeMovies('right_max') , font=('Orelega One','16') , state = DISABLED )
                Button_RightMaxMovieMain.grid( row = 1 , column = 4 , pady = 10 )
                Button_LeftMaxMovieMain.grid_forget()
                Button_LeftMaxMovieMain = Button( Frame_MovieView , text = '<<<' , command =lambda: TreeMovies('left_max') , font=('Orelega One','16') )
                Button_LeftMaxMovieMain.grid( row = 1 , column = 0 , pady = 10 )
        Tree_variable = 0
        
def Delete_Movie( ):
    global tree
    for number in tree.selection():
        temp = tree.item( number )
        tree.delete( number )
        sql = "DELETE FROM movies WHERE movie_id = %s "
        add = ( temp['values'][0] , )
        mycursor.execute(sql , add )
        mydb.commit()
    Movie_View( None )


# Frame Edit Movies

def disable_event():
    global EditMovies_Window
    EditMovies_Window.withdraw()

EditMovies_Window = Toplevel( )
EditMovies_Window.protocol( "WM_DELETE_WINDOW" , disable_event )
EditMovies_Window.title( "Edit Your Movie" )
EditMovies_Window.iconbitmap("edit.ico")
EditMovies_Window.withdraw()
frame_EditMovie = Frame( EditMovies_Window )

def Edit_Movie():

    global tree
    global EditMovies_Window
    global frame_EditMovie
    global Entry_MovieNameEdit
    global Entry_MovieYearEdit
    global listboxEdit
    global Entry_MovieRunHEdit
    global Entry_MovieRunMEdit
    global Entry_MovieDirEdit
    global Entry_MovieFranEdit
    global EditMovies_Window
    EditMovies_Window.deiconify()
    frame_EditMovie.pack()
    Reset_AllEdit()
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
        Entry_MovieRunHEdit.insert(0 , test2[0] )
        Entry_MovieRunMEdit.insert(0 , test2[1] )
        Entry_MovieDirEdit.insert(0 , temp['values'][7] )
        Entry_MovieFranEdit.insert(0 , temp['values'][8] )

def ConfirmMovies_Edit():
    global tree
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
    List_StopEdit()
    global Movie_Genre1Edit
    global Movie_Genre2Edit
    global Movie_Genre3Edit
    global Choices2Edit
    Movie_Genre1Edit = Movie_Genre2Edit = Movie_Genre3Edit = None
    #print(Choices2)
    
    if len(Choices2Edit) == 1:
        Movie_Genre1Edit = Choices2Edit[0] 
    elif len( Choices2Edit ) == 2:
        Movie_Genre1Edit = Choices2Edit[0] 
        Movie_Genre2Edit = Choices2Edit[1]
    elif len(Choices2Edit ) == 3:
        Movie_Genre1Edit = Choices2Edit[0] 
        Movie_Genre2Edit = Choices2Edit[1]
        Movie_Genre3Edit = Choices2Edit[2]
    
    global Movie_RunEdit
    Movie_RunEdit = CountEdit()
    global Movie_DirEdit
    Movie_DirEdit = Entry_MovieDirEdit.get()
    global Movie_StarsEdit
    global star_numberEdit
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

    sql = "UPDATE movies SET movie_name = %s, movie_year = %s, movie_genre1 = %s, movie_genre2 = %s, movie_genre3 = %s, movie_runtime = %s, movie_rating = %s, movie_director = %s, movie_franchise = %s WHERE movie_id = %s"
    val = ( Movie_NameEdit , Movie_YearEdit , Movie_Genre1Edit , Movie_Genre2Edit , Movie_Genre3Edit , Movie_RunEdit , Movie_StarsEdit , Movie_DirEdit , Movie_FranEdit  ,  Movie_IdEdit )
    mycursor.execute(sql, val)
    
    mydb.commit()
    EditMovies_Window.withdraw()
    global option2
    global Edit_Or_Click
    Edit_Or_Click = 1
    Movie_View( option2 )


Label_EnterMovieNameEdit = Label(frame_EditMovie , text='Enter movie name: ' , font=('Orelega One','16') )
Label_EnterMovieNameEdit.grid( row  = 0 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieNameEdit = Entry( frame_EditMovie )
Entry_MovieNameEdit.grid( row = 0 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieYearEdit = Label(frame_EditMovie , text='Enter year: ' , font=('Orelega One','16') )
Label_EnterMovieYearEdit.grid( row  = 1 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieYearEdit = Entry( frame_EditMovie )
Entry_MovieYearEdit.grid( row = 1 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieGenreEdit = Label(frame_EditMovie , text='Enter genre: ' , font=('Orelega One','16') )
Label_EnterMovieGenreEdit.grid( row  = 2 , column = 0 , padx = 10 , pady = 10 )

listboxEdit = Listbox(frame_EditMovie , selectmode=MULTIPLE , selectbackground='gray' , height=25  , font=('Orelega One','12') )
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
listboxEdit.grid( row = 2 , column = 1 )


Label_EnterMovieRunEdit = Label(frame_EditMovie , text='Enter run-time: ' , font=('Orelega One','16') )
Label_EnterMovieRunEdit.grid( row  = 3 , column = 0 , padx = 10 , pady = 10 )

###### Frame_MovieRun

Frame_MovieRunEdit = Frame( frame_EditMovie )
Frame_MovieRunEdit.grid( row = 3 , column = 1 , padx = 10 , pady = 10 )
Entry_MovieRunHEdit = Entry( Frame_MovieRunEdit , width = 3)
Entry_MovieRunHEdit.grid( row = 0 , column = 0 )
LabelHoursEdit = Label( Frame_MovieRunEdit, text = 'hour(s)' , font=('Orelega One','16') )
LabelHoursEdit.grid( row = 0 , column = 1 )
Entry_MovieRunMEdit = Entry( Frame_MovieRunEdit , width = 3)
Entry_MovieRunMEdit.grid( row = 0 , column = 2 )
LabelMinutesEdit = Label( Frame_MovieRunEdit, text = 'minute(s)' , font=('Orelega One','16') )
LabelMinutesEdit.grid( row = 0 , column = 3 )

#######

Label_EnterMovieDirEdit = Label(frame_EditMovie , text='Enter Director: ' , font=('Orelega One','16') )
Label_EnterMovieDirEdit.grid( row = 4 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieDirEdit = Entry ( frame_EditMovie )
Entry_MovieDirEdit.grid( row = 4 , column = 1 , padx = 10 , pady = 10 )

Label_EnterMovieRatingEdit = Label(frame_EditMovie , text='Choose rating: ' , font=('Orelega One','16') )
Label_EnterMovieRatingEdit.grid( row  = 5 , column = 0 , padx = 10 , pady = 10 )

Label_EnterMovieFranEdit = Label(frame_EditMovie , text='Enter movie franchise: ' , font=('Orelega One','16') )
Label_EnterMovieFranEdit.grid( row = 6 , column = 0 , padx = 10 , pady = 10 )
Entry_MovieFranEdit = Entry ( frame_EditMovie )
Entry_MovieFranEdit.grid( row = 6 , column = 1 , padx = 10 , pady = 10 )

# Frame_Stars

Frame_StarsEdit = Frame( frame_EditMovie )
Frame_StarsEdit.grid( row = 5 , column = 1 )

Star1Left_ButtonEdit = Button(Frame_StarsEdit , image = starleft_img , bd = 0 , command = lambda: Star_AmountEdit(0.5) , activebackground = '#F9FFB5' )
Star1Left_ButtonEdit.grid( row = 0 ,  column = 0 )
Star1Right_ButtonEdit = Button(Frame_StarsEdit , image = starright_img , bd = 0 , command = lambda: Star_AmountEdit(1) , activebackground = '#F9FFB5')
Star1Right_ButtonEdit.grid( row = 0 ,  column = 1 )

Star2Left_ButtonEdit = Button(Frame_StarsEdit , image = starleft_img , bd = 0 , command = lambda: Star_AmountEdit(1.5)  , activebackground = '#F9FFB5')
Star2Left_ButtonEdit.grid( row = 0 , column = 2 )
Star2Right_ButtonEdit = Button(Frame_StarsEdit , image = starright_img , bd = 0 , command = lambda: Star_AmountEdit(2)  , activebackground = '#F9FFB5')
Star2Right_ButtonEdit.grid( row = 0 , column = 3 )

Star3Left_ButtonEdit = Button(Frame_StarsEdit , image = starleft_img , bd = 0 , command = lambda: Star_AmountEdit(2.5) , activebackground = '#F9FFB5' )
Star3Left_ButtonEdit.grid( row = 0 , column = 4 )
Star3Right_ButtonEdit = Button(Frame_StarsEdit , image = starright_img , bd = 0 , command = lambda: Star_AmountEdit(3) , activebackground = '#F9FFB5' )
Star3Right_ButtonEdit.grid( row = 0 , column = 5 )

Star4Left_ButtonEdit = Button(Frame_StarsEdit , image = starleft_img , bd = 0 , command = lambda: Star_AmountEdit(3.5) , activebackground = '#F9FFB5' )
Star4Left_ButtonEdit.grid( row = 0 , column = 6 )
Star4Right_ButtonEdit = Button(Frame_StarsEdit , image = starright_img , bd = 0 , command = lambda: Star_AmountEdit(4) , activebackground = '#F9FFB5' )
Star4Right_ButtonEdit.grid( row = 0 , column = 7 )

Star5Left_ButtonEdit = Button(Frame_StarsEdit , image = starleft_img , bd = 0 , command = lambda: Star_AmountEdit(4.5) , activebackground = '#F9FFB5' )
Star5Left_ButtonEdit.grid( row = 0 , column = 8 )
Star5Right_ButtonEdit = Button(Frame_StarsEdit , image = starright_img , bd = 0 , command = lambda: Star_AmountEdit(5) , activebackground = '#F9FFB5' )
Star5Right_ButtonEdit.grid( row = 0 , column = 9 )

# Frame_EnterMovie Buttons

frame_MovieButtonsEdit = Frame( frame_EditMovie )
frame_MovieButtonsEdit.grid( row = 7 , columnspan = 2)

Confirm_ButtonEdit = Button(frame_MovieButtonsEdit , text = 'Confirm' , font=('Orelega One','16') , command = ConfirmMovies_Edit )
Confirm_ButtonEdit.grid( row = 0 , column = 0 , padx = 30 , pady = 30 )
Reset_ButtonEdit = Button(frame_MovieButtonsEdit , text = 'Reset' , font=('Orelega One','16') , command = Reset_AllEdit )
Reset_ButtonEdit.grid( row = 0 , column = 2 , padx = 30 , pady = 30 )




#############################################################################################################
#                                                                                                           #
#                                            TV Shows                                                       #
#                                                                                                           #
#############################################################################################################        



# Frame_MainMenu

MyLabel_Movie = Button(frame_movies , bd = 4 , image = movie_img , bg = "#b00029" , activebackground = "#ff003b" , command=Movie_Main ) 
MyLabel_Movie2 = Label(frame_movies , text= 'Movies' , font=('Orelega One','16' , 'italic underline') )
MyLabel_Movie2.grid( row = 0)
MyLabel_Movie.grid( row = 1 )


MyLabel_Tv = Button(frame_tv , bd = 4 ,  image = show_img , bg = "#005bb0" , activebackground = "#0084ff")
MyLabel_Tv2 = Label(frame_tv , text= 'TV Shows', font=('Orelega One','16' , 'italic underline') )
MyLabel_Tv2.grid( row = 0 )
MyLabel_Tv.grid( row = 1 )


MyLabel_Book = Button(frame_books  , bd = 4 , image = book_img , bg = "#b3bd00" , activebackground = "#f2ff00")
MyLabel_Book2 = Label( frame_books , text='Books', font=('Orelega One','16' , 'italic underline') )
MyLabel_Book2.grid( row = 0 )
MyLabel_Book.grid( row = 1 )


MyLabel_Game = Button(frame_games , bd = 4  , image = game_img , bg = "#00b509" , activebackground = "#00ff0d")
MyLabel_Game2 = Label( frame_games , text='Games', font=('Orelega One','16' , 'italic underline'))
MyLabel_Game2.grid( row = 0 )
MyLabel_Game.grid( row = 1 )



root.mainloop()