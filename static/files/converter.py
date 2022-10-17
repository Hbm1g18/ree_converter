import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import figure
import random
import zipfile
import shutil

data = [0.367,0.957,0.137,0.711,0.231,0.087,0.306,0.058,0.381,0.085,0.249,0.036,0.248,0.038]

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

converted_df = pd.DataFrame(columns=['La','Ce','Pr','Nd','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu'])
converted_df.loc[0] = data

user = pd.read_csv("data.csv")

for i in range(len(user)):
    converted_df.loc[i] = user.loc[i]
for i in range(len(converted_df)):
    converted_df.loc[i] = converted_df.loc[i] / data

here_dir = os.path.dirname(__file__)
data_dir = os.path.join(here_dir, 'Results/')
if not os.path.isdir(data_dir):
    os.makedirs(data_dir)
datasheet = "Normalised_Data.csv"
converted_df.to_csv(data_dir + datasheet, index=False, encoding='utf-8-sig')

for i in range(len(converted_df)):
    xax = converted_df.loc[i]
    r = random.random()
    b = random.random()
    g = random.random()
    color = (r, g, b)
    fig, ax = plt.subplots()
    figure1 = figure(figsize=(6,8))
    plot = figure1.add_subplot(1,1,1)
    for axis in ['top','bottom','left','right']:
        plot.spines[axis].set_linewidth(2)
        plot.tick_params(width=2)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    y = [1, 10, 100, 1000]
    plot.set_xlabel('REE', fontdict=font)
    plot.set_ylabel('Rock/Chondrite', fontdict=font)
    plot.set_ylim(ymax=1000, ymin=1)
    plot.set_yticks(y)
    plot.set_yscale("log")
    plot.plot(xax,linestyle='-', c=color, linewidth = 2.5)
    plot.set_yticklabels(['1', '1', '10', '100', '1000'], fontdict=labelfont)
    plot.set_xticklabels(['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'], fontdict=labelfont)
    plot.minorticks_off()
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(data_dir, 'Figures/')
    png = "REE_plot_" + str(i) + ".png"
    svg = "Editable_" + str(i) + ".svg"
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    plt.savefig(results_dir + png, bbox_inches='tight', dpi=300)
    plt.savefig(results_dir + svg, bbox_inches='tight', dpi=300)

zf = zipfile.ZipFile("Results.zip", "w")
for dirname, subdirs, files in os.walk("Results/"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()
shutil.rmtree('Results/')