from operator import index
from unicodedata import name
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import pathlib
import re

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
    df = df[df['Calibration Reading'] == 'FALSE']
    return df

# a summary df filtered to only show results that equal positive in the results column
def summary_df_filtered_to_positive(df):
    df = df[df['Result'] == 'Positive']
    return df

# get calibration by filtering the df to show results that equal true in the calibration reading column
def get_calibration_readings(df):
    df = df[df['Calibration Reading'] == 'TRUE']
    return df

def rename_columns(df, column_names):
    df.columns = column_names
    return df

# convert nan to empty string
def convert_nan_to_na(df):
    df = df.fillna('N/A')
    return df


# convert a df to a dict
def convert_df_to_dict(df):
    dict = df.to_dict(orient='records')
    return dict


"""
FUNCTIONS FOR FIELDS NEEDED FOR TEMPLATE
"""

# testing start date - get first value of df column called date and first value of column called time and return a tuple
def get_testing_start_date(df):
    date = df['Date'].iloc[0]
    time = df['Time'].iloc[0]
    return (date, time)

# testing end  date - get last value of df column called date and first value of column called time and return a tuple
def get_testing_end_date(df):
    date = df['Date'].iloc[-1]
    time = df['Time'].iloc[-1]
    return (date, time)

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
    app_version = instrument_type.iloc[4,1]
    info = {'name': name, 'model': model, 'type': type, 'serial': serial}
    return ', '.join(str(key).upper() + ": " + str(value) for key, value in info.items())


# if any positive readings - return true
def is_positive_readings(df):
    if len(summary_df_filtered_to_positive(df).index) > 0:
        return True
    else:
        return False
    


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
    
    
    
    
# get a file save location using tkinter
def get_save_location():
    from tkinter import filedialog
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("html files","*.html"),("all files","*.*")))
    file_path = file_path_to_windows_friendly(file_path)
    return file_path





columns_to_keep = ['Reading #', 'Concentration', 'Result',
       'Component', 'Component2', 'Substrate', 'Side', 'Room', 'Calibration Reading']

"""
DATA PROCESSING (PANDAS)
"""
df = convert_csv_to_df("C:\\Users\\dovid\\OneDrive\\Penguin Group\\first_project\\initial_data.csv")
make_header_row(df, 5)
df = remove_first_rows(df, 6)
df = remove_all_but_columns(df, columns_to_keep)
df = set_df_column_names(df, columns_to_keep)
df = convert_nan_to_na(df)


df = change_column_order(df, ['Room', 'Reading #','Side', 'Component', 'Component2', 'Concentration', 'Substrate', 'Result', 'Calibration Reading'])
df = df.rename(columns={'Reading #': 'Reading No.', 'Concentration': 'Lead (mg/cm2)', 'Result': 'Result', 'Component': 'Component', 'Component2': 'Sub Component', 'Side': 'Wall', 'Room': 'Room', 'Calibration Reading': 'Calibration Reading', 'Substrate': 'Substrate'})



report_df_columns = ['Room', 'Reading No.', 'Lead (mg/cm2)', 'Result', 'Component', 'Sub Component', 'Wall']
report_df = sort_df(df, ['Room', 'Reading No.'])
report_df = remove_all_but_columns(report_df, report_df_columns)


summary_df_columns = ['Reading No.', 'Lead (mg/cm2)', 'Result', 'Component', 'Sub Component', 'Wall', 'Room']
summary_df = summary_df_filtered_to_positive(df)
summary_df = remove_all_but_columns(summary_df, summary_df_columns)
summary_df_dict = convert_df_to_dict(summary_df)

calibration_df_columns = ['Reading No.', 'Lead (mg/cm2)']
calibration_df = get_calibration_readings(df)
calibration_df = remove_all_but_columns(calibration_df, calibration_df_columns)

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
field_df = convert_csv_to_df("C:\\Users\\dovid\\OneDrive\\Penguin Group\\first_project\\initial_data.csv")
clean_df = make_header_row(field_df, 5)
clean_df = remove_first_rows(field_df, 6)
calibration_total = total_num_calibration_tests(clean_df)
without_calibration_df = remove_calibration_readings(clean_df)
start_date = get_testing_start_date(clean_df)
end_date = get_testing_end_date(clean_df)
readings_total = total_number_of_readings(clean_df)
positive_readings = num_positive_readings(clean_df)
instrument_detail = instrument_details(field_df)
results = is_positive_readings(clean_df)

fields = {'start_date': start_date, 'end_date': end_date, 'calibration_total': calibration_total, 'readings_total': readings_total, 'positive_readings': positive_readings, 'instrument_detail': instrument_detail, 'results': results, 'table1': report_df_html, 'table2': summary_df_html, 'table3': calibration_df_html}

dialog_fields = ['location name', 'location address', 'report number']

# FIX THIS 1 - get_user_input function is not working since it doesnt return any values
# user_fields = get_user_input(dialog_fields)
# FIX THIS 1 FAKE PATCH
user_fields = {'location_name': 'test', 'location_address': 'test', 'report_number': 'test'}

tables = {'summary_df': summary_df_dict, 'headings': summary_df_dict[0].keys()}

all_fields = {**user_fields, **fields, **tables}




"""
RENDERING HTML (jinja2)
"""
template_dir = "C:\\Users\\dovid\\OneDrive\\Penguin Group\\first_project"
template = set_up_jinja2_env('template_html.html', template_dir=template_dir)
rendered = template.render(**all_fields)
file_name = 'rendered.html'
save_location = f'C:\\Users\\dovid\\OneDrive\\Penguin Group\\first_project\\app\\{file_name}'
write_html_to_file([rendered, report_df_html, summary_df_html, calibration_df_html], save_location)

merged = merge_html_objects([rendered])

from html2pdf import convert_html_to_pdf

location = "C:\\Users\\dovid\\OneDrive\\Penguin Group\\first_project\\app\\test.pdf"

convert_html_to_pdf(merged, location)
































