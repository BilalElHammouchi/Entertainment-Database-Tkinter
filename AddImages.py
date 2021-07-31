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

def Find_MovieImage(Entry_MovieName):
    Movie_Name = Entry_MovieName.get()
    if Movie_Name == '':
        tkinter.messagebox.showerror("Error", "You must include at least the name of the movie!")
        return 0
    MakeEditWindow( )
    global Frame_AddMoviePoster, AddMoviePoster_Window
    AddMoviePoster_Window.deiconify()
    Frame_AddMoviePoster.pack()
    Movie_Name = Movie_Name.replace(" ","+")
    url = "https://www.cinematerial.com/search?q=" + Movie_Name
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    anchor_rows = soup.findAll('a')
    span_rows = soup.findAll('span')
    Frame_tree_select_movie = Frame( Frame_AddMoviePoster )
    Frame_tree_select_movie.grid( row = 0 , columnspan =	5 )
    tree_select_movie = ttk.Treeview( Frame_tree_select_movie , column=("c1","c2") , height = 5 , )
    tree_select_movie.pack(  side = LEFT, fill = BOTH )
    scrollbar_tree_select_movie = Scrollbar( Frame_tree_select_movie )
    scrollbar_tree_select_movie.pack(side = RIGHT, fill = BOTH )
    tree_select_movie.config(yscrollcommand = scrollbar_tree_select_movie.set)
    scrollbar_tree_select_movie.config(command = tree_select_movie.yview)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Treeview', rowheight=100)
    tree_select_movie.heading("#0", text="Icon" )
    tree_select_movie.column("#0", anchor= CENTER , width = 100 )
    tree_select_movie.heading("#1", text="Name" )
    tree_select_movie.column("#1", anchor= CENTER , width = 300 )
    tree_select_movie.heading("#2", text="Year" )
    tree_select_movie.column("#2", anchor= CENTER , width = 100 )
    movies = [ ]
    movie_years = []
    for span in span_rows:
        test = span.get_text()
        test = int(test)
        movie_years.append(test)
    i = 0
    for row in anchor_rows:
        href = row.get('href')
        if href[:7] != '/movies':
            continue
        images = row.find_all("img")
        for image in images:
            img_url = image.attrs.get("src")
            if not img_url:
                continue
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
            main_img = img_url
        if row.get_text().strip():
            movies_placeholder = []
            filename = download( main_img,"Images/Movies/current")
            filename = filename.replace('\\','/')
            icon = ImageTk.PhotoImage( Image.open(filename)  )
            movies_placeholder.append(icon)
            movies_placeholder.append(row.get_text())
            movies_placeholder.append(movie_years[i])
            movies_placeholder.append(href)
            if movies_placeholder != []:
                movies.append(movies_placeholder)
            i += 1
    tree_select_movie.insert('', 'end', image = movies[0][0] , values= (movies[0][1],movies[0][2]) )

def disable_event():
    global AddMoviePoster_Window
    AddMoviePoster_Window.withdraw()

def MakeEditWindow( ):
    global Frame_AddMoviePoster,AddMoviePoster_Window
    AddMoviePoster_Window = Toplevel( )
    AddMoviePoster_Window.protocol( "WM_DELETE_WINDOW" , disable_event )
    AddMoviePoster_Window.title( "Add Poster To Your Movie" )
    AddMoviePoster_Window.withdraw()
    Frame_AddMoviePoster = Frame( AddMoviePoster_Window )