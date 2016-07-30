import sys
import shutil   # to copy files
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import json

from excel_reader import read_excel
from save_a_pdf import GetSave
"""
empty page fix implemented, check if it works ---- check file for info
"""
from settings import Settings





"""
main menu file with class structure

TO DO
    - load settings at startup
        DONE - main directory path
        DONE - dict dossier folders

    - move backup files /
        -renaming/copy to specific paths

    -settings menu
        - storing settings with json when 'ok' is pressed
        DONE - create scan option for dossier folders

    -dossier reference nr (user input)
        DONE - auto locate *.xls file by user input and get excel data
                 DONE - create dossier folder path
                 DONE - find *.xls file in dossier map
    -create pdf save path, append "//Stabiliteit//Plannen pdf"
                to dossier path


ISSUES
    DONE - settings reset when reopening settings menu after pressing ok
             ONLY happens after reload program after pressin ok in settings

               need to load settings and put them into the variables outside classes
               because not manually selecting means saving empty settings

    - UPDATE DOSSIERS
        - does not remove dossier when map is removed
"""

'''The point of a computer is ....
... To do repetitive tasks for you. If you find yourself copy and pasteing
code 13 times, you are doing the computer's job!'''

LARGE_FONT= ("Verdana", 12)


main_settings = {
    "directory":""
    }

folder_scan = {
    }



class CADapp(tk.Frame, Settings):
    def __init__(self, master): # only runs one time at startup
        tk.Frame.__init__(self, master)
        self.master = master
        #----------------
        #add menu bar
        """?    how class already being called"""
        menubar = Menu(self)
        master.config(menu=menubar)
        #----------------
        self.frames = {}                            # multiple windows
        for window in [StartPage]:                  # list of windows
            frame = window(self)                    # startpage = initial window
            self.frames[window] = frame
            frame.grid(row= 0, column= 0, sticky="nsew", padx=5,pady=5)
        self.show_frame(StartPage)                  # show starting frame

        self.loading()

    def loading(self):
        print("loading settings/folders *.txt")
        mains, folder_s = self.loader()             # returns a tuple, from settings.py

        for item in mains:
            main_settings[item] = mains[item]
        for item in folder_s:
            folder_scan[item] = folder_s[item]


    def show_frame(self, cont):
        print("initialising page(frame)")
        frame = self.frames[cont]
        frame.tkraise()

    def selecting(self, dossier=None):
        print("get data from *.xls")
        #gets data from *.xls
        the_dict = read_excel(dossier)              #imported method from excel_reader.py, returns the_dictionary
        """?    """
        #adds dossier number from entry
        the_dict['dossier_nummer'] = self.dossier.get()
        page = self.master.frames[StartPage]        #!!!!!!!!!!!!!!!!!!!!!!
        page.renew_entry_data(the_dict)
        print(the_dict)

"""--------------------menu--------------------"""

class Menu(tk.Menu):
    def __init__(self, master):
        print("initiate menu")
        tk.Menu.__init__(self, master)
        filemenu = tk.Menu(self, tearoff = 0)
        #filemenu.add_command(label="select file", command=master.selecting)
        filemenu.add_command(label="settings", command=lambda: Dialog(master))
        """?    somehow works"""
        filemenu.add_command(label="save pdf", command=lambda: self.master.frames[StartPage].save_pdf())  #better call for this???
        filemenu.add_separator()    #adding divider
        filemenu.add_command(label="exit", command = quit)
        #add filemenu to menubar
        self.add_cascade(label="File", menu=filemenu)




"""--------------------adding pages--------------------"""

# Having the fields in a single list with a single name scheme will
# make editing the fields a lot easier.
FIELDS = [
    "bouwheer",
    "werfadres",
    "werfgemeente",
    "woning straat",
    "woning gemeente",
    "architect",
    "architect straat",
    "architect gemeente",
    "aannemer",
    "aannemer straat",
    "aannemer gemeente",
    "ingenieur"]

CAPS_TEMPLATE = """\
{0[bouwheer]}
{0[werfadres]}

{0[werfgemeente]}
{0[woning straat]}
{0[woning gemeente]}

{0[architect]}
{0[architect straat]}
{0[architect gemeente]}
{0[aannemer]}

{0[aannemer straat]}
{0[aannemer gemeente]}

{0[ingenieur]}"""



