from Abstract import Abstract, resource_path
import configparser
from PIL import ImageTk,Image


class Books(Abstract):
    def __init__(self,root):
        super().__init__(root)
        if self.root.configparser['Options']['book_view'] == "List":
            self.button_menuView.configure( command = self.view )
        else:
            self.button_menuView.configure( command = self.posters )


    def main_image(self, width, height):
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        theme = self.configparser['Options']['theme']
        if theme == "black" or theme == "equilux":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books black.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "blue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books blue.jpg") ).resize( (width,height) ) )
        elif theme == "alt" or theme == "classic" or theme == "default" or theme == "elegance" or theme == "scidblue" or theme == "scidgreen" \
            or theme == "scidgrey" or theme == "scidmint" or theme == "scidpink" or theme == "scidpurple" or theme == "scidsand":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books alt.jpg") ).resize( (width-4,height-4) ) )
        elif theme == "clam":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books clam.jpg") ).resize( (width,height) ) )
        elif theme == "itft1":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books itft1.jpg") ).resize( (width,height) ) )
        elif theme == "keramik" or theme == "keramik_alt":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books keramik.jpg") ).resize( (width,height) ) )
        elif theme == "kroc":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books kroc.jpg") ).resize( (width,height) ) )
        elif theme == "winxpblue":
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books winxpblue.jpg") ).resize( (width,height) ) )
        else:
            self.img_menu = ImageTk.PhotoImage( Image.open( resource_path("lib/best books.jpg") ).resize( (width-2,height-2) ) )