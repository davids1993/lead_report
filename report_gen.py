from jinja2 import Environment, PackageLoader, select_autoescape
import jinja2
import pandas as pd
from regex import P

"""
DATA PROCESSING FUNCTIONS
"""

#csv file to pandas dataframe
def convert_csv_to_df(csv_file):
    df = pd.read_csv(csv_file)
    return df


# remove the first N rows from df
def remove_first_rows(df, n):
    df = df.iloc[n:]
    return df

# remove all columns beside for specified list of columns
def remove_all_but_columns(df, columns_to_keep):
    df = df[columns_to_keep]
    return df


# make row n in df the header row
def make_header_row(df, n):
    df.columns = df.iloc[n]
    return df

# print out the headers of df
def print_headers(df):
    print(df.columns)
    
# sort df by specified colums
def sort_df(df, columns_to_sort_by):
    df = df.sort_values(by=columns_to_sort_by)
    return df

# color the df row red if the value states "Positive"
def color_red_if_positive(df):
    df.style.applymap(lambda x: 'background-color: red' if x == 'Positive' else 'background-color: white')
    return df

"""
HTML GENERATION FUNCTIONS
"""
    
    
# return df as html object 
def return_df_as_html(df):
    html = df.to_html()
    return html

# write html to file accept a list html objects
def write_html_to_file(html_list, file_name):
    with open(file_name, 'w') as f:
        for html in html_list:
            f.write(html)
            
# create a jinja2 environment
def create_jinja2_environment():
    env = Environment(
        loader=PackageLoader('report_gen', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env


# create a jinja2 template
def create_jinja2_template(env, template_name):
    template = env.get_template(template_name)
    return template


# fill in the template with the data 
def fill_template(template, data):
    html = template.render(data)
    return html
            
"""
USER INPUT FUNCTIONS
"""
            
            
# take a file path and make it windows friendly using pathlib
def file_path_to_windows_friendly(file_path):
    import pathlib
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
    print(values)
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
       'Component', 'Component2', 'Side', 'Room']

# df = convert_csv_to_df("C:\\Users\\dovid\\OneDrive\\Penguin Group\\First Project\\initial_data.csv")
# make_header_row(df, 5)
# df = remove_first_rows(df, 6)
# df = remove_all_but_columns(df, columns_to_keep)
# df = sort_df(df, ['Room', 'Reading #'])
# df = color_red_if_positive(df)
# a = return_df_as_html(df)
# b = return_df_as_html(df)

# write_html_to_file([a,b], "C:\\Users\\dovid\\OneDrive\\Penguin Group\\First Project\\report.html")

# fields = ['company', 'project ID', 'date', 'location']

# env = create_jinja2_environment()
# template = create_jinja2_template(env, "C:\\Users\\dovid\\OneDrive\\Penguin Group\\First Project\\templates\\template_a.html")

# data = {'date': '2019-01-01'}
# template = fill_template(template, data)
# print(template)


print(get_save_location())





















