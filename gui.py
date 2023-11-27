import PySimpleGUI as sg
import sys



import PySimpleGUI as sg

def input_window():
    # Initialize the list for PDF input elements
    pdf_input_elements = [
        [sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]
    ]

    # Define the layout of the window
    layout = [
        [sg.Text('Client Name:', size=(15, 1)), sg.InputText()],
        [sg.Text('Inspection Addr.', size=(15, 1)), sg.InputText()],
        [sg.Text('Unit Number', size=(15, 1)), sg.InputText()],
        [sg.Text('Inspector Name', size=(15, 1)), sg.InputText()],
        [sg.Text('Inspector License', size=(15, 1)), sg.InputText()],
        [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
        [sg.Frame(layout=[
            [sg.Text("PDF File", size=(8, 1)), *pdf_input_elements[0]],
        ], title='PDF Files', relief=sg.RELIEF_SUNKEN, key='-PDF_FRAME-')],
        [sg.Button('Add More PDF Files', key='-ADD_MORE-')],
        [sg.Text('Save Folder', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
        [sg.Checkbox('Branding', default=True)],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    # Set the theme and create the window
    sg.theme('BrownBlue')
    window = sg.Window('Lead Report', layout, background_color='light grey', icon='icon.ico')

    # Set for storing unique PDF file paths
    pdf_file_paths = []

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == '-ADD_MORE-':
            # Add a new set of PDF input elements
            new_pdf_input = [sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]
            pdf_input_elements.append(new_pdf_input)
            window.extend_layout(window['-PDF_FRAME-'], [[sg.Text("PDF File", size=(8, 1)), *new_pdf_input]])
        elif event == 'Ok':
            # Iterate over the PDF input elements to collect file paths
            for input_element in pdf_input_elements:
                pdf_path = values[input_element[0].Key]  # Get the value from the Input element
                if pdf_path and pdf_path.endswith('.pdf'):
                    pdf_file_paths.append(pdf_path)
            
            # Store the PDF paths as a single string in user_values
            user_values = values
            user_values['PDF_PATHS'] = ';'.join(pdf_file_paths)
            break

    window.close()
    return user_values

    
    
def error_message(message, title='Error'):
    sg.popup_error(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
    sys.exit("Error: " + message)
    
    

def warning_message(message, title='Warning'):
    sg.popup(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
    
    

