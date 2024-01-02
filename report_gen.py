from collections import OrderedDict
from os import chdir
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import pathlib
from pathlib import Path
import re
from gui import input_window, error_message, warning_message
import PySimpleGUI as sg
from datetime import date
import numpy as np
import sys
import json
import os



p = pathlib.PurePath(__file__).parent
chdir(p)


"""
DATA PROCESSING FUNCTIONS
"""

#csv file to pandas dataframe
def convert_csv_to_df(csv_file):
    df = pd.read_csv(csv_file)
    return df


# remove the first n rows from df
def remove_first_rows(df, n):
    df = df.iloc[n:]
    return df

# remove all columns beside for specified list of columns
def remove_all_but_columns(df, columns_to_keep):
    df = df[columns_to_keep]
    return df


# change the column order of df
def change_column_order(df, column_order):
    df = df[column_order]
    return df


# make row n in df the header row
def make_header_row(df, n):
    df.columns = df.iloc[n]
    return df

# set df column names from list
def set_df_column_names(df, column_names):
    df.columns = column_names
    return df

# print out the headers of df
def print_headers(df):
    print(df.columns)
    
# sort df by specified colums
def sort_df(df, columns_to_sort_by):
    df = df.sort_values(by=columns_to_sort_by)
    return df

# remove calibration readings from df
def remove_calibration_readings(df):
    df = df[df['Structure'].str.upper() != 'CALIBRATION']
    return df

# a summary df filtered to only show results that equal positive in the results column
def summary_df_filtered_to_positive(df):
    df = df[(df['Result'] == 'Positive') | (df['Result'] == 'Inconclusive')]
    return df

# get calibration by filtering the df to show results that equal true in the calibration reading column
def get_calibration_readings(df):
    df = df[df['Structure'].str.upper() == 'CALIBRATION']
    return df

def rename_columns(df, column_names):
    df.columns = column_names
    return df

# convert nan to empty string
def convert_nan_to_na(df):
    df = df.fillna('N/A')
    return df



def add_result_column(df):
    conditions = [
    (df['Concentration'] > 0.5) & (df['Structure'].str.upper() != 'CALIBRATION'),
    (df['Concentration'] <= 0.4) & (df['Structure'].str.upper() != 'CALIBRATION'),
    (df['Concentration'] == 0.5) & (df['Structure'].str.upper() != 'CALIBRATION')
    ]

    
    values = ['Positive', 'Negative', 'Inconclusive']
    df['Result'] = np.select(conditions, values, default='--')
    return df




"""
VALIDATE DF FUNCTIONS
"""
# test if df contains all required columns and return missing columns
def validate_df_columns(df, required_columns):
    column_headers = list(df.iloc[5])
    missing = []
    for column in required_columns:
        if column not in column_headers:
            missing.append(column)
    if len(missing) == len(required_columns):
        error_message("Missing all required columns. Make sure your column headers start on line 7 of the csv.")
    elif len(missing) > 0:
        error_message('Missing columns: ' + str(missing))
    

    
    
# 

"""
Notes extraction functions
"""
# convert a df to a list of tupples
def df_to_list_of_tupples(df):
    records = df.to_records(index=False)
    return list(records)


# convert a list of 2 item tuples into a dict with key and list of values
def list_of_tuples_to_dict(list_of_tuples):
    notes_dict = {}
    for t in list_of_tuples:
        if t[0] in notes_dict:
            notes_dict[t[0]].append(str(t[1]))
        else:
            notes_dict[t[0]] = [str(t[1])]
            
    return notes_dict


# take a dict of keys and list values and convert the values into a string
def dict_list_to_string(dict):
    for key, value in dict.items():
        dict[key] = ', '.join(str(value) for value in value if value != 'nan')
    return dict
    


# convert a df to a dict
def convert_df_to_dict(df):
    dict = df.to_dict(orient='records', into=OrderedDict)
    return dict


"""
FUNCTIONS FOR FIELDS NEEDED FOR TEMPLATE
"""