class StartPage(CADapp, tk.Frame, Settings):

    def __init__(self, parent):
        print("initiate StartPage")
        tk.Frame.__init__(self, parent)                 #parent class = CADapp
        self.parent = parent
        self.initialise()
        self.body_buttons()

    def initialise(self):
        """?    remove back to self ----?? test for ridge on frame"""
        box_entries = tk.Frame(self, bd=4, relief = 'ridge')
        self.values = {}
        for row, field in enumerate(FIELDS, start=3):
            label = tk.Label(box_entries, text=field, font=LARGE_FONT)
            label.grid(row=row,column=0, sticky=tk.W, padx=5,pady=5)
            entry = tk.Entry(box_entries, width = 60)   #an Entry widget does not require a StringVar, and it does not help you any
            entry.grid(row=row, column = 1)
            self.values[field] = entry
        #create text widget for CAPS convertor
        self.caps = tk.Text(box_entries, width= 60)
        self.caps.grid(row= 3, column= 2, rowspan = 15, padx=5,pady=5)
        box_entries.grid(row = 3, column = 0, padx=5, pady=5)

    def body_buttons(self):
        box_buttons = tk.Frame(self)
        box_info = tk.Frame(self, bd=4, relief = 'ridge')
        #create dossier reference label
        label = tk.Label(box_info, text= "Dossier:" ,justify= "center", font= LARGE_FONT, relief= "groove")
        label.grid(row=1,column=0, sticky=tk.W, padx=5,pady=5)
        #create dossier reference entry
        self.dossier = tk.Entry(box_info, justify= 'center')
        self.dossier.grid(row=1,column=1, sticky=tk.W, padx=5,pady=5)
        self.dossier.bind("<Return>", self.get_data)        #get data for dossier
        self.dossier.focus_set()
        self.values["dossier_nummer"] = self.dossier
        namelabel = tk.Label(box_info, text = 'Naam:',justify= "center", font= LARGE_FONT, relief= "groove")
        namelabel.grid(row=2, column=0, sticky = tk.W, padx=5,pady=5)
        self.name = tk.Label(box_info, anchor="e", justify="center", font=LARGE_FONT)
        self.name.grid(row=2, column=1, sticky = tk.W, padx=5,pady=5)
        #create buttons
        self.mbutton_caps = ttk.Button(box_buttons, text = 'convert to caps', command=self.get_caps)
        self.mbutton_caps.grid(row= 0, column= 0, padx=5,pady=5)
        self.mbutton_files = ttk.Button(box_buttons, text = 'move files', command= self.move_backup)
        self.mbutton_files.grid(row=0, column= 1, padx=5,pady=5)

        box_buttons.grid(row= 0,column= 0, columnspan= 3, sticky= tk.W, padx= 5,pady= 5)
        box_info.grid(row= 1, column = 0, columnspan= 3, sticky= tk.W, padx= 5, pady= 5)

    def save_pdf(self):
        print("create new dict, useless?")
        """?    why create new dict?"""
        new_dict = {k:v.get() for k,v in self.values.items()}   #self.values from def initialise
        GetSave(new_dict)                                       #imported method from save_a_pdf.py

    def get_caps(self):
        print("convert to CAPS")
        self.caps.configure(state="normal")
        self.caps.delete(1.0, tk.END)
        data = {k:v.get().upper() for k,v in self.values.items()}
        self.caps.insert(tk.INSERT, CAPS_TEMPLATE.format(data))
        self.caps.configure(state="disabled")

    def renew_entry_data(self, the_dict):
        print("updating entry boxes")
        for key, value in the_dict.items():
            if key in self.values:
                self.values[key].delete(0, tk.END)
                self.values[key].insert(0, value)

    def get_data(self, event=None):
        print("searches datafile for dossier: *.xls")
        dossier = self.dossier.get()                            #gets dossier from entry
        while dossier.isdigit():                                #check for integer
            doss = folder_scan[dossier]
            bijlage = [f for f in os.listdir(doss['path']) if f.endswith('.xls')]
            if len(bijlage) == 1:
                x = doss["path"] + "//" + bijlage[0]
                self.name['text'] = folder_scan[dossier]['name']# set label text to name
                self.dossier_dir(folder_scan[dossier])          # check folders for dossier and creates missing folders
                self.selecting(x)                               # gets data
            else:
                #add manual support to select proper *.xls file
                #done in excelreader.py when no dossier(?)
                result = tk.messagebox.askquestion('Error', 'Excel Data file not found \n Do you want to select it manually?')
                if result == 'yes':
                    print('manually selecting *.xls')
                else:
                    break
        else:
            messagebox.showwarning("error", "not a number")

    def move_backup(self):
        print("moving backups")
        struct = self.structure()
        print(struct)
        """ need to redo code, change creation of paths"""
        path = os.path.dirname(os.path.realpath(sys.argv[0]))   # working directory path
        staal_path = folder_scan[self.dossier.get()]['path'] + "//Stabiliteit//Meetstaat & borderel//"
        backup_path = path + "//Backups"
        print("check if files already exist")
        for filename in os.listdir(backup_path):
            s_path = staal_path + "//" + filename
            direct = backup_path + "//" + filename
            if os.path.isfile(s_path) == False:
                print(" copy", filename)
                shutil.copy(direct, staal_path)
            else:
                print("passing")
                continue








