from flask import Flask, render_template, request
import itertools
import os
import filecmp
import pandas as pd
import numpy as np
from main import *


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def sth():
    cwd = os.getcwd()
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', cwd = cwd)
    else:
        path1 = request.form.get('path_1')
        path2 = request.form.get('path_2')
        depth = int(request.form.get('depth_entered'))
        paths_list = [path1, path2]
        df, current_path = run_it(paths_list, depth)
    
        return render_template('index.html', 
                               path__1 = os.listdir(path1), 
                               path__2 = os.listdir(path2),
                               current_path = current_path)