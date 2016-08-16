import os
import shutil
import sys
import time

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory

from settings import Settings
from excel_reader import read_excel
from save_a_pdf import GetSave
from excel_cad import xlstocad, xlstomeetstaat


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


class Functions(Settings):

    """
    #####################################################################
                            CORE functions
    #####################################################################
    """

    def loading(self):
        """
        loads settings (main app and dossiers)
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
        reads xls file
            returns dict with data
        """
        the_dict = read_excel(dossier)                          # imported method from excel_reader.py, returns the_dictionary
        the_dict['dossier'] = self.dossier.get()                # adds dossier number from entry
            # else has no value because not in xls file
        return the_dict

    def getentries(self):
        """
        create dict with data from entry boxes + dossier number
        """
        entries = {k:v.get() for k,v in self.values.items()}        #self.values from def initialise
        entries['dossier'] = self.dossier.get()
        return entries

    """
    #####################################################################
                            startpage functions
    #####################################################################
    """
    def openfolder(self):
        """
        open current dossier
        """
        print("opening dossier")
        os.startfile(folder_scan[self.dossier.get()]['path'])

    def save(self, item):
        data = self.getentries()
        dossierfolder = folder_scan[data['dossier']]['path']
        if item == 'pdf':
            pdfpath =  dossierfolder + "//Stabiliteit//Algemene documenten//stabiliteitsbundel.pdf"
            GetSave(data, pdfpath)                          # imported method from save_a_pdf.py
        elif item == 'cad':
            xlspath = dossierfolder + "//Stabiliteit//Stabiliteitsplannen//data.xls"
            xlstocad(data, xlspath)                         # imported method from excel_cad.py
        elif item == 'meetstaat':
            xlspath = dossierfolder + "//Stabiliteit//Meetstaat & borderel//data meetstaat&borderel.xls"
            xlstomeetstaat(data, xlspath)                   # imported method from excel_cad.py
            # check if still works after reloading program (folder_scan global variable)

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

    #working on move_backup
    def move_backup(self, back):
        str_back = {'staal':'//Backups/Staal',
                'cad':'//Backups//Cad'}
        cwd = os.path.dirname(os.path.realpath(sys.argv[0])         # working directory
        src_dir = src_back + str_back[back]
        pass


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
        self.dst_dir = folder_scan[self.dossier.get()]['path'] + "//Stabiliteit//Stabiliteitsplannen//"
        print("check if files already exist")
        """
        change with try ? Make seperate function??? since same as move_xls
        """
        self.copyfiles(src_dir, self.dst_dir)
        #add renaming filename

    def copyfiles(self, src_dir, dst_dir):
        """
        copies ALL files from source directory (src_dir) to destination directory (dst_dir)
        """
        for filename in os.listdir(src_dir):
            self.dst_file = os.path.join(dst_dir, filename)
            src_file = os.path.join(src_dir, filename)
            if os.path.isfile(self.dst_file) == False:
                shutil.copy(src_file, self.dst_file)
                #self.changename(filename)
            else:
                print("existing: add replace function?\n", filename)
                continue


    def changename(self, filename):
        if filename.endswith('.dwg'):
            date = time.strftime("%Y%m%d")
            print(date)
            print(type(date))
            newname = "stabiliteitsplan"
            creator = "ddb"
            dossier = self.dossier.get()
            extention = ".dwg"
            newfilename = "{}_{}_{}_{}{}".format(date, newname, creator, dossier, extention)
            dst_newfilename = os.path.join(self.dst_dir, newfilename)
            os.rename(self.dst_file, dst_newfilename)


    """
    #####################################################################
                            Settings functions
    #####################################################################
    """

    def select_folder(self, event=None):
        """
        select main directory
                    = folder with dossiers
        """
        print("setting: manually select main folder")
        global main_settings
        self.main_dir = askdirectory()
        if not self.main_dir:
            print("nothing selected")                       # add popup message
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
            """does not save, but stores in memory

            check vs save file on loading settings?
            or somehow remove when going back to settings"""
            main_settings["directory"] = self.main_dir      # remove for no instant save
            self.dir_label['text'] = self.main_dir          # update label
        """?    change above settings save,
        only save when pressing ok???"""

    def scan_folder(self):
        """
        populates folder_scan with dirscan
        """
        global main_settings, folder_scan
        print("scanning folder, needs to check for removed folders\n")
        s = self.read_folders(main_settings["directory"])       # Settings.py, main directory path
        folder_scan = {}                                        # clear dict first to not keep removed folders
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