"""--------------------settings window--------------------"""


""" change focus when settings window goes up, focus still on input entry"""

class Dialog(tk.Toplevel, Settings):
    def __init__(self, parent, title = None):
        print("initiating settings")
        tk.Toplevel.__init__(self, parent)
        if title:
            self.title("settings")
        self.body()
        self.buttonbox()
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.minsize(width=600, height=200)
        #these commands must be last in __init__
        self.transient(parent)                                  #set to be on top of the main window
        self.grab_set()                                         #hijack all commands from the master (clicks on the main window are ignored)
        parent.wait_window(self)                                #pause anything on the main window until this one closes

    def body(self):
        box = tk.Frame(self, pady=40)
        label = tk.Label(box, text="main directory",  relief = tk.RAISED)
        label.grid(column=0, row=0)
        self.dir_label = tk.Label(box, text = main_settings["directory"], relief = tk.RIDGE)
        self.dir_label.grid(column=1, row=0)
        box.pack()

    def buttonbox(self):
        box = tk.Frame(self, pady=40)
        w = ttk.Button(box, text="update dossiers", command=lambda: self.scan_folder())
        w.grid(column=3, row=1)
        w = ttk.Button(box, text="select folder", width=10, command = self.select_folder)
        w.grid(column=2, row=1)
        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(column= 0, row = 1)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(column= 1, row = 1)
        w = ttk.Button(box, text="check dirs", width=10, command=lambda: self.check_folders(folder_scan))
        w.grid(column = 4, row = 1)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()



    # standard button semantics
    """
    ISSUE 1 (solved?)
        MOVE saving settings when pressing ok
           other settings?
           put settings dict as class variable
        saving settings should save ALL settings

        also load settings from *.txt first
    """



    def select_folder(self, event=None):
        print("setting: manually select main folder")
        self.main_dir = askdirectory()
        if not self.main_dir:
            print("nothing selected")   # add popup message
            pass
            #WATCH FOR
            """
            >>>bool("")
            False
            >>> bool("   ")
            True
            >>> bool("   ".strip())
            False
            """
        else:
            print("saving settings")
            main_settings["directory"] = self.main_dir      #remove(?)
            self.dir_label['text'] = self.main_dir          # update label
        """?    change above settings save,
        only save when pressing ok???"""

    def scan_folder(self):
        print("scanning folder, needs to check for removed folders")
        s = self.read_folders(main_settings["directory"])   # from import Settings, main directory path
        global folder_scan                                  # clear dict first to not keep removed folders
        folder_scan = {}
        for item in s:
            folder_scan[item] = s[item]
        print('folder_scan', folder_scan)


    def ok(self, event=None):
        print("saving settings")
        """
        DONE
            load settings at init,
            and keep variables as class variable
            to send to save functions in settings.py
        """
        print("saving: \n", main_settings)
        print("saving: \n", folder_scan)
        global folder_scan
        self.save_set(main_settings)
        self.save_folder(folder_scan)
        self.cancel()

    def cancel(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = tk.Tk()                                           # create the root window here to give us flexibility
    window = CADapp(app)
    window.pack()
    app.mainloop()
