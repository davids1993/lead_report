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



p = pathlib.PurePath(__file__).parent
chdir(p)




"""
TODO:

# calibration number not going into template. - DONE spelling mistake

# change detailed report and summary report sort order to be in the order of the csv don't sort - DONE

# Add numbers to the suammry and detailed reports - DONE

# do some basic error handling
    - missing values in columns cause errors
    - test with many missing values, like cell, or rows
    - check inputs for errors. 
        validate csv
"""


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
    df = df[df['Component'].str.upper() != 'CALIBRATION']
    return df

# a summary df filtered to only show results that equal positive in the results column
def summary_df_filtered_to_positive(df):
    df = df[(df['Result'] == 'Positive') | (df['Result'] == 'Inconclusive')]
    return df

# get calibration by filtering the df to show results that equal true in the calibration reading column
def get_calibration_readings(df):
    df = df[df['Component'].str.upper() == 'CALIBRATION']
    return df

def rename_columns(df, column_names):
    df.columns = column_names
    return df

# convert nan to empty string
def convert_nan_to_na(df):
    df = df.fillna('N/A')
    return df

# add column to df with reading results - positive, negative or inconclusive
# this is calculated based on the value of the Lead (mg/cm2) column.
# if the valu is greater than 0.5 mg/cm2, the result is positive
# if the value is less than 0.5 mg/cm2, the result is negative
# if the value is 0.5 mg/cm2, the result is inconclusive
# def add_result_column(df):
#     df['Result'] = df['Concentration'].apply(lambda x: 'Positive' if x > 0.5 else 'Negative' if x <= 0.4 else 'Inconclusive' if x == 0.5 else 'N/A')
#     df['Result'] = df['Component'].apply(lambda x: 'N/A' if x == 'CALIBRATION' else df['Result'])
#     return df

def add_result_column(df):
    conditions = [
    (df['Concentration'] > 0.5) & (df['Component'].str.upper() != 'CALIBRATION'),
    (df['Concentration'] <= 0.4) & (df['Component'].str.upper() != 'CALIBRATION'),
    (df['Concentration'] == 0.5) & (df['Component'].str.upper() != 'CALIBRATION')
    ]

    
    values = ['Positive', 'Negative', 'Inconclusive']
    df['Result'] = np.select(conditions, values, default='N/A')
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
    name = instrument_type.iloc[0,1]
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
    file_path = pathlib.Path(file_path)
    return file_path

    
            
            
# create a tkinter dialog box to select a csv file
def select_csv_file():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    csv_file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    csv_file = file_path_to_windows_friendly(csv_file)
    return csv_file

import tkinter as tk


# fetch entries and add to dictionary
def fetch(entries):
    values = {}
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        values[field] = text
    return values


def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries


