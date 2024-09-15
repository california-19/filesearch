### fileSearch Version 0.3 ###
### This code searches for same files in given directories ###
### and produces a csv file with the list of duplicates ###

import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import numpy as np
from functions import *

root = tk.Tk()
root.title('fileSearch, Search your duplicate files with ease!')
root.geometry("800x600")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

path_entry1 = tk.StringVar()
path_entry2 = tk.StringVar()
depth_entry = tk.StringVar()

frame_1 = ttk.Frame(root)
frame_1.grid(row=0, column=0)

frame_1.columnconfigure(0, weight=1)
frame_1.rowconfigure(1, weight=1)

frame_2 = ttk.Frame(root)
frame_2.grid(row=1, column=0)

frame_2.columnconfigure(0, weight=1)
frame_2.rowconfigure(1, weight=1)

text_intro = 'INTRO: This program finds duplicate files in the two directories provided. It finds duplicates \
within each directory and in between them. The output file is saved to the folder below.\n \
This program does NOT delete or move any files. It does NOT collect any information. The source code is\
open to anyone at https://github.com/california-19/filesearch to verify this.'
text_instructions = 'INSTRUCTIONS: Edit the first and second paths, starting folders to search, below.'
label_intro = tk.Label(frame_1, text = text_intro, wraplength=400, justify='left', width=50, height=5, padx=10, pady=10)
label_intro.grid(row=0, column=1, sticky='nsew')
label_instructions = tk.Label(frame_1, text = text_instructions, wraplength=400, justify='left', width=50, height=4, padx=10, pady=10)
label_instructions.grid(row=1, column=1, sticky='nsew')
text_cwd = tk.Text(frame_1, width=50, height=3, padx=10, pady=10)
text_cwd.insert(tk.END, os.getcwd())
text_cwd.grid(row=2, column=1, sticky='ew')

entry_1 = ttk.Entry(frame_2, textvariable = path_entry1)
entry_1.insert(tk.END, os.getcwd())
entry_1.grid(row=2, column=1, sticky='ew')
entry_2 = ttk.Entry(frame_2, textvariable=path_entry2)
entry_2.insert(tk.END, os.getcwd())
entry_2.grid(row=3, column=1, sticky='ew')
entry_depth = ttk.Entry(frame_2, textvariable=depth_entry)
entry_depth.insert(tk.END, 5)
entry_depth.grid(row=4, column=1, sticky='ew')

label_1 = ttk.Label(frame_2, text='Edit the first path to search:').grid(row=2, column=0, sticky='ew')
label_2 = ttk.Label(frame_2, text='Edit the second path to search:').grid(row=3, column=0, sticky='ew')
label_depth = ttk.Label(frame_2, text='Edit the depth of search, a number between 1 and 100:').grid(row=4, column=0, sticky='ew')

def on_click():
    path1 = path_entry1.get()
    path2 = path_entry2.get()
    depth = depth_entry.get()

    paths_list = [path1, path2]
    df, current_path = run_it(paths_list, int(depth))

    print(df.head())
    print(current_path)
    label_df.config(text=f'Your output file is saved at {current_path}')

btn_run = ttk.Button(frame_2, text='Run it', command=on_click).grid(row=5, column=1)
label_df = ttk.Label(frame_2, text = 'Your output file is being prepared').grid(row=6, column=0, columnspan=2, sticky='ew')

root.mainloop()