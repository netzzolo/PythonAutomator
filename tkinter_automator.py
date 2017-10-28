#!/usr/bin/env python
from Tkinter import *
import ttk, tkFileDialog, time
import threading



def startauto(*args):
    try:
        startb.config(relief=SUNKEN, bg="red", text="Stop", command=stopb)
        # Disable All options
        senario_length_entry.config(state=DISABLED)
        TXon_entry.config(state=DISABLED)
        TXoff_entry.config(state=DISABLED)
        audiobutton.config(state=DISABLED)
        logbutton.config(state=DISABLED)
        # countdown! running in its own thread
        CD_thread.set()

    except ValueError:
        pass


def stopb(*args):
    try:
        startb.config(relief=RAISED, bg="green", text="Start", command=startauto)
        # enable all options
        senario_length_entry.config(state=NORMAL)
        TXon_entry.config(state=NORMAL)
        TXoff_entry.config(state=NORMAL)
        audiobutton.config(state=NORMAL)
        logbutton.config(state=NORMAL)
        CD_thread.clear()

    except ValueError:
        pass


def chooseaudio(*args):
    try:
        audiofileC = tkFileDialog.askopenfilename(initialdir="/", title="Select Audio File",
                                                  filetypes=(("WAV files", "*.wav"), ("All Files", "*.*")))
        audiobutton.config(text="Audio File:")

        print(audiofileC)
        audiofile.set(audiofileC)
    except ValueError:
        pass


def chooselog(*args):
    try:
        logfileC = tkFileDialog.asksaveasfilename(initialdir="/", title="Select Log File", \
                                                  filetypes=(
                                                  ("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All Files", "*.*")))
        logbutton.config(text="Log File:")
        print(logfileC)
        logfile.set(logfileC)
    except ValueError:
        pass


def countdown(i, j, k):
    CD = threading.currentThread()
    while getattr(CD, "do_run", TRUE):

        TxUpC = int(i)
        TxDownC = int(j)+int(i)
        SenLenC = int(float(k)*60)


        while SenLenC > -1:
            #make the minutes and/or seconds pretty
            SLmins, SLsecs = divmod(SenLenC, 60)
            TUmins, TUsecs = divmod(TxUpC, 60)
            TDmins, TDsecs = divmod(TxDownC,60)
            SCtimeformat = '{:02d}:{:02d}'.format(SLmins, SLsecs)
            TUtimeformat = '{:02d}:{:02d}'.format(TUmins, TUsecs)
            TDtimeformat = '{:02d}:{:02d}'.format(TDmins, TDsecs)

            #update the timer block
            Stimer.config(text=SCtimeformat)
            txremain.config(text=TUtimeformat)
            Itimer.config(text=TDtimeformat)

            #Decrement all timers
            SenLenC -= 1
            if TxUpC > 0:
                TxUpC -= 1
            TxDownC -= 1
            print("Down - " + str(TxDownC))
            print("Up - " + str(TxUpC))
            print("Sen - " + str(SenLenC))

            # loop TX up counter and Interval Timer until scenario is finished
            if TxUpC < 1 and TxDownC < 1:
                print("made it")
                TxUpC = int(i)
            if TxDownC < 1:
                TxDownC = int(i)+int(j)

            root.update_idletasks()
            time.sleep(1)

        print("hello")

if __name__=='__main__':


    root = Tk()
    style = ttk.Style()
    root.title("Python Automator")


    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    TXon = StringVar()
    TXoff = StringVar()
    senario_length = StringVar()

    # TX up entry box
    TXon_entry = Entry(mainframe, width=5, textvariable=TXon, justify=CENTER)
    TXon_entry.grid(column=1, row=1, sticky=E)
    ttk.Label(mainframe, text="TX up (s)").grid(column=2, row=1, sticky=W)

    # TX down entry box
    TXoff_entry = Entry(mainframe, width=5, justify=CENTER)
    TXoff_entry.grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="TX down (s)").grid(column=2, row=2, sticky=W)

    # Scenario Length entry box
    senario_length_entry = Entry(mainframe, width=5, justify=CENTER)
    senario_length_entry.grid(column=1, row=3, sticky=E)
    ttk.Label(mainframe, text="Scenario Length (m)").grid(column=2, row=3)

    # Log File Chooser
    logfile = StringVar()
    logbutton = Button(mainframe, text="Choose Log File", command=chooselog)
    logbutton.grid(column=1, row=4, sticky=E)
    ttk.Label(mainframe, textvariable=logfile).grid(column=2, row=4, sticky=(W, E))

    # Audio File Chooser
    audiofile = StringVar()
    audiobutton = Button(mainframe, text="Choose Audio File", command=chooseaudio)
    audiobutton.grid(column=1, row=5, sticky=E)
    ttk.Label(mainframe, textvariable=audiofile).grid(column=2, row=5, sticky=(W, E))

    # Start Button
    startb = Button(mainframe, text="Start", command=startauto, padx=3)
    startb.configure(bg="green")
    startb.grid(column=3, row=1, sticky=W)

    # Timer Watch
    ##TX Remaining
    txremain_Label = Label(mainframe, text="TX Remaining")
    txremain_Label.grid(column=3, row=2, sticky=(W, E))
    txremain = Label(mainframe)
    txremain.grid(column=3, row=3)

    ##Interval Timer
    Itimer_Label = Label(mainframe, text="Interval Timer")
    Itimer_Label.grid(column=3, row=4, sticky=(W, E))
    Itimer = Label(mainframe)
    Itimer.grid(column=3, row=5, sticky=(W, E))

    ##Scenario Timer
    Stimer_Label = Label(mainframe, text="Scenario Remaining")
    Stimer_Label.grid(column=3, row=6, sticky=(W, E))
    Stimer = Label(mainframe)
    Stimer.grid(column=3, row=7, sticky=(W, E))

    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    CD_event = threading.Event()
    CD_thread = threading.Thread(target=countdown(TXon_entry.get(), TXoff_entry.get(), senario_length_entry.get()),
                                 args=(CD_event,))
    CD_thread.start()

    root.mainloop()
