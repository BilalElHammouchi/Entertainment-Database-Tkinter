import math
from tkinter import ttk, CENTER
import tkinter
import os
import sys
import configparser
from tkinter.messagebox import NO
from PIL import ImageTk,Image
from threading import Thread

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class Abstract():
    def __init__(self,root):
        self.root = root
        self.root.frame_mainMenu.pack_forget()
        self.configparser = configparser.ConfigParser()
        self.configparser.read('lib/configuration.ini')
        self.frame_menu = ttk.Frame(self.root)
        self.frame_menu.pack( expand = True, fill = "both" )
        self.main_image(900, 600)
        for i in range(3):
            tkinter.Grid.columnconfigure(self.frame_menu, i, weight = 1 )
        tkinter.Grid.rowconfigure(self.frame_menu, 0, weight = 1 )
        stylelabelcenter = ttk.Style()
        stylelabelcenter.configure( "Kim.TLabel", anchor = "center", bg = "red" )
        self.label_menuImg = ttk.Label(self.frame_menu, style = "Kim.TLabel" )
        self.label_menuImg.grid( row = 0, column = 0, columnspan = 3, sticky = "NSEW" )
        self.button_menuBack = ttk.Button(self.frame_menu, text = "Back" )
        self.button_menuBack.grid( row = 1, column = 0, pady = 10 )
        self.button_menuView = ttk.Button(self.frame_menu, text = "View" )
        self.button_menuView.grid( row = 1, column = 1, pady = 10 )
        self.button_enter = ttk.Button(self.frame_menu, text = "Enter", command = self.enter )
        self.button_enter.grid( row = 1, column = 2, pady = 10 )
        self.sorted_option = "added_time"
        self.label_menuImg.bind('<Configure>' , self.resize_main )
        self.button_menuBack.configure( command = self.menu_toroot)
        self.root.center()


    def main_image(self, width, height):
        pass


    def resize_main(self,e):
        self.main_image( self.label_menuImg.winfo_width(), self.label_menuImg.winfo_height() )
        self.label_menuImg.configure( image = self.img_menu )

    
    def menu_toroot(self):
        self.frame_menu.pack_forget()
        self.root.frame_mainMenu.pack( expand = True, fill = "both" )
        self.root.center()


    def slider_changed(self,e):
        if self.variable_rating.get() < 0.5:
            self.label_ratingValue[ 'text' ] = "0 Stars"
        elif self.variable_rating.get() < 1:
            self.label_ratingValue[ 'text' ] = "0.5 Stars" 
        elif self.variable_rating.get() % math.floor(self.variable_rating.get() ) < 0.5:
            self.label_ratingValue[ 'text' ] = str( math.floor(self.variable_rating.get()) ) + " Stars"
        else:
            self.label_ratingValue[ 'text' ] = str( math.floor(self.variable_rating.get()) + 0.5 ) + " Stars"


    def to_menu(self):
        for child in self.root.winfo_children():
            child.pack_forget()
        """
        if self.root.configparser['Options']['movie_view'] == "List":
            self.button_menuView.configure( command = self.movie_view )
        else:
            self.button_menuView.configure( command = self.movie_posters )
        """
        self.frame_menu.pack( expand = True, fill = "both")
        self.root.center()


    def view(self):
        for child in self.root.winfo_children():
            child.pack_forget()
        self.frame_view = ttk.Frame(self.root)
        self.frame_view.pack( fill = 'both', expand = True )
        self.frame_search = ttk.Frame(self.frame_view )
        self.frame_search.grid( row = 0, column = 0, columnspan = 4, sticky = 'NSEW', pady = 10 )
        for i in range(2):
            tkinter.Grid.columnconfigure(self.frame_search, i, weight = 1 )
        self.var_search = tkinter.StringVar()
        self.entry_search = ttk.Entry(self.frame_search, textvariable = self.var_search )
        self.entry_search.grid( row = 0, column = 0, sticky = "E", padx = 10 )
        self.var_search2 = tkinter.StringVar()
        self.combobox_search = ttk.Combobox(self.frame_search, textvariable = self.var_search2 )
        self.combobox_search.grid( row = 0, column = 1, sticky = "W", padx = 10 )
        self.frame_tree = ttk.Frame(self.frame_view )
        self.frame_tree.grid( row = 1, column = 0, columnspan = 4, sticky = 'NSEW' )
        for i in range(4):
            tkinter.Grid.columnconfigure(self.frame_view, i, weight = 1 )
        tkinter.Grid.rowconfigure(self.frame_view, 1, weight = 1 )
        self.view_tree = ttk.Treeview( self.frame_tree, show='headings' , yscrollcommand = "true" , height = 20 )
        self.view_scrollbar = ttk.Scrollbar( self.view_tree )
        self.view_scrollbar.pack(side = "right", fill = "both" )
        self.view_tree.config(yscrollcommand = self.view_scrollbar.set)
        self.view_scrollbar.config(command = self.view_tree.yview)
        self.var_search.trace_add("write", self.view_search )
        self.var_search2.trace_add("write", self.view_search )
        self.view_tree.pack(  side = "left", fill = "both", expand = True )
        self.button_viewBack = ttk.Button(self.frame_view, text = "Back", command = self.to_menu )
        self.button_viewBack.grid( row = 2, column = 0, pady = 10 )
        self.button_edit = ttk.Button(self.frame_view, text = "Edit", command = lambda: Thread( target = self.edit ).start() )
        self.button_edit.grid( row = 2, column = 1, pady = 10 )
        self.button_delete = ttk.Button(self.frame_view, text = "Delete", command = self.delete )
        self.button_delete.grid( row = 2, column = 2, pady = 10 )
        self.button_posters = ttk.Button(self.frame_view, text = "Posters", command = self.posters )
        self.button_posters.grid( row = 2, column = 3, pady = 10 )
        self.root.center()
        

    def enter(self):
        for child in self.root.winfo_children():
            child.pack_forget()
        self.frame_enter = ttk.Frame(self.root)
        self.frame_enter.pack( fill = 'both', expand = True )
        self.frame_enterBottom = ttk.Frame(self.frame_enter)
        self.frame_enterBottom.pack( fill = 'x', side = 'bottom' )
        self.frame_enterTop = ttk.Frame(self.frame_enter)
        self.frame_enterTop.pack( fill = 'both', expand = True, side = 'top' )
        tkinter.Grid.rowconfigure(self.frame_enterTop, 1, weight = 1 )
        for i in range(2):
            tkinter.Grid.columnconfigure(self.frame_enterTop, i, weight = 1 )
        self.entry_enterSearch = ttk.Entry(self.frame_enterTop, width = 40  )
        self.entry_enterSearch.grid( row = 0, column = 0, pady = 10 )
        self.entry_enterSearch.focus_force()
        self.button_enterSearch = ttk.Button(self.frame_enterTop, text = "Search" )
        self.button_enterSearch.grid( row = 0, column = 1, pady = 10 )
        self.frame_tree = ttk.Frame(self.frame_enterTop )
        self.frame_tree.grid( row = 1, column = 0, columnspan = 2, sticky = 'NSEW' )
        self.tree_select = ttk.Treeview( self.frame_tree, column=("c1","c2","c3", "c4",) , height = 5 , style='Poster.Treeview' ,)
        self.tree_select.pack( expand = True, fill = "both", side = "left" )
        self.select_scrollbar = ttk.Scrollbar( self.frame_tree )
        self.select_scrollbar.pack(side = "right", fill = "both" )
        self.tree_select.config(yscrollcommand = self.select_scrollbar.set)
        self.select_scrollbar.config(command = self.tree_select.yview)
        self.tree_select.column("#0", anchor = CENTER, width = 120, stretch = NO )
        self.tree_select.heading("#0", text = "Poster" )
        self.tree_select.column("#1", anchor = CENTER, width = 250, stretch = NO )
        self.tree_select.heading("#1", text = "Title" )
        self.tree_select.column("#2", anchor = CENTER, width = 150, stretch = NO )
        self.tree_select.heading("#2", text = "Year" )
        self.tree_select.column("#3", anchor= CENTER, width = 450 )
        self.tree_select.heading("#3", text="Description" )
        self.tree_select.column("#4", anchor= CENTER, width = 0, minwidth = 0, stretch = NO )
        tkinter.Grid.columnconfigure(self.frame_enterBottom, 0, weight = 1 )
        frame_buttons = ttk.Frame(self.frame_enterBottom)
        frame_buttons.grid( row = 0, column = 0, pady = 10, sticky = "EW" )
        for i in range(3):
            tkinter.Grid.columnconfigure(frame_buttons, i, weight = 1 )
        self.button_enterBack = ttk.Button(frame_buttons, text = "Back", command = self.enter_tomain )
        self.button_enterBack.grid( row = 0, column = 0 )
        self.button_enterSelect = ttk.Button(frame_buttons, text = "Select" )
        self.button_enterSelect.grid( row = 0, column = 1, pady = 10 )
        self.button_enterManually = ttk.Button(frame_buttons, text = "Enter Manually", command = self.enter_manually )
        self.button_enterManually.grid( row = 0, column = 2, pady = 10 )
        self.root.center()


    def enter_manually(self):
        pass


    def enter_tomain(self):
        self.frame_enter.pack_forget()
        self.frame_menu.pack( expand = True, fill = "both" )
        self.root.center()


    def view_search(self, var, index, mode):
        pass


    def delete(self):
        pass


    def posters(self):
        pass


    def edit(self):
        pass