import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import tkinter as tk

objects = ("google","ibm","kaspersky","amazon","facebook","sony","microsoft","apple")
y_pos = np.arange(len(objects))


def get_df_stuff():
    cols = ["a","b","c","d","e","f","g","h"]
    df = pd.read_csv("",header=None,  names=cols,encoding = "UTF-8",low_memory=False)  #path for live sentiment info
    performance = df.values.tolist()                                                      #putting dataframe values to a list of lists for some reason
    flat_list = np.array([int(item) for sublist in performance for item in sublist])    #turning list of list into one list, making list with values to display
    return flat_list

def update_graph():
    ax.axhline(0, color='black')
    mask1 = np.array(get_df_stuff()) < 0
    mask2 = np.array(get_df_stuff()) >= 0
    bars = ax.bar(y_pos[mask1], np.array(get_df_stuff())[mask1], align='center', color='r', width=1, edgecolor="black", linewidth=1,picker=True)
    bars = ax.bar(y_pos[mask2], np.array(get_df_stuff())[mask2], align='center', color='g', width=1, edgecolor="black", linewidth=1,picker=True)
    plt.xticks(y_pos, objects)
    plt.ylim(-100, 100)
    plt.xlim(None, None)
    plt.ylabel('company sentiment (%)')
    plt.title('Real time company sentiment')
    fig.canvas.draw()                                                                     # draw canvas
    for label in ax.get_xticklabels():                                                   # make the xtick labels pickable
        label.set_picker(True)
    win.after(20000, update_graph)                                                        # re run function

def show_deets(company):
    display_info(company)

def clear_widget(widget):
    widget.destroy()

def display_info(company):
    root = tk.Tk()
    new_cols = []
    cols = ["google", "ibm", "kaspersky", "amazon", "facebook", "sony", "microsoft", "apple",
                "google total tweets", "ibm total tweets", "kaspersky total tweets", "amazon total tweets",
                "facebook total tweets", "sony total tweets", "microsoft total tweets", "apple total tweets",
                "google neg tweets", "ibm neg tweets", "kaspersky neg tweets", "amazon neg tweets",
                "facebook neg tweets", "sony neg tweets", "microsoft neg tweets", "apple neg tweets",
                "google pos tweets", "ibm pos tweets", "kaspersky pos tweets", "amazon pos tweets",
                "facebook pos tweets", "sony pos tweets", "microsoft pos tweets", "apple pos tweets",
                "google total tweets w/sec words", "ibm total tweets w/sec words", "kaspersky total tweets w/sec words",
                "amazon total tweets w/sec words", "facebook total tweets w/sec words", "sony total tweets w/sec words",
                "microsoft total tweets w/sec words", "apple total tweets w/sec words",
                "google neg tweets w/sec words", "ibm neg tweets w/sec words", "kaspersky neg tweets w/sec words",
                "amazon neg tweets w/sec words", "facebook neg tweets w/sec words", "sony neg tweets w/sec words",
                "microsoft neg tweets w/sec words", "apple neg tweets w/sec words",
                "google pos tweets w/sec words", "ibm pos tweets w/sec words", "kaspersky pos tweets w/sec words",
                "amazon pos tweets w/sec words", "facebook pos tweets w/sec words", "sony pos tweets w/sec words",
                "microsoft pos tweets w/sec words", "apple pos tweets w/sec words",
                "google sec words #", "ibm sec words", "kaspersky sec words #", "amazon sec words #",
                "facebook sec words #", "sony sec words #", "microsoft sec words #", "apple sec words #",
                "date", "time"]

    for column in cols:
        if column.split()[0] != company:
            new_cols.append(column)

    comp_df = pd.read_csv((""), header=None, names=cols, encoding="UTF-8", low_memory=False) # path for company info
    comp_df = comp_df.drop(columns=new_cols)
    label = tk.Label(root, text=comp_df.iloc[0], font=('Times', '12'), fg='blue')
    lambda: clear_widget(label)
    label.pack()
    root.mainloop()

def onpick1(event):
    if isinstance(event.artist, Line2D):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        print('onpick1 a line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
    elif isinstance(event.artist, Rectangle):
        patch = event.artist
        print('onpick1 b patch:', patch.get_path())
    elif isinstance(event.artist, Text):
        text = event.artist
        show_deets(text.get_text())
        print('onpick1 c text:', text.get_text())

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
win = fig.canvas.manager.window
fig.canvas.mpl_connect('pick_event', onpick1)
win.after(100, update_graph)
plt.show()

