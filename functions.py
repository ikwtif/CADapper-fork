import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from settings import Settings
from excel_reader import read_excel
from save_a_pdf import GetSave
from tkinter import messagebox
from excel_cad import xlstocad

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



class Functions(Settings):

    """
    #####################################################################
                            CORE functions
    #####################################################################
    """

    def loading(self):
        """
        loads settings main app and dossiers
        """
        main_settings = {}
        folder_scan = {}
        mains, folder_s = self.loader()                         # returns a tuple, from settings.py
        print(mains, folder_s)
        for item in mains:
            main_settings[item] = mains[item]
        for item in folder_s:
            folder_scan[item] = folder_s[item]
        print("succesfully loaded \n {} \n {} ".format(main_settings, folder_scan))
        return main_settings, folder_scan


    def xlsgetdata(self, dossier=None):
        """
        returns dict with data after reading xls file
        """
        print("get data from *.xls")
        #gets data from *.xls
        the_dict = read_excel(dossier)                          #imported method from excel_reader.py, returns the_dictionary
        """?    """
        #adds dossier number from entry
        the_dict['dossier_nummer'] = self.dossier.get()         # else has no value because not in xls file
        return the_dict



    """
    #####################################################################
                            startpage functions
    #####################################################################
    """

    def save_pdf(self):
        """
        create dict with data from entry boxes and send to save function
        """
        new_dict = {k:v.get() for k,v in self.values.items()}       #self.values from def initialise
        GetSave(new_dict)                                           #imported method from save_a_pdf.py

    def save_cad(self):
        new_dict = {k:v.get() for k,v in self.values.items()}
        print("creating dictionary:\n", new_dict)
        xlstocad(new_dict)



    def get_caps(self):
        """
        Capitalise data in entry boxes and update textbox
        """
        self.caps.configure(state="normal")
        self.caps.delete(1.0, tk.END)
        data = {k:v.get().upper() for k,v in self.values.items()}
        self.caps.insert(tk.INSERT, CAPS_TEMPLATE.format(data))
        self.caps.configure(state="disabled")

    def update_entry(self, the_dict):
        """
        update entry boxes
        """
        for key, value in the_dict.items():
            if key in self.values:
                self.values[key].delete(0, tk.END)
                self.values[key].insert(0, value)

    def xlscheck(self, dossier, folder_scan, event=None):
        """
        checks for ONE existing xls or lets you chose if non existent/multiple
        defaults to NONE when not manually chosen
        """
        doss = folder_scan[dossier]
        xlsfiles = [f for f in os.listdir(doss['path']) if f.endswith('.xls')]
        if len(xlsfiles) == 1:
            xlspath = doss["path"] + "//" + xlsfiles[0]
            return xlspath
        else:
            result = tk.messagebox.askquestion('Error', 'Excel Data file not found \n Do you want to select it manually?')
            if result == 'yes':
                print('manually selecting *.xls')
                xlspath = askopenfilename()
                return xlspath
            else:
                print("no selection made")


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

    def openfolder(self):
        dossier = self.dossier.get()





    """
    #####################################################################
                            Settings functions
    #####################################################################
    """

    def select_folder(self, settings, event=None):
        print("setting: manually select main folder")
        global main_settings
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
            print("saving settings \n")
            settings["directory"] = self.main_dir      #remove(?)
            self.dir_label['text'] = self.main_dir          # update label
        """?    change above settings save,
        only save when pressing ok???"""

    def scan_folder(self, settings):
        print("scanning folder, needs to check for removed folders\n")
        s = self.read_folders(settings["directory"])   # from import Settings, main directory path
        #global folder_scan                                  # clear dict first to not keep removed folders
        self.folder_scan = {}
        for item in s:
            self.folder_scan[item] = s[item]
        print('folder_scan:\n', self.folder_scan)


    def ok(self, fold, main, event=None):
        """
        Saves settings
        """
        #global folder_scan, main_settings
        print("saving: \n", main)
        print("saving: \n", fold)
        self.save_set(main, "settings.txt")
        self.save_set(fold, "folders.txt")
        self.cancel()

    def cancel(self, event=None):
        self.destroy()
