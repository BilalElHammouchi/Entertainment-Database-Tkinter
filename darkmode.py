from Movies_Functions import *
from MainMenu import *
import os.path
import configparser

config = configparser.ConfigParser()
config.read('configuration.ini')
if os.path.isfile("configuration.ini"):
    if config['DEFAULT']['darkmode'] == 'True':
        dark_modeRoot = True
    else:
        dark_modeRoot = False
else:
    config['DEFAULT'] = {'Darkmode': 'True'}
    with open('configuration.ini', 'w') as configfile:
        config.write(configfile)


def dark_function( root ):
    global dark_modeRoot
    darkMovies_function( )    
    darkMenu_function()
    if dark_modeRoot is False:
        root.configure( bg= '#1F1B24' )
        dark_modeRoot = True
    else:
        root.configure( bg= '#F0F0F0' )
        dark_modeRoot = False