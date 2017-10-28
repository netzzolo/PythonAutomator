#!/usr/bin/env python
from Tkinter import *
import ttk, tkFileDialog, time
import threading

# globals
running = 1
radionumber =1
radiochoicelist = []
radiochoiceframe =[]
freqentry = []
freqlabel=[]
otherlabel=[]
otherentry=[]
radiochoice = []


def startauto(*args):
    try:
        # set running to 1 so the countdown loop runs
        global running
        running = 1
        print ("start " + str(running))
        # make the start button look like a stop button
        startb.config(relief=SUNKEN, bg="red", text="Stop", command=stopb)
        # Disable All options
        senario_length_entry.config(state=DISABLED)
        TXon_entry.config(state=DISABLED)
        TXoff_entry.config(state=DISABLED)
        audiobutton.config(state=DISABLED)
        logbutton.config(state=DISABLED)
        # countdown! running in its own thread
        CD_thread = threading.Thread(target=countdown,
                                     args=(TXon_entry.get(), TXoff_entry.get(), senario_length_entry.get()))
        CD_thread.start()


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
        # stop the while loop
        global running
        running = 0

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
                                                      ("CSV files", "*.csv"), ("TXT files", "*.txt"),
                                                      ("All Files", "*.*")))
        logbutton.config(text="Log File:")
        print(logfileC)
        logfile.set(logfileC)
    except ValueError:
        pass


def addradio():
    try:
        global radionumber
        global radiochoicelist
        global radiochoiceframe
        global freqentry
        global freqlabel
        global otherentry
        global otherlabel
        global radiochoice

        #remove radio button
        if radionumber ==1:
            minusradio = Button(rf, command=removeradio, text="-")
            minusradio.grid(column=2, row = 1)

        # Radio Dropdown Box
        radioList = ('choice 1', 'choice 2', 'choice 3', 'other')
        radio = StringVar()
        radio.set(radioList[0])
        radiochoiceframe.append(LabelFrame(rf, text="Radio " + str(radionumber), labelanchor='nw'))
        radiochoiceframe[-1].grid(column = 1, row = radionumber+1, sticky = W)
        radiochoicelist.append(OptionMenu(radiochoiceframe[-1], radio, *radioList))
        radiochoicelist[-1].grid()
        freqlabel.append(Label(rf, text="Freq "))
        freqlabel[-1].grid(column=2, row = radionumber+1)
        freqentry.append(Entry(rf, width = 10, justify=CENTER))
        freqentry[-1].grid(column=3, row=radionumber+1)
        radionumber += 1

        # #other box
        # if radiochoicelist[-1].get() == "other":
        #     otherlabel.append(Label(rf, text="Freq "))
        #     otherlabel[-1].grid(column=2, row=radionumber + 1)
        #     otherlabel.append(Entry(rf, width=10, justify=CENTER))
        #     otherlabel[-1].grid(column=3, row=radionumber + 1)

        print("radionumber", radionumber)
        print(radiochoicelist)
        print(radio.get() , 'var is')


    except ValueError:
        pass

def removeradio():
    try:
        global radionumber
        global radiochoicelist
        global radiochoiceframe
        global freqentry
        global freqlabel

        #radiochoicelist.remove(radionumber)
        radiochoiceframe[-1].grid_remove()
        radiochoiceframe.pop()
        radiochoicelist.pop()
        freqentry[-1].grid_remove()
        freqentry.pop()
        freqlabel[-1].grid_remove()
        freqlabel.pop()
        radionumber -= 1
        root.update_idletasks()
        print('radio number' , radionumber)
        print ('rcl' , radiochoicelist)
        print ('rcf' , radiochoiceframe)
    except ValueError:
        pass

