from tkinter import *
import os.path
import configparser

def disable_eventConfig():
    global Config_Window
    Config_Window.withdraw()

def ConfigWindow( ):
    global Frame_Config,Config_Window
    Config_Window = Toplevel( )
    Config_Window.protocol( "WM_DELETE_WINDOW" , disable_eventConfig )
    Config_Window.title( "Settings" )
    Config_Window.withdraw()
    Frame_Config = Frame( Config_Window )

Darkmode_Config = 1
ViewMode = 'List'
def Config_Func():
    global Darkmode_Config
    ConfigWindow()
    Frame_Config.pack()
    Config_Window.deiconify()
    Label_DarkMode = Label(Frame_Config, text='Darkmode: ' , font=('Orelega One','16') , justify='left' )
    Label_DarkMode.grid( row = 0 , column = 0 , padx = 15 , pady = 10 )
    DarkMode_True = Radiobutton(Frame_Config , text='True' , font=('Orelega One','16') , variable = Darkmode_Config , command=lambda:darkmode_remember(1),value=1, justify='left')
    DarkMode_True.grid( row = 0 , column = 1  , padx = 7 )
    DarkMode_False = Radiobutton(Frame_Config , text='False' , font=('Orelega One','16') ,variable = Darkmode_Config ,command=lambda:darkmode_remember(0),value=0, justify='left')
    DarkMode_False.grid( row = 0 , column = 2 , padx = 7 )
    Label_ViewMode = Label(Frame_Config, text='View Mode: ' , font=('Orelega One','16') , justify='left')
    Label_ViewMode.grid( row = 1 , column = 0 , padx = 15 , pady = 10 )
    ListView = Radiobutton(Frame_Config , text='List' , font=('Orelega One','16') , variable = ViewMode , command=lambda:viewmode_remember('List'),value='List', justify='left')
    ListView.grid( row = 1 , column = 1  , padx = 7 )
    ImagesView = Radiobutton(Frame_Config , text='Images' , font=('Orelega One','16') ,variable = ViewMode ,command=lambda:viewmode_remember('Images'),value='Images', justify='left')
    ImagesView.grid( row = 1 , column = 2 , padx = 7 )


def darkmode_remember( value ):
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    if value == 1:
        config['DEFAULT']['Darkmode'] = 'True'
    else:
        config['DEFAULT']['Darkmode'] = 'False'
    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)

def viewmode_remember( value ):
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    if value == 'List':
        config['DEFAULT']['Viewmode'] = 'List'
    else:
        config['DEFAULT']['Darkmode'] = 'Images'
    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)