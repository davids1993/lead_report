from pprint import pp
from unicodedata import name
import PySimpleGUI as sg
import sys


def input_window():
    layout = [  [sg.Text('Location Name:', size=(15, 1)), sg.InputText(),],
                [sg.Text('Location Address', size=(15, 1)), sg.InputText()],
                [sg.Text('Report Number', size=(15, 1)), sg.InputText()],
                [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
                [sg.Text("Additional PDF'S", size=(15, 1)), sg.Input(), sg.FilesBrowse(file_types=(('PDF', '*.pdf'),))],
                [sg.Text('Save Folder', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
                [sg.Checkbox('Branding', default=True)],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
    
    
    sg.theme('BrownBlue')



    window = sg.Window('Lead Report', layout, background_color='dark grey')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        window.close()
        return values
    
    
def error_message(message):
    sg.popup_error(message)
    sys.exit("Error: " + message)
    
    

def warning_message(message):
    sg.popup(message)
    
    