def countdown(i, j, k):
    # CD = threading.currentThread()
    # while getattr(CD, "do_run", TRUE):

    TxUpC = int(i)
    TxDownC = int(j) + int(i)
    SenLenC = int(float(k) * 60)
    global running

    while SenLenC > -1 and running == 1:
        # make the minutes and/or seconds pretty
        SLmins, SLsecs = divmod(SenLenC, 60)
        TUmins, TUsecs = divmod(TxUpC, 60)
        TDmins, TDsecs = divmod(TxDownC, 60)
        SCtimeformat = '{:02d}:{:02d}'.format(SLmins, SLsecs)
        TUtimeformat = '{:02d}:{:02d}'.format(TUmins, TUsecs)
        TDtimeformat = '{:02d}:{:02d}'.format(TDmins, TDsecs)

        # update the timer block
        Stimer.config(text=SCtimeformat)
        txremain.config(text=TUtimeformat)
        Itimer.config(text=TDtimeformat)

        # Decrement all timers
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
            TxDownC = int(i) + int(j)

        root.update_idletasks()
        time.sleep(1)

    print("hello")


if __name__ == '__main__':

    root = Tk()
    style = ttk.Style()
    root.title("Python Automator")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # Scenario Frame
    sf = LabelFrame(mainframe, text="Scenario Paramaters:", labelanchor='nw', padx=5, pady=5)
    sf.grid(column=1, row=1, sticky=NW)

    # TX up entry box
    TXon = StringVar()
    TXon_entry = Entry(sf, width=5, textvariable=TXon, justify=CENTER)
    TXon_entry.grid(column=1, row=1, sticky=E)
    ttk.Label(sf, text="TX up (s)").grid(column=2, row=1, sticky=W)

    # TX down entry box
    TXoff = StringVar()
    TXoff_entry = Entry(sf, width=5, justify=CENTER)
    TXoff_entry.grid(column=1, row=2, sticky=E)
    ttk.Label(sf, text="TX down (s)").grid(column=2, row=2, sticky=W)

    # Scenario Length entry box
    senario_length = StringVar()
    senario_length_entry = Entry(sf, width=5, justify=CENTER)
    senario_length_entry.grid(column=1, row=3, sticky=E)
    ttk.Label(sf, text="Scenario Length (m)").grid(column=2, row=3)

    # Log File Chooser
    logfile = StringVar()
    logbutton = Button(mainframe, text="Choose Log File", command=chooselog)
    logbutton.grid(column=1, row=2, sticky=NW)
    ttk.Label(mainframe, textvariable=logfile).grid(column=2, row=4, sticky=(W, E))

    # Audio File Chooser
    audiofile = StringVar()
    audiobutton = Button(mainframe, text="Choose Audio File", command=chooseaudio)
    audiobutton.grid(column=1, row=3, sticky=NW)
    ttk.Label(mainframe, textvariable=audiofile).grid(column=2, row=5, sticky=(W, E))

    # Start Button
    startb = Button(mainframe, text="Start", command=startauto, padx=3)
    startb.configure(bg="green")
    startb.grid(column=1, row=5, sticky=W)

    # Timer Frame
    tf = LabelFrame(mainframe, text="Timers:", labelanchor='nw', padx=5, pady=5)
    tf.grid(column=1, row=4, sticky=NW)

    # Timer Watch
    ##TX Remaining
    txremain_Label = Label(tf, text="TX Remaining")
    txremain_Label.grid(column=1, row=1, sticky=(W))
    txremain = Label(tf)
    txremain.grid(column=1, row=2)

    ##Interval Timer
    Itimer_Label = Label(tf, text="Interval Timer")
    Itimer_Label.grid(column=1, row=3, sticky=(W))
    Itimer = Label(tf)
    Itimer.grid(column=1, row=4, sticky=(W))

    ##Scenario Timer
    Stimer_Label = Label(tf, text="Scenario Remaining")
    Stimer_Label.grid(column=1, row=5, sticky=(W))
    Stimer = Label(tf)
    Stimer.grid(column=1, row=6, sticky=(W))

    # Radio Chooser Frame
    rf = LabelFrame(mainframe, text="Radios:", labelanchor='nw', padx=5, pady=5)
    rf.grid(column=2, row = 1, sticky=N, rowspan = 5)

    # Add Radio Button
    plusradio = Button(rf, command=addradio, text="+")
    plusradio.grid(column=1, row = 1, sticky=N)



    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    root.mainloop()
