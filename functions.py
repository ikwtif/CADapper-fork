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
from excel_cad import xlstocad, xlstomeetstaat, xlstoborderel
from datetime import datetime

main_settings = {
    "directory":""
    }

folder_scan = {
    }


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

"""
ADD backup move for CAD START DWGs and linked XLS files in move_backup
"""

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
        global main_settings, folder_scan
        main_settings = {}
        folder_scan = {}
        mains, folder_s = self.loader()                         # returns a tuple, from settings.py
        print(mains, folder_s)
        for item in mains:
            main_settings[item] = mains[item]
        for item in folder_s:
            folder_scan[item] = folder_s[item]
        print("succesfully loaded \n {} \n {} ".format(main_settings, folder_scan))



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
    def openfolder(self):
        print("opening dossier")
        os.startfile(folder_scan[self.dossier.get()]['path'])

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

    def save_meetstaat(self):
        new_dict = {k:v.get() for k,v in self.values.items()}
        new_dict['dossier'] = self.dossier.get()
        print("creating dictionary:\n", new_dict)
        xlstomeetstaat(new_dict, folder_scan)


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


    def move_xls(self):
        print("moving backup borderel&meetstaat")
        src_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + "//Backups/Staal"   # working directory path
        dst_dir = folder_scan[self.dossier.get()]['path'] + "//Stabiliteit//Meetstaat & borderel//"
        print("check if files already exist")
        print("source:", src_dir)
        print("destination:", dst_dir)
        self.copyfiles(src_dir, dst_dir)
        """
        Needs to create maps if not existing
        same as move dwg, seperate function?
        """
        #add renaming filename

    def move_dwg(self):
        print("moving backup dwg&xls")
        src_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + "//Backups//Cad"
        dst_dir = folder_scan[self.dossier.get()]['path'] + "//Stabiliteit//Stabiliteitsplannen//"
        print("check if files already exist")
        """
        change with try ? Make seperate function??? since same as move_backup
        """
        self.copyfiles(src_dir, dst_dir)
        #add renaming filename

    def copyfiles(self, src_dir, dst_dir):
        """
        copies all files in src_dir to dst_dir
        """
        for filename in os.listdir(src_dir):
            dst_file = os.path.join(dst_dir, filename)
            src_file = os.path.join(src_dir, filename)
            if os.path.isfile(dst_file) == False:
                shutil.copy(src_file, dst_file)
                self.changename(filename)
            else:
                print("existing: add replace function?\n", filename)
                continue


    def changename(self, filename):
        
        if filename.endswith('.dwg'):
            date = datetime.now()
            print(date)
            print(type(date))
            newname = "stabiliteitsplan"
            creator = "ddb"
            dossier = self.dossier.get()
            newfilename = date + "_" + newname + "_" + creator + "_" + dossier
            dst_newfilename = os.path.join(dst_dir, newfilename)
            os.rename(dst_file, dst_newfilename)

        """
        change filename
        example:
        def copy_rename(old_file_name, new_file_name):
        src_dir= os.curdir
        dst_dir= os.path.join(os.curdir , "subfolder")
        src_file = os.path.join(src_dir, old_file_name)
        shutil.copy(src_file,dst_dir)
        
        dst_file = os.path.join(dst_dir, old_file_name)
        new_dst_file_name = os.path.join(dst_dir, new_file_name)
        os.rename(dst_file, new_dst_file_name)
        """





    """
    #####################################################################
                            Settings functions
    #####################################################################
    """

    def select_folder(self, event=None):
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
            print("saving settings \n need to remove (?) next line, only save when pressing button")
            """does not save, but stores in memory check vs save file on loading settings?
               or somehow remove when going back to settings"""
            main_settings["directory"] = self.main_dir #remove
            self.dir_label['text'] = self.main_dir          # update label
        """?    change above settings save,
        only save when pressing ok???"""

    def scan_folder(self):
        global main_settings, folder_scan
        print("scanning folder, needs to check for removed folders\n")
        s = self.read_folders(main_settings["directory"])        # Settings.py, main directory path
        # clear dict first to not keep removed folders
        folder_scan = {}
        for item in s:
            folder_scan[item] = s[item]
        print('folder_scan:\n {}'.format(folder_scan))


    def ok(self, event=None):
        global folder_scan, main_settings
        """
        content = fold, main
        Saves settings with (filename, content)
        """
        #global folder_scan, main_settings
        print("saving: \n", main_settings)
        print("saving: \n", folder_scan)
        self.save_set("settings.txt", main_settings)
        self.save_set("folders.txt", folder_scan)
        self.cancel()

    def cancel(self, event=None):
        self.destroy()
