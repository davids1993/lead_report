import PySimpleGUI as sg
import sys
from pathlib import Path
import shutil
import re

import json

inspector_names = []
for file in Path('additional_pdfs/inspectors').iterdir():
    if file.suffix == '.pdf':
        inspector_names.append(file.stem)

def read_structures_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_structures_to_file(file_path, structures):
    with open(file_path, 'w') as f:
        json.dump(structures, f)
    

def create_structure_types_window():
    highlight_structures = read_structures_from_file('highlight_structures.json')

    layout = [
        [sg.Listbox(values=highlight_structures, size=(40, 10), key='-STRUCTURE_LIST-')],
        [sg.Text('New Structure', size=(15, 1)), sg.InputText(key='-NEW_STRUCTURE-')],
        [sg.Button('Add Structure', key='-ADD_STRUCTURE-')],
        [sg.Button('Delete Structure', key='-DELETE_STRUCTURE-')],
        [sg.Button('Close')]
    ]

    return sg.Window('Settings', layout)

def create_clients_window():
    clients = read_structures_from_file('clients.json')
    layout = [
        [sg.Listbox(values=clients, size=(40, 10), key='-CLIENT_LIST-')],
        [sg.Text('New Client', size=(15, 1)), sg.InputText(key='-NEW_CLIENT-')],
        [sg.Button('Add Client', key='-ADD_CLIENT-')],
        [sg.Button('Delete Client', key='-DELETE_CLIENT-')],
        [sg.Button('Close')]
    ]

    return sg.Window('Settings', layout)

def create_edit_inspectors_window():
    layout = [
        # list of inspectors 
        [sg.Listbox(values=inspector_names, size=(40, 10), key='-INSPECTOR_LIST-')],
        [sg.Text('Inspector PDF:', size=(15, 1)), sg.Input(key='INSPECTOR_PDF'), sg.FileBrowse(file_types=(('PDF Files', '*.pdf'),), key='PDF_BROWSE')],
        [sg.Text('Change file name (Optional):', size=(15, 1)), sg.InputText(key='-NEW_FILE_NAME-')],
        [sg.Button('Add Inspector', key='-ADD_INSPECTOR-')],
        [sg.Button('Delete Inspector', key='-DELETE_INSPECTOR-')],
        [sg.Button('Close')]
    ]

    return sg.Window('Settings', layout)

