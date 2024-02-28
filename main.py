### fileSearch Version 0.1 ###
### This code searches for same files in given directories ###
### and produces a csv file with the list of duplicates ###

import itertools
import os
import filecmp
import pandas as pd
import numpy as np

def print_it(parameter):
    print(parameter)

def compare_them(f1, f2):
    return filecmp.cmp(f1, f2, shallow=False)

def run_it(paths_list, depth):
    files = {}   # This dictionary will keep a log of all files and their locations
    for initial_path in paths_list:
        dir_list = [initial_path]     # This is where the logging will start, one of the two in paths_list
        for depth_ in range(depth):
            new_dir_list = []      # This list will contain every subdirectory in every directory(path) in dir_list
            for path in dir_list:
                subdir = [os.path.join(path, x) for x in os.listdir(path) if (os.path.isdir(os.path.join(path, x)))
                        & (not x.startswith('.'))]
                subfile = [x for x in os.listdir(path) if (os.path.isfile(os.path.join(path, x)))
                        & (not x.startswith('.'))]
                new_dir_list.extend(subdir)     # The subdirectories under the current path are added to new_dir_list
                
                for file in subfile:    # All the files under the path are added to the files dictionary together with their paths
                    if file in files.keys():
                        files[file].append(path)   # If the file is already in the dictionary, append its path to list of other paths
                    else:
                        files[file] = [path]       # If the file is not in the dictionary, add it

            dir_list = new_dir_list.copy()    # The new dir_list is new_dir_list. This is repeated as many as the depth variable

    df = into_df(files, paths_list)    # The dictionary is converted into a dataframe
    current_path = os.getcwd()
    df.sort_values(['how_many_times', 'file_name', 'path'], ascending=[False, True, False]).to_csv('output.csv', 
                                                                                               index=False)
    
    return df, current_path

def into_df(files, paths_list):
    df = pd.DataFrame(columns=['file_name', 'path', 'how_many_times', 'same_name', 'all_same_content', 
                               'initial_path'])
    for key, value in files.items():
        num = len(value)    # An entry in the dictionary may have a single or more more entries. That value is num
        if num == 1:      # If there is a single entry, just add it to the df after finding its initial path
            if value[0].startswith(paths_list[0]):
                initial_path = paths_list[0]
            else:
                initial_path = paths_list[1]
            df.loc[len(df)] = [key, value[0], num, np.nan, np.nan, initial_path]
        else:
            combinations = list(itertools.combinations(value, 2))  # Make a list of all 2 value combinations of all locations
            all_same_content = True
            for comb in combinations:  # For every 2 value combinations, check if they are the same file using the custom compare_them function
                all_same_content = all_same_content & compare_them(os.path.join(comb[0], key),
                                                                   os.path.join(comb[1], key))
                if not all_same_content:    # If any combination is not the same, break the loop
                    break
            for i in range(num):
                if value[i].startswith(paths_list[0]):   # Determine the inital path, one of two, of the file
                    initial_path = paths_list[0]
                else:
                    initial_path = paths_list[1]
                df.loc[len(df)] = [key, value[i], num, True, all_same_content, initial_path]  # add an entry to the end of the df
    return df