import PySimpleGUI as sg
import sys



import PySimpleGUI as sg

def create_settings_window():
    with open('highlight_structures.txt', 'r') as f:
        highlight_structures = [line.strip() for line in f]

    layout = [
        [sg.Listbox(values=highlight_structures, size=(40, 10), key='-STRUCTURE_LIST-')],
        [sg.Text('New Structure', size=(15, 1)), sg.InputText(key='-NEW_STRUCTURE-')],
        [sg.Button('Add Structure', key='-ADD_STRUCTURE-')],
        [sg.Button('Delete Structure', key='-DELETE_STRUCTURE-')],
        [sg.Button('Close')]
    ]

    return sg.Window('Settings', layout)

def input_window():
    # Initialize the list for PDF input elements
    pdf_input_elements = [
        [sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]
    ]
    
    # get inspectors names from file names in additional_pdfs/inspectors
    from pathlib import Path

    inspector_names = []
    for file in Path('additional_pdfs/inspectors').iterdir():
        if file.suffix == '.pdf':
            inspector_name = file.stem
            inspector_names.append(inspector_name)

    # Define the layout of the window
    layout = [
        [sg.Text('Client Name:', size=(15, 1)), sg.InputText()],
        [sg.Text('Inspection Addr.', size=(15, 1)), sg.InputText()],
        [sg.Text('Unit Number', size=(15, 1)), sg.InputText()],
        # [sg.Text('Inspector Name', size=(15, 1)), sg.InputText()],
        #change inspector name to drop down list
        [sg.Text('Inspector', size=(15, 1)), sg.Combo(inspector_names, size=(25, 1), readonly=True)],
        # [sg.Text('Inspector License', size=(15, 1)), sg.InputText()],
        [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
        [sg.Frame(layout=[
            [sg.Text("PDF File", size=(8, 1)), *pdf_input_elements[0]],
        ], title='PDF Files', relief=sg.RELIEF_SUNKEN, key='-PDF_FRAME-')],
        [sg.Button('Add More PDF Files', key='-ADD_MORE_PDFS-')],
        [sg.Text('Save Folder', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
        [sg.Button('Ok'), sg.Button('Cancel')],
    ]

    # Set the theme and create the window
    sg.theme('BrownBlue')
    window = sg.Window('Lead Report', layout, background_color='light grey', icon='icon.ico')

    # Set for storing unique PDF file paths
    pdf_file_paths = []

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sys.exit()
        elif event == '-ADD_MORE_PDFS-':
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
    
# import PySimpleGUI as sg
# import sys
# from pathlib import Path

# def read_structures_from_file(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             return [line.strip() for line in f]
#     except FileNotFoundError:
#         return []

# def write_structures_to_file(file_path, structures):
#     with open(file_path, 'w') as f:
#         for structure in structures:
#             f.write(structure + '\n')

# def create_settings_window():
#     highlight_structures = read_structures_from_file('highlight_structures.txt')

#     layout = [
#         [sg.Listbox(values=highlight_structures, size=(40, 10), key='-STRUCTURE_LIST-')],
#         [sg.Text('New Structure', size=(15, 1)), sg.InputText(key='-NEW_STRUCTURE-')],
#         [sg.Button('Add Structure', key='-ADD_STRUCTURE-')],
#         [sg.Button('Delete Structure', key='-DELETE_STRUCTURE-')],
#         [sg.Button('Close')]
#     ]

#     return sg.Window('Settings', layout)

# def input_window():
#     pdf_input_elements = [[sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]]

#     inspector_names = []
#     for file in Path('additional_pdfs/inspectors').iterdir():
#         if file.suffix == '.pdf':
#             inspector_names.append(file.stem)

#     layout = [
#         [sg.Text('Client Name:', size=(15, 1)), sg.InputText()],
#         [sg.Text('Inspection Addr.', size=(15, 1)), sg.InputText()],
#         [sg.Text('Unit Number', size=(15, 1)), sg.InputText()],
#         [sg.Text('Inspector', size=(15, 1)), sg.Combo(inspector_names, size=(25, 1), readonly=True)],
#         [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),))],
#         [sg.Frame(layout=[
#             [sg.Text("PDF File", size=(8, 1)), *pdf_input_elements[0]],
#         ], title='PDF Files', relief=sg.RELIEF_SUNKEN, key='-PDF_FRAME-')],
#         [sg.Button('Add More PDF Files', key='-ADD_MORE_PDFS-')],
#         [sg.Text('Save Folder', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
#         [sg.Button('Ok'), sg.Button('Cancel')],
#         [sg.Button('Settings')]
#     ]

#     sg.theme('BrownBlue')
#     window_main = sg.Window('Lead Report', layout, background_color='light grey', icon='icon.ico')

#     pdf_file_paths = []

#     while True:
#         event, values = window_main.read()
#         if event in (sg.WIN_CLOSED, 'Cancel'):
#             sys.exit()
#         elif event == '-ADD_MORE_PDFS-':
#             new_pdf_input = [sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]
#             pdf_input_elements.append(new_pdf_input)
#             window_main.extend_layout(window_main['-PDF_FRAME-'], [[sg.Text("PDF File", size=(8, 1)), *new_pdf_input]])
#         elif event == 'Ok':
#             for input_element in pdf_input_elements:
#                 pdf_path = values[input_element[0].Key]
#                 if pdf_path and pdf_path.endswith('.pdf'):
#                     pdf_file_paths.append(pdf_path)
#             user_values = values
#             user_values['PDF_PATHS'] = ';'.join(pdf_file_paths)
#             break
#         elif event == 'Settings':
#             settings_window = create_settings_window()
#             while True:
#                 settings_event, settings_values = settings_window.read()
#                 if settings_event in (sg.WIN_CLOSED, 'Close'):
#                     break
#                 elif settings_event == '-ADD_STRUCTURE-':
#                     new_structure = settings_values['-NEW_STRUCTURE-'].strip()
#                     if new_structure and new_structure not in settings_values['-STRUCTURE_LIST-']:
#                         updated_structures = settings_values['-STRUCTURE_LIST-'] + [new_structure]
#                         settings_window['-STRUCTURE_LIST-'].update(values=updated_structures)
#                         write_structures_to_file('highlight_structures.txt', updated_structures)
#                 elif settings_event == '-DELETE_STRUCTURE-':
#                     selected_structures = settings_values['-STRUCTURE_LIST-']
#                     if selected_structures:
#                         updated_structures = [structure for structure in settings_values['-STRUCTURE_LIST-'] if structure not in selected_structures]
#                         settings_window['-STRUCTURE_LIST-'].update(values=updated_structures)
#                         write_structures_to_file('highlight_structures.txt', updated_structures)
#             settings_window.close()
#     window_main.close()
#     return user_values

# def error_message(message, title='Error'):
#     sg.popup_error(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
#     sys.exit("Error: " + message)

# def warning_message(message, title='Warning'):
#     sg.popup(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')

# if __name__ == "__main__":
#     user_input = input_window()
#     print(user_input)  # Just to demonstrate, you can process the input as needed
