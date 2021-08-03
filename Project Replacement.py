import mysql.connector
from MainMenu import *
from tkinter import *
from tkinter import ttk
from darkmode import *
from Config import *
from PIL import ImageTk,Image
import shutil

# MySQL set-up

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database="entertainment"
)

mycursor = mydb.cursor()

def delete_folder():
  try:
    shutil.rmtree("Images/Movies/current")
    root.destroy()
  except:
    root.destroy()

# root and icon

root = Tk()
root.title("App")
root.iconbitmap("popcorn.ico")
root.protocol( "WM_DELETE_WINDOW" , delete_folder )


# Menu
program_menu = Menu(root)
root.config(menu=program_menu)
file_menu = Menu(program_menu)
program_menu.add_cascade(label="File", menu=file_menu )
file_menu.add_command(label="Dark Mode" , command =lambda:dark_function(root) )
file_menu.add_command(label="Change View Mode" , command =lambda:changeto_images( mycursor, root, Images_List, mydb ) )
file_menu.add_command(label="Settings" , command = Config_Func )
file_menu.add_command(label="Exit", command=root.quit )

# Images

movie_img = ImageTk.PhotoImage( Image.open("clapperboard.png")  )
show_img = ImageTk.PhotoImage( Image.open("tv-show.png")  )
game_img = ImageTk.PhotoImage( Image.open("console.png")  )
book_img = ImageTk.PhotoImage( Image.open("open-book.png")  )
MovieMain_img = ImageTk.PhotoImage( Image.open("best movies2.jpg"))
MovieMainDark_img = ImageTk.PhotoImage( Image.open("best movies dark.jpg"))
starleft_img = ImageTk.PhotoImage( Image.open("star_left.png")  )
starright_img = ImageTk.PhotoImage( Image.open("star_right.png")  )

Images_List = [ movie_img,show_img,game_img,book_img,MovieMain_img,starleft_img,starright_img,MovieMainDark_img ]
#                  0          1       2         3          4            5             6               7

# Movie View Parameters

Frame_MainMenu(root, Images_List, mycursor, mydb)
root.mainloop()