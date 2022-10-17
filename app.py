import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory, send_file
import pandas as pd
import csv
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import glob
import os
import matplotlib.pyplot as plt
import random
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/files/Results/"
app.config['SECRET_KEY'] = 'supersecretkey'
full_path = os.path.join(app.root_path, 'static/')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# INDEX
@app.route("/", methods=['GET','POST'])
def index():

    font = {'family': 'sans serif',
        'color':  'black',
        'weight': 'bold',
        'size': 12,
        }
    labelfont = {'family': 'sans serif',
        'color':  'black',
        'weight': 'bold',
        'size': 10,
        }
    

    title = "Home"
    form = UploadFileForm()
    data = [0.367,0.957,0.137,0.711,0.231,0.087,0.306,0.058,0.381,0.085,0.249,0.036,0.248,0.038]
    if form.validate_on_submit():
        if os.path.exists('static/Converted.zip'):
            os.remove('static/Converted.zip')
        holder = os.path.dirname("static/files/Results/holder")
        if not os.path.isdir(holder):
                os.makedirs(holder)
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
        # return "File has been uploaded."
        df = pd.read_csv("static/files/Results/data.csv")
        here_dir = os.path.dirname("static/files/Results/holder/")
        data_dir = os.path.join(here_dir, 'Results/')
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        for i in range(len(df)):
            df.loc[i] = df.loc[i] / data
        df.to_csv('static/files/Results/holder/Results/normalised.csv', index=False)
        normdata = pd.read_csv('static/files/Results/holder/Results/normalised.csv')
        # Above works

        for i in range(len(normdata)):
            r = random.random()
            b = random.random()
            g = random.random()
            color = (r, g, b)
            xax = normdata.loc[i]
            y = [1, 10, 100, 1000]

            fig = Figure(figsize=(6,8))
            axis = fig.add_subplot(1, 1, 1)
            axis.set_ylabel('Rock/Chondrite', fontdict=font)
            axis.set_ylim(ymax=1000, ymin=1)
            axis.set_yscale("log")
            axis.set_yticks(y)
            axis.set_yticklabels(['1', '10', '100', '1000'], fontdict=labelfont)
            axis.set_xticklabels(['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'], fontdict=labelfont)
            axis.minorticks_off()
            axis.plot(xax, c=color, linewidth=2.5)

            script_dir = os.path.dirname(__file__)
            fig_dir = os.path.join(data_dir, 'Figures/')
            if not os.path.isdir(fig_dir):
                os.makedirs(fig_dir)
            png = "REE_plot_" + str(i) + ".png"
            svg = "Editable_" + str(i) + ".svg"
            fig.savefig(fig_dir + png, bbox_inches='tight', dpi=300)
            fig.savefig(fig_dir + svg, bbox_inches='tight', dpi=300)
        shutil.make_archive('static/Converted', 'zip', 'static/files/Results/holder')
        shutil.rmtree('static/files/Results/holder')
        os.remove('static/files/Results/data.csv')

        return send_from_directory(full_path,'Converted.zip')
        # Below works
        # return render_template('index.html', shape=df.shape, form=form)
    return render_template('index.html', form=form)


if __name__ == '__app__':
    app.run(debug=True)



# Run the app in powershell
# $env:FLASK_APP = "app.py"
# $env:FLASK_DEBUG = "1"
# flask run 

# For pushing to github
# git add -A
# git commit -m "some text"
# git push


