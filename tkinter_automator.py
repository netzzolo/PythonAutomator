#!/usr/bin/env python
from Tkinter import *
import ttk, tkFileDialog


def startauto(*args):
    try:
        startb.config(relief=SUNKEN, background="red", text = "Stop")
    except ValueError:

        pass

def chooseaudio(*args):
    try:
        audiofileC = tkFileDialog.askopenfilename(initialdir="/", title="Select Audio File",
                                                filetypes=(("WAV files", "*.wav"), ("All Files", "*.*")))
        print(audiofileC)
        audiofile.set(audiofileC)
    except ValueError:
        pass

def chooselog(*args):
    try:
        logfileC = tkFileDialog.asksaveasfilename(initialdir="/", title="Select Log File",
                                                filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All Files", "*.*")))
        print(logfileC)
        logfile.set(logfileC)
    except ValueError:
        pass

root = Tk()
style=ttk.Style()
root.title("Python Automator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

TXon = StringVar()
TXoff = StringVar()

# TX up entry box
TXon_entry = ttk.Entry(mainframe, width=5, textvariable=TXon).grid(column=1, row=1, sticky=(E))
ttk.Label(mainframe, text="TX up").grid(column=2, row=1, sticky=W)

# TX down entry box
TXoff_entry = ttk.Entry(mainframe, width=5, textvariable=TXoff).grid(column=1, row=2, sticky=(E))
ttk.Label(mainframe, text="TX down").grid(column=2, row=2, sticky=W)

# Scenario Length entry box
senario_length_entry = ttk.Entry(mainframe, width=5, textvariable=TXoff).grid(column=1, row=3, sticky=(E))
ttk.Label(mainframe, text="Scenario Length").grid(column=2, row=3, sticky=W)

# Log File Chooser
logfile = StringVar()
ttk.Label(mainframe, text="Log File:").grid(column=2, row=4, sticky=W)
ttk.Button(mainframe, text="Choose Log File", command=chooselog).grid(column=1, row=4, sticky=E)
ttk.Label(mainframe, textvariable=logfile).grid(column=3, row=4, sticky=(W, E))

# Audio File Chooser
audiofile = StringVar()
ttk.Label(mainframe, text="Audio File:").grid(column=2, row=5, sticky=W)
ttk.Button(mainframe, text="Choose Audio File", command=chooseaudio).grid(column=1, row=5, sticky=E)
ttk.Label(mainframe, textvariable=audiofile).grid(column=3, row=5, sticky=(W, E))

# Start Button
startb = ttk.Button(mainframe, text="Start", command=startauto).grid(column=3, row=1, sticky=W)
#startstyle.configure('TButton', bg='green')



for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