# testing start date - get first value of df column called date and first value of column called time and return a tuple
def get_testing_start_date(df):
    # need all this to account for missing values or non date values
    date_frame = pd.DataFrame()
    time_frame = pd.DataFrame()

    date_frame['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    time_frame['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    date_frame = date_frame.dropna()
    time_frame = time_frame.dropna()
    
    # extract just the date and time from the datetime object
    date_frame['Date'] = date_frame['Date'].dt.strftime('%m/%d/%Y')
    time_frame['Time'] = time_frame['Time'].dt.time
    
    min_date = min(date_frame['Date'])
    min_time = min(time_frame['Time'])
    
    return (min_date, min_time)
    
    


# testing end  date - get last value of df column called date and first value of column called time and return a tuple
def get_testing_end_date(df):
    # need all this to account for missing values or non date values
    date_frame = pd.DataFrame()
    time_frame = pd.DataFrame()

    date_frame['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    time_frame['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    date_frame = date_frame.dropna()
    time_frame = time_frame.dropna()
    
    # extract just the date and time from the datetime object
    date_frame['Date'] = date_frame['Date'].dt.strftime('%m/%d/%Y')
    time_frame['Time'] = time_frame['Time'].dt.time
    
    max_date = max(date_frame['Date'])
    max_time = max(time_frame['Time'])

    return (max_date, max_time)


# total number of calibration tests - count number times it sais true in the calibration reading column
def total_num_calibration_tests(df):
    df = get_calibration_readings(df)
    return len(df.index)


# total number of readings - get number of rows in df
def total_number_of_readings(df):
    return len(df.index)


# num positive readings - get number of rows in df where result = positive
def num_positive_readings(df):
    df = summary_df_filtered_to_positive(df)
    return len(df.index)

# instrument type - get from first 5 rows of initial df / uncleaned df
def instrument_details(df):
    instrument_type = df.iloc[0:5]
    name = "Viken " + instrument_type.iloc[0,1]
    model = instrument_type.iloc[1,1]
    type = instrument_type.iloc[2,1]
    serial = instrument_type.iloc[3,1]
    info = {'name': name, 'model': model, 'type': type, 'serial': serial}
    return ', '.join(str(key).upper() + ": " + str(value) for key, value in info.items())


# if any positive readings - return true
def is_positive_readings(df):
    if len(summary_df_filtered_to_positive(df).index) > 0:
        return True
    else:
        return False
    
# summary of df filtered to inconclusive readings
def summary_df_filtered_to_inconclusive(df):
    df = df[df['Result'] == 'Inconclusive']
    return df
    

# number of inconclusive readings - get number of rows in df where result = inconclusive
def num_inconclusive_readings(df):
    df = summary_df_filtered_to_inconclusive(df)
    return len(df.index)
    


"""
HTML GENERATION FUNCTIONS
"""

# regex to add table attributes to html
def add_table_attributes(html):
    html = re.sub(
    r'<table([^>]*)>',
    r'<table\1 repeat="1">',
    html)
    return html
    
    
# return df as html object 
def return_df_as_html(df):
    html = df.to_html(classes='tables', justify='center', index=False)
    html = add_table_attributes(html)
    return html

# write html to file accept a list html objects (can merge HTML objects)
def write_html_to_file(html_list, file_name):
    with open(file_name, 'w') as f:
        for html in html_list:
            f.write(html)

# merge html objects
def merge_html_objects(html_list):
    html = ""
    for html_object in html_list:
        html += html_object
    return html

# set up jinja2 environment
def set_up_jinja2_env(template_file, template_dir):
    file_loader = FileSystemLoader(template_dir)
    env = Environment(loader=file_loader)
    template = env.get_template(template_file)
    return template
            
"""
USER INPUT FUNCTIONS
"""
            
            
# take a file path and make it windows friendly using pathlib
def file_path_to_windows_friendly(file_path):
    #remove new line character
    file_path = str(file_path).replace('\n', '')
    file_path = pathlib.Path(file_path)
    return file_path



values = input_window()
if values is not None:
    client_name = values['CLIENT_NAME']
    inspection_address = values['INSPECTION_ADDRESS']
    unit_number = values['UNIT_NUMBER']
    inspector_file_name = values['INSPECTOR']
    inspector_name, inspector_license = map(str.title, inspector_file_name.split('-'))
    csv_lead_file = Path(values['CSV_LEAD_REPORT'])
    additional_pdf_files = [Path(file) for file in values['PDF_PATHS'].split(';')]
    save_location = Path(values['SAVE_FOLDER'])
else:
    sys.exit("User cancelled operation")


    ##############################################FIX THIS

columns_to_keep = ['Reading #', 'Concentration',
       'Calibration Reading', 'Date', 'Time', 'Room Choice', 'Structure', 'Member', 'Substrate', 'Wall', 'Location', 'Paint Color', 'Paint Condition', 'Notes']

"""
DATA PROCESSING (PANDAS)
"""
# file_path = select_csv_file()
file_path = csv_lead_file
df = convert_csv_to_df(file_path)
validate_df_columns(df, columns_to_keep)
make_header_row(df, 5)
df = remove_first_rows(df, 6)
df = remove_all_but_columns(df, columns_to_keep)
df = set_df_column_names(df, columns_to_keep)
df['Concentration'] = df['Concentration'].astype(float)
df = add_result_column(df)


clean_df = df




# create a df with Notes and Room columns
note_df = remove_all_but_columns(df, ['Room Choice', 'Notes'])

# convert note df to a list of tuples
note_data = df_to_list_of_tupples(note_df)

# convert note tupple to dictionary with room name as key and a list as the value with the notes
note_dict = list_of_tuples_to_dict(note_data)


# convert the list of notes into a string
note_dict = dict_list_to_string(note_dict)


# fill N/A values be carefull they won't cause an error with a later operation like sorting
# I want to be explicit about what I'm doing here with each column
df['Reading #'] = df['Reading #'].fillna(0)
df['Room Choice'] = df['Room Choice'].fillna('--')
df['Structure'] = df['Structure'].fillna('--')
df['Member'] = df['Member'].fillna('--')
df['Substrate'] = df['Substrate'].fillna('--')
df['Wall'] = df['Wall'].fillna('--')
df['Location'] = df['Location'].fillna('--')
df['Paint Color'] = df['Paint Color'].fillna('--')
df['Paint Condition'] = df['Paint Condition'].fillna('--')
df['Concentration'] = df['Concentration'].fillna('--')
df['Result'] = df['Result'].fillna('--')


# df = change_column_order(df, ['Room', 'Reading #','Side', 'Component', 'Component2', 'Concentration', 'Substrate', 'Result', 'Calibration Reading'])
df = change_column_order(df, ['Reading #', 'Result', 'Room Choice', 'Structure', 'Member', 'Substrate', 'Wall', 'Location', 'Paint Color', 'Paint Condition', 'Concentration'])
# df = df.rename(columns={'Reading #': 'Reading No.', 'Concentration': 'Lead (mg/cm2)', 'Result': 'Result', 'Component': 'Component', 'Component2': 'Sub Component', 'Side': 'Wall', 'Room': 'Room', 'Calibration Reading': 'Calibration Reading', 'Substrate': 'Substrate', 'Date': 'Date', 'Time': 'Time'})
df = df.rename(columns={
 'Reading #': 'Read #',
 'Room Choice': 'Room Choice',
 'Structure': 'Structure',
 'Member': 'Member',
 'Substrate': 'Substrate',
 'Wall': 'Wall',
 'Location': 'Location',
 'Paint Color': 'Color',
 'Paint Condition': 'Condition',
 'Concentration': 'Lead (mg/cm2)',
 'Result': 'Result'
})



report_df_columns = ['Read #', 'Room Choice', 'Structure', 'Member', 'Substrate', 'Wall', 'Location', 'Color', 'Condition', 'Lead (mg/cm2)', 'Result']
report_df = remove_all_but_columns(df, report_df_columns)
report_df = remove_calibration_readings(report_df)
report_df_dict = convert_df_to_dict(report_df)


summary_df_columns = ['Read #', 'Room Choice', 'Structure', 'Member', 'Substrate', 'Wall', 'Location', 'Color', 'Condition', 'Lead (mg/cm2)', 'Result']
summary_df = summary_df_filtered_to_positive(df)
summary_df = remove_all_but_columns(summary_df, summary_df_columns)
summary_df_dict = convert_df_to_dict(summary_df)

calibration_df_columns = ['Read #', 'Lead (mg/cm2)']
calibration_df = get_calibration_readings(df)
calibration_df = remove_all_but_columns(calibration_df, calibration_df_columns)
calibration_df_dict = convert_df_to_dict(calibration_df)


sequential_df_columns = ['Read #', 'Room Choice', 'Structure', 'Member', 'Substrate', 'Wall', 'Location', 'Color', 'Condition', 'Lead (mg/cm2)', 'Result']
sequential_df = df
sequential_df['Read #'] = sequential_df['Read #'].astype(int)
sequential_df = sort_df(sequential_df, ['Read #'])
sequential_df = remove_all_but_columns(sequential_df, sequential_df_columns)
sequential_df_dict = convert_df_to_dict(sequential_df)

report_df_html = return_df_as_html(report_df)
summary_df_html = return_df_as_html(summary_df)
calibration_df_html = return_df_as_html(calibration_df)




"""
GET FIELDS TO NEEDED FOR RENDERING

testing start date - get first value of df date and time column
testing end date - get last value of df date and time column
location name - get from input dialog box
location address - get from input dialog box
all calibration tests succeeded - (?not sure where this data is reported?)
total number of calibration tests - get number of rows in calibration df
total number of readings - get number of rows in df
positive readings - get number of rows in df where result = positive
report number - get from input dialog box
instrument type - get from first 5 rows of initial df
report results (lead based paint presant or not) - if any positive readings, report yes, otherwise report no
calibration readings (reading number, reading value) - get from calibration df

"""
field_df = convert_csv_to_df(file_path)
# clean_df = make_header_row(field_df, 5)
# clean_df = remove_first_rows(field_df, 6)
calibration_total = total_num_calibration_tests(clean_df)


if calibration_total == 0:
    warning_message("No calibration tests were found in the file. You may want to check your spelling. The program will continue..")
    

without_calibration_df = remove_calibration_readings(clean_df)
start_date = get_testing_start_date(clean_df)
end_date = get_testing_end_date(clean_df)
readings_total = total_number_of_readings(clean_df)
positive_readings = num_positive_readings(clean_df)
inconlusive_readings = num_inconclusive_readings(clean_df)
instrument_detail = instrument_details(field_df)
results = is_positive_readings(clean_df)


if results == True:
    results = 'Positive'
else:
    results = 'Negative'

fields = {'start_date': start_date, 'end_date': end_date, 'calibration_total': calibration_total, 'readings_total': readings_total, 'positive_readings': positive_readings, 'inconlusive_readings': inconlusive_readings, 'instrument_detail': instrument_detail, 'results': results, 'calibrations': calibration_df_dict, 'report_date': date.today().strftime('%m/%d/%Y')}

# dialog_fields = ['location name', 'inspection address', 'report number']

# load json file with highlighted structures
with open('highlight_structures.json') as f:
    highlight_structures = json.load(f)

user_fields = {'client_name': client_name, 'inspection_address': inspection_address, 'unit_number': unit_number, 'inspector_name': inspector_name, 'inspector_license': inspector_license, 'highlight_structures': highlight_structures}

tables = {'summary_df': summary_df_dict, 'results_df': report_df_dict, 'sequential_df': sequential_df_dict, 'headings': report_df_dict[0].keys(), 'notes': note_dict}

all_fields = {**user_fields, **fields, **tables}




"""
RENDERING HTML (jinja2)
"""
template_dir = Path("./template")
template = set_up_jinja2_env('template_html.html', template_dir=template_dir)
rendered = template.render(**all_fields)

# write html to file
write_html_to_file([rendered], f'{save_location}/lead-report.html')

merged = merge_html_objects([rendered])

from html2pdf import convert_html_to_pdf

location = Path(f"{save_location}/{inspection_address}, {unit_number} - XRF Inspection Report.pdf")



convert_html_to_pdf(merged, location)


# ask user if they want to merge PDF's
# additional = prompt_yes_no('Do you want to add additional PDFs to the report?')

#path to generated report pdf file
report_file = file_path_to_windows_friendly(location)


#add additional pdf files to list
if Path.is_file(additional_pdf_files[0]):
    additional_pdf_files.insert(0, report_file)
else:
    additional_pdf_files = [report_file]
    
# get base dir to executable (if running as pyinstaller executable)
def get_base_path():
    # Check if the app is running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # If it's a bundle, use the executable's directory
        return os.path.dirname(sys.executable)
    else:
        # If it's not a bundle, use the script's directory
        return os.path.dirname(__file__)

base_path = get_base_path()
#add report cover
additional_pdf_files.insert(0, Path('./other_pdfs/cover.pdf'))

#add final page
# additional_pdf_files.append(Path('./additional_pdfs/inspectors/' + inspector_file_name + '.pdf'))
additional_pdf_files.append(Path(base_path + '/additional_pdfs/inspectors/' + inspector_file_name + '.pdf'))
# add company license as final page
additional_pdf_files.append(Path(base_path + '/other_pdfs/license.pdf'))

from html2pdf import merge_pdfs

merge_pdfs(additional_pdf_files, f"{save_location}/{inspection_address}, {unit_number} - XRF Inspection Report.pdf")

    
sg.popup_ok('Your Report has sucessfuly been generated!', background_color='light grey', text_color='black', auto_close=True, auto_close_duration=2, title='Success!')
    
    
    