# dialog box to get user input
def get_user_input(fields):
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = tk.Button(root, text='Submit',
            command=(lambda e=ents: fetch(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
    


# get a file save folder location using tkinter
def get_save_folder_location():
    from tkinter import filedialog
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(initialdir = "/",title = "Select folder to save files")
    file_path = file_path_to_windows_friendly(file_path)
    return file_path


# tkinter prompt to select yes or no
def prompt_yes_no(question):
    from tkinter import messagebox
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askyesno("Merge PDFs", question)
    return response


# tkinter dialog box to select multiple pdf file paths
def select_multiple_pdf_files():
    from tkinter import filedialog
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(initialdir = "/",title = "Select files",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    return file_paths


values = input_window()
location_name = values[0]
location_address = values[1]
report_number = values[2]

csv_lead_file = values[3]
csv_lead_file = Path(csv_lead_file)
additional_pdf_files = values[4].split(';')
additional_pdf_files = [Path(file) for file in additional_pdf_files]
save_location = values[5]
save_location = Path(save_location)
branding = values[6]








    
    




columns_to_keep = ['Reading #', 'Concentration',
       'Component', 'Component2', 'Substrate', 'Side', 'Room', 'Room Number', 'Calibration Reading', 'Notes', 'Date', 'Time']

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
# merge room and room number columns then remove room number col
missing_room_df = remove_calibration_readings(df)
if missing_room_df['Room Number'].isnull().values.any():
    warning_message("You are mising some or all numbers in your [Room Number] column. Program will continue..")
    


df['Room Number'] = df['Room Number'].fillna('')
df['Room'] = df['Room'].fillna('N/A')
df["Room"] = df['Room Number'].astype(str) +" "+ df["Room"].astype(str)
df.drop('Room Number', axis=1, inplace=True)


clean_df = df




# create a df with Notes and Room columns
note_df = remove_all_but_columns(df, ['Room', 'Notes'])

# convert note df to a list of tuples
note_data = df_to_list_of_tupples(note_df)

# convert note tupple to dictionary with room name as key and a list as the value with the notes
note_dict = list_of_tuples_to_dict(note_data)


# convert the list of notes into a string
note_dict = dict_list_to_string(note_dict)









df = change_column_order(df, ['Room', 'Reading #','Side', 'Component', 'Component2', 'Concentration', 'Substrate', 'Result', 'Calibration Reading'])
df = df.rename(columns={'Reading #': 'Reading No.', 'Concentration': 'Lead (mg/cm2)', 'Result': 'Result', 'Component': 'Component', 'Component2': 'Sub Component', 'Side': 'Wall', 'Room': 'Room', 'Calibration Reading': 'Calibration Reading', 'Substrate': 'Substrate', 'Date': 'Date', 'Time': 'Time'})


# fill N/A values be carefull they won't cause an error with a later operation like sorting
# I want to be explicit about what I'm doing here with each column
df['Reading No.'] = df['Reading No.'].fillna(0)
df['Lead (mg/cm2)'] = df['Lead (mg/cm2)'].fillna('N/A')
df['Result'] = df['Result'].fillna('N/A')
df['Component'] = df['Component'].fillna('N/A')
df['Sub Component'] = df['Sub Component'].fillna('N/A')
df['Wall'] = df['Wall'].fillna('N/A')
df['Calibration Reading'] = df['Calibration Reading'].fillna('N/A')
df['Substrate'] = df['Substrate'].fillna('N/A')





report_df_columns = ['Room','Reading No.', 'Wall', 'Component', 'Sub Component', 'Substrate', 'Lead (mg/cm2)', 'Result']
report_df = remove_all_but_columns(df, report_df_columns)
report_df = remove_calibration_readings(report_df)
report_df_dict = convert_df_to_dict(report_df)


summary_df_columns = ['Room','Reading No.', 'Wall', 'Component', 'Sub Component', 'Substrate', 'Lead (mg/cm2)', 'Result']
summary_df = summary_df_filtered_to_positive(df)
summary_df = remove_all_but_columns(summary_df, summary_df_columns)
summary_df_dict = convert_df_to_dict(summary_df)

calibration_df_columns = ['Reading No.', 'Lead (mg/cm2)']
calibration_df = get_calibration_readings(df)
calibration_df = remove_all_but_columns(calibration_df, calibration_df_columns)
calibration_df_dict = convert_df_to_dict(calibration_df)


sequential_df_columns = ['Room','Reading No.', 'Wall', 'Component', 'Sub Component', 'Substrate', 'Lead (mg/cm2)', 'Result']
sequential_df = df
sequential_df['Reading No.'] = sequential_df['Reading No.'].astype(int)
sequential_df = sort_df(sequential_df, ['Reading No.'])
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
    warning_message("No calibration tests were found in the file. You may want to check your spelling. The program will continue now..")
    

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

dialog_fields = ['location name', 'location address', 'report number']


user_fields = {'location_name': location_name, 'location_address': location_address, 'report_number': report_number}

tables = {'summary_df': summary_df_dict, 'results_df': report_df_dict, 'sequential_df': sequential_df_dict, 'headings': report_df_dict[0].keys(), 'notes': note_dict, 'branding': branding}

all_fields = {**user_fields, **fields, **tables}




"""
RENDERING HTML (jinja2)
"""
template_dir = Path("./template")
template = set_up_jinja2_env('template_html.html', template_dir=template_dir)
rendered = template.render(**all_fields)
# file_name = 'rendered.html'
# save_location = save_location
# save_location_rendered = f'{save_location}\\{file_name}'
# write_html_to_file([rendered, report_df_html, summary_df_html, calibration_df_html], save_location)

merged = merge_html_objects([rendered])

from html2pdf import convert_html_to_pdf

location = Path(f"{save_location}/lead-report.pdf")


convert_html_to_pdf(merged, location)


# ask user if they want to merge PDF's
# additional = prompt_yes_no('Do you want to add additional PDFs to the report?')

if Path.is_file(additional_pdf_files[0]):
    report_file = file_path_to_windows_friendly(location)

    additional_pdf_files.insert(0, report_file)

    from html2pdf import merge_pdfs

    merge_pdfs(additional_pdf_files, f'{save_location}/Merged-report.pdf')
    
sg.popup_ok('Your Report has sucessfuly been generated!', background_color='light grey', text_color='black', no_titlebar=True, auto_close=True, auto_close_duration=2, title='Success!')
    
    
    