def input_window():
    pdf_input_elements = [[sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]]
    


    # Define the layout of the window
    clients = read_structures_from_file('clients.json')
    menu_def = [['Settings', ['Edit Structure Types', 'Edit Clients', 'Edit Inspectors']]]
    layout = [
        [sg.Menu(menu_def)],
        # [sg.Text('Client Name:', size=(15, 1)), sg.InputText(key='CLIENT_NAME')],
        [sg.Text('Client Name:', size=(15, 1)), sg.Combo(clients, size=(25,1), readonly=True, key='CLIENT_NAME')],
        [sg.Text('Inspection Addr.', size=(15, 1)), sg.InputText(key='INSPECTION_ADDRESS')],
        [sg.Text('Unit Number', size=(15, 1)), sg.InputText(key='UNIT_NUMBER')],
        [sg.Text('Inspector', size=(15, 1)), sg.Combo(inspector_names, size=(25, 1), readonly=True, key='INSPECTOR')],
        [sg.Text('CSV Lead Report', size=(15, 1)), sg.Input(key='CSV_LEAD_REPORT'), sg.FileBrowse(file_types=(('CSV Files', '*.csv'),), key='CSV_BROWSE')],
        [sg.Frame(layout=[
            [sg.Text("PDF File", size=(8, 1)), *pdf_input_elements[0]],
        ], title='PDF Files', relief=sg.RELIEF_SUNKEN, key='-PDF_FRAME-')],
        [sg.Button('Add More PDF Files', key='-ADD_MORE_PDFS-')],
        [sg.Text('Save Folder', size=(15, 1)), sg.InputText(key='SAVE_FOLDER'), sg.FolderBrowse(key='FOLDER_BROWSE')],
        [sg.Button('Ok'), sg.Button('Cancel')],
    ]

    sg.theme('BrownBlue')
    window_main = sg.Window('Lead Report', layout, background_color='light grey', icon='icon.ico')

    pdf_file_paths = []
    all_structures = read_structures_from_file('highlight_structures.json')
    


    while True:
        event, values = window_main.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            sys.exit()
        elif event == '-ADD_MORE_PDFS-':
            new_pdf_input = [sg.Input(), sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),))]
            pdf_input_elements.append(new_pdf_input)
            window_main.extend_layout(window_main['-PDF_FRAME-'], [[sg.Text("PDF File", size=(8, 1)), *new_pdf_input]])
        elif event == 'Ok':
            for input_element in pdf_input_elements:
                pdf_path = values[input_element[0].Key]
                if pdf_path and pdf_path.endswith('.pdf'):
                    pdf_file_paths.append(pdf_path)
            user_values = values
            user_values['PDF_PATHS'] = ';'.join(pdf_file_paths)
            break
        elif event == 'Edit Structure Types':
            # Open the structure types settings window
            structure_types_window = create_structure_types_window()
            while True:
                structure_types_event, structure_types_values = structure_types_window.read()
                if structure_types_event in (sg.WIN_CLOSED, 'Close'):
                    structure_types_window.close()
                    break
                elif structure_types_event == '-ADD_STRUCTURE-':
                    new_structure = structure_types_values['-NEW_STRUCTURE-'].strip().lower()
                    if new_structure and new_structure not in all_structures:
                        all_structures.append(new_structure)
                        write_structures_to_file('highlight_structures.json', all_structures)
                        structure_types_window['-STRUCTURE_LIST-'].update(values=all_structures)
                        # clear input field
                        structure_types_window['-NEW_STRUCTURE-'].update('')
                elif structure_types_event == '-DELETE_STRUCTURE-':
                    selected_structures = structure_types_values['-STRUCTURE_LIST-']
                    if selected_structures:
                        all_structures = [structure for structure in all_structures if structure not in selected_structures]
                        write_structures_to_file('highlight_structures.json', all_structures)
                        structure_types_window['-STRUCTURE_LIST-'].update(values=all_structures)
                        # clear input field
                        structure_types_window['-NEW_STRUCTURE-'].update('')
        elif event == 'Edit Clients':
            clients_window = create_clients_window()
            while True: 
                client_event, client_values = clients_window.read()
                if client_event in (sg.WIN_CLOSED, 'Close'):
                    clients_window.close()
                    break
                elif client_event == '-ADD_CLIENT-':
                    new_client = client_values['-NEW_CLIENT-'].strip().title()
                    if new_client and new_client not in clients:
                        clients.append(new_client)
                        write_structures_to_file('clients.json', clients)
                        clients_window['-CLIENT_LIST-'].update(values=clients)
                        # clear input field
                        clients_window['-NEW_CLIENT-'].update('')
                elif client_event == '-DELETE_CLIENT-':
                    selected_clients = client_values['-CLIENT_LIST-']
                    if selected_clients:
                        clients = [client for client in clients if client not in selected_clients]
                        write_structures_to_file('clients.json', clients)
                        clients_window['-CLIENT_LIST-'].update(values=clients)
                        # clear input field
                        clients_window['-NEW_CLIENT-'].update('')
            
        elif event == 'Edit Inspectors':
            inspector_window = create_edit_inspectors_window()
            while True:
                inspector_event, inspector_values = inspector_window.read()
                if inspector_event in (sg.WIN_CLOSED, 'Close'):
                    inspector_window.close()
                    break
                elif inspector_event == '-ADD_INSPECTOR-':
                    pdf_path = inspector_values['INSPECTOR_PDF']
                    if pdf_path and pdf_path.endswith('.pdf'):
                        pdf_file = Path(pdf_path)
                        if inspector_values['-NEW_FILE_NAME-']:
                            new_file_name = inspector_values['-NEW_FILE_NAME-'] + '.pdf'
                        else:
                            new_file_name = pdf_file.name
                        # validate file name follows letters-numbers.pdf format (ex. 'John Doe-1234.pdf')
                        pattern = r'^[a-zA-Z\s]+-\d+\.pdf$'
                        if re.match(pattern, new_file_name):
                            shutil.copy2(pdf_file, Path('additional_pdfs/inspectors') / new_file_name)
                            inspector_names.append(new_file_name)
                            inspector_window['-INSPECTOR_LIST-'].update(values=inspector_names)
                            # clear input fields
                            inspector_window['INSPECTOR_PDF'].update('')
                            inspector_window['-NEW_FILE_NAME-'].update('')
                        else:
                            sg.popup('Invalid file name. It should be in the format [NAME]-[NUM].pdf')
                elif inspector_event == '-DELETE_INSPECTOR-':
                    selected_inspectors = inspector_values['-INSPECTOR_LIST-']
                    if selected_inspectors:
                        for inspector in selected_inspectors:
                            inspector_file = Path('additional_pdfs/inspectors') / (inspector + '.pdf')
                            if inspector_file.exists():
                                inspector_file.unlink()
                        for selected_inspector in selected_inspectors:
                            while selected_inspector in inspector_names:
                                inspector_names.remove(selected_inspector)
                        inspector_window['-INSPECTOR_LIST-'].update(values=inspector_names)
                        # clear input fields
                        inspector_window['INSPECTOR_PDF'].update('')
                        inspector_window['-NEW_FILE_NAME-'].update('')
            

    window_main.close()
    return user_values

def error_message(message, title='Error'):
    sg.popup_error(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')
    sys.exit("Error: " + message)

def warning_message(message, title='Warning'):
    sg.popup(message, title=title, icon='icon.ico', background_color='light grey', text_color='red')


