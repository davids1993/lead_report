import PySimpleGUI as sg
import sys



def input_window():
    layout = [  [sg.Text('Client Name:', size=(15, 1)), sg.InputText(),],
                [sg.Text('Inspection Addr.', size=(15, 1)), sg.InputText()],
                [sg.Text('Unit Number', size=(15, 1)), sg.InputText()],
                [sg.Text('Inspector Name', size=(15, 1)), sg.InputText()],
                [sg.Text('Inspector License', size=(15, 1)), sg.InputText()],
                [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
                        [sg.Frame(layout=[
                [sg.Text("PDF File", size=(8, 1)), sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]],
                title='PDF Files', relief=sg.RELIEF_SUNKEN, key='-PDF_FRAME-')],
                [sg.Button('Add More PDF Files', key='-ADD_MORE-')],
                [sg.Text('Save Folder', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
                [sg.Checkbox('Branding', default=True)],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
    
    
    sg.theme('BrownBlue')



    window = sg.Window('Lead Report', layout, background_color='light grey', icon='icon.ico')

    user_values = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == '-ADD_MORE-':
            window.extend_layout(window['-PDF_FRAME-'], [[sg.Text("PDF File", size=(8, 1)), sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]])
        elif event == 'Ok':
            user_values = values
            break

    window.close()
    return user_values
    
    
def error_message(message, title='Error'):
    sg.popup_error(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
    sys.exit("Error: " + message)
    
    

def warning_message(message, title='Warning'):
    sg.popup(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
    
    

