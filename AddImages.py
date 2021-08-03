from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
import requests
import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from urllib.request import Request, urlopen
import sys 

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    return filename
movies = [ ]
def Find_MovieImage(Entry_MovieName):
    Movie_Name = Entry_MovieName.get()
    if Movie_Name == '':
        tkinter.messagebox.showerror("Error", "You must include at least the name of the movie!")
        return 0
    ChooseMovie_Window( )
    global Frame_AddMoviePoster, AddMoviePoster_Window, movies
    movies = []
    AddMoviePoster_Window.deiconify()
    Frame_AddMoviePoster.pack()
    Movie_Name = Movie_Name.replace(" ","+")
    """"
    url = "https://www.themoviedb.org/search?query=" + Movie_Name
    html = urlopen(url, context=ctx).read()
    """
    req = Request('https://www.themoviedb.org/search/movie?query=' + Movie_Name, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    anchor_rows = soup.findAll('a')
    span_rows = soup.findAll('span')
    movie_years = []
    for span in span_rows:
        class_span = span.get('class')
        if class_span == ['release_date'] :   
            text = span.get_text()
            movie_years.append(text)
    
    i = j = 0
    movies_placeholder = []
    for row in anchor_rows:
        class_anchor = row.get('class')
        data_media = row.get('data-media-type')
        image_notfound = ImageTk.PhotoImage( Image.open("Images/image-not-found.png").resize((94,141), Image.ANTIALIAS) )
        if class_anchor == ['result'] and data_media == 'movie':
            if i % 2 == 0 :
                image_anchor = row.find_all('img')
                if image_anchor != []:
                    for link in image_anchor:
                        img_url = link.get('src')
                    if not img_url:
                        continue
                    try:
                        pos = img_url.index("?")
                        img_url = img_url[:pos]
                    except ValueError:
                        pass
                    img_url = urljoin('https://www.themoviedb.org/search/movie?query=' + Movie_Name, img_url)
                    filename = download( img_url,"Images/Movies/current")
                    filename = filename.replace('\\','/')
                    filename = Image.open(filename) 
                    #filename= filename.resize((94,100), Image.ANTIALIAS)
                    icon = ImageTk.PhotoImage( filename )
                    movies_placeholder.append(icon)
                else:
                    movies_placeholder.append(image_notfound)
            elif i % 2 == 1:
                movies_placeholder.append(row.find('h2').get_text())
                try:
                    movies_placeholder.append(movie_years[j])
                except:
                    movies_placeholder.append("TBD")
                #movies_placeholder.append(movie_description[j])
                movies_placeholder.append(row.get('href'))
                if movies_placeholder != []:
                    movies.append(movies_placeholder)
                movies_placeholder = []
                j += 1
        i += 1
    Insert_TreeMovieIcon( None )
    ConfirmPoster_Button = Button(Frame_AddMoviePoster, font=('Orelega One','16'), text= 'Confirm', command= Confirm_MoviePoster )
    ConfirmPoster_Button.grid( row = 1 , column = 0, padx = 15, pady = 30 )
    AddPoster_Button = Button(Frame_AddMoviePoster, font=('Orelega One','16'), text= 'Add Manually' )
    AddPoster_Button.grid( row = 1 , column = 1 , padx = 15, pady = 30 )

def _on_mouse_wheel(event):
    global Poster_Canvas
    Poster_Canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

switch_movieposter_year = switch_movieposter_name = 0
poster_buttons = []
posters = []
def Insert_TreeMovieIcon( option ):
    global movies, switch_movieposter_year, switch_movieposter_name, tree_select_movie,Frame_AddMoviePoster
    Frame_tree_select_movie = Frame( Frame_AddMoviePoster )
    Frame_tree_select_movie.grid( row = 0 , columnspan =	2 )
    tree_select_movie = ttk.Treeview( Frame_tree_select_movie , column=("c1","c2") , height = 5 , style='Poster.Treeview' ,)
    tree_select_movie.pack(  side = LEFT, fill = BOTH )
    scrollbar_tree_select_movie = Scrollbar( Frame_tree_select_movie )
    scrollbar_tree_select_movie.pack(side = RIGHT, fill = BOTH )
    tree_select_movie.config(yscrollcommand = scrollbar_tree_select_movie.set)
    scrollbar_tree_select_movie.config(command = tree_select_movie.yview)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Poster.Treeview', rowheight=143)
    tree_select_movie.heading("#0", text="Icon" )
    tree_select_movie.column("#0" , width = 130 )
    tree_select_movie.heading("#1", text="Name" , command=lambda:Insert_TreeMovieIcon('Name'))
    tree_select_movie.column("#1", anchor= CENTER , width = 500 )
    tree_select_movie.heading("#2", text="Year" , command=lambda:Insert_TreeMovieIcon('Year') )
    tree_select_movie.column("#2", anchor= CENTER , width = 150 )
    if option == 'Year':
        for i in range(len(movies)-1):
            switch_movieposter_name = 0
            j = i + 1
            while movies[j][2] > movies[j-1][2] and j > 0:
                temp = movies[j]
                movies[j] = movies[j-1]
                movies[j-1] = temp
                j -= 1
        if switch_movieposter_year % 2 == 1:
            movies.reverse()
        switch_movieposter_year += 1
    if option == 'Name':
        switch_movieposter_year = 0
        for i in range(len(movies)-1):
            j = i + 1
            while movies[j][1] < movies[j-1][1] and j > 0:
                temp = movies[j]
                movies[j] = movies[j-1]
                movies[j-1] = temp
                j -= 1
        if switch_movieposter_name % 2 == 1:
            movies.reverse()
        switch_movieposter_name += 1
    for movie in movies:
        tree_select_movie.insert('', 'end', image = movie[0] , values= (movie[1],movie[2], movie[3]) )

def Confirm_MoviePoster():
    global tree_select_movie, Frame_AddMoviePoster, Frame_ChooseMoviePoster, AddMoviePoster_Window,poster_buttons, posters, ChoosePoster_Window,Poster_Canvas
    movie_selected = tree_select_movie.selection()
    temp = tree_select_movie.item( movie_selected )
    if movie_selected == ():
        tkinter.messagebox.showerror("Error", "You must select a movie!")
        return 0
    elif len(movie_selected) > 1:
        tkinter.messagebox.showerror("Error", "You must select only one movie!")
        return 1
    posters = []
    Choose_PosterWindow()
    AddMoviePoster_Window.withdraw()
    ChoosePoster_Window.deiconify()
    Frame_ChooseMoviePoster = Frame(ChoosePoster_Window )
    Frame_ChooseMoviePoster.grid( row = 0)
    Poster_Canvas = Canvas( Frame_ChooseMoviePoster , width= 1115, height=650)
    Poster_Canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    Poster_Canvas.pack(side = LEFT, fill = BOTH, expand = 1 )
    Poster_Scrollbar = Scrollbar(Frame_ChooseMoviePoster, orient = VERTICAL, command=Poster_Canvas.yview)
    Poster_Scrollbar.pack(side = LEFT, fill = Y)
    Poster_Canvas.configure( yscrollcommand= Poster_Scrollbar.set )
    Poster_Canvas.bind('<Configure>' , lambda e: Poster_Canvas.configure(scrollregion= Poster_Canvas.bbox("all") ) )
    Frame_Canvas = Frame(Poster_Canvas)
    Poster_Canvas.create_window( (0,0), window = Frame_Canvas, anchor = "nw" )
    Back_Button = Button(ChoosePoster_Window , text='Back' , font=('Orelega One','16'), command=Back_FromPoster )
    Back_Button.grid( row = 1, pady = 15)
    href = temp['values'][2]
    req = Request('https://www.themoviedb.org/' + href + '/images/posters', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    i = j = 0
    image_anchor = soup.find_all('img')
    for anchor in image_anchor:
        class_image = anchor.get('class')
        loading_image = anchor.get('loading')
        if class_image != ['poster'] or loading_image != 'lazy' :
            continue
        img_url =  anchor.get('src')
        if not img_url:
            continue
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        img_url = urljoin('https://www.themoviedb.org/' + href + '/images/posters', img_url)
        filename = download(img_url, "Images/Movies/current")
        filename = filename.replace('\\','/')
        image_name = filename.split('/')
        filename = Image.open(filename) 
        #filename= filename.resize((94,100), Image.ANTIALIAS)
        filename = ImageTk.PhotoImage( filename )
        posters.append( filename )
        image_name = image_name[3]
        poster_button = Button(Frame_Canvas, image = posters[i+5*j], bd = 0, command=lambda image_name = image_name:download_poster(image_name) )
        poster_button.grid( row = j , column = i )
        poster_buttons.append(poster_button)
        i += 1
        if i == 5:
            j += 1
            i = 0

image_db_name = None

def send_image_name():
    global image_db_name
    return image_db_name

def download_poster(image_name):
    global image_db_name, ChoosePoster_Window
    if tkinter.messagebox.askyesno( "Poster chosen", "Are you sure you chose the right poster?" ):
        download( "https://www.themoviedb.org/t/p/original/" + image_name , "Images/Movies")
        ChoosePoster_Window.withdraw()
        image_db_name = image_name

def disable_event():
    global AddMoviePoster_Window
    AddMoviePoster_Window.withdraw()

def ChooseMovie_Window( ):
    global Frame_AddMoviePoster,AddMoviePoster_Window
    AddMoviePoster_Window = Toplevel( )
    AddMoviePoster_Window.protocol( "WM_DELETE_WINDOW" , disable_event )
    AddMoviePoster_Window.title( "Choose Movie" )
    AddMoviePoster_Window.withdraw()
    Frame_AddMoviePoster = Frame( AddMoviePoster_Window )

def disable_event2():
    global ChoosePoster_Window
    ChoosePoster_Window.withdraw()

def Choose_PosterWindow( ):
    global Frame_ChoosePoster,ChoosePoster_Window
    ChoosePoster_Window = Toplevel( )
    ChoosePoster_Window.protocol( "WM_DELETE_WINDOW" , disable_event2 )
    ChoosePoster_Window.title( "Choose Poster" )
    #ChoosePoster_Window.geometry("1200x850")
    ChoosePoster_Window.withdraw()
    Frame_ChoosePoster = Frame( ChoosePoster_Window )

def Back_FromPoster():
    global AddMoviePoster_Window, ChoosePoster_Window
    ChoosePoster_Window.withdraw()
    AddMoviePoster_Window.deiconify()