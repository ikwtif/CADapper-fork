import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import json

from excel_reader import read_excel
from save_a_pdf import get_save

"""
main menu file with class structure

TO DO
    - load settings at startup
        - main directory path 
        - dict dossier folders 

    -settings menu
        - storing settings with json when 'ok' is pressed
        - create scan option for dossier folders
    
    -dossier reference nr (user input)
        -auto locate *.xls file by user input and get excel data
            -create dossier folder path
            -find *.xls file in dossier map
            -create pdf save path, append "//Stabiliteit//Plannen pdf"
                to dossier path

"""

LARGE_FONT= ("Verdana", 12)



class CADapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        
        self.container.grid(row= 0,column= 0)            
        self.container.grid_rowconfigure(0, weight= 1)    
        self.container.grid_columnconfigure(0, weight= 1)

        #-----------------------------------------------------------------------
        #add menu bar
        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label="select file", command=lambda: self.selecting(frame, self.container))
        filemenu.add_command(label="settings", command=lambda: Dialog(frame, self.container))
        #filemenu.add_command(label="save settings"
        filemenu.add_separator()    #adding divider
        filemenu.add_command(label="exit", command = quit)
        #add filemenu to menubar
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        #--------------------------------------------------------------------------
        self.frames = {}                            #multiple windows
        frame = StartPage(self.container, self)     #startpage = initial window
        self.frames[StartPage] = frame
        frame.grid(row= 0, column= 0, sticky="nsew", padx=5,pady=5)      
        self.show_frame(StartPage)                  #initialise StartPage

    def show_frame(self, cont):
        #initialise page
        frame = self.frames[cont]
        frame.tkraise()                             
        
    def selecting(self, parent, controller):
        #gets data from *.xls
        reading_excel = read_excel()    #imported method from excel_reader.py
                                        #returns the_dictionary
        self.diction = reading_excel.reading()
        the_dict = self.diction
        page = self.frames[StartPage]
        page.renew_entry_data(the_dict)
        

"""adding pages"""

class StartPage(tk.Frame, CADapp):

    def __init__(self, parent, controller):        
        tk.Frame.__init__(self, parent)             #parent class = CADapp
        self.controller = controller
        self.initialise()
        self.body_buttons()
        
    def initialise(self):
        self.usertext1 = StringVar()
        self.usertext12 = StringVar()
        self.usertext13 = StringVar()
        self.usertext2 = StringVar()
        self.usertext3 = StringVar()
        self.usertext4 = StringVar()
        self.usertext5 = StringVar()
        self.usertext6 = StringVar()
        self.usertext7 = StringVar()
        self.usertext8 = StringVar()
        self.usertext9 = StringVar()
        self.usertext10 = StringVar()
        self.usertext11 = StringVar()
             
        #create labels
        label1 = tk.Label(self, text="bouwheer", font=LARGE_FONT)
        label1.grid(row= 3,column= 0, sticky=tk.W, padx=5,pady=5)
        label11 = tk.Label(self, text="werfadres", font=LARGE_FONT)
        label11.grid(row= 4,column= 0, sticky=tk.W, padx=5,pady=5)
        label12 = tk.Label(self, text="werfgemeente", font=LARGE_FONT)
        label12.grid(row= 5,column= 0, sticky=tk.W, padx=5,pady=5) 
        label2 = tk.Label(self, text="woning straat", font=LARGE_FONT)
        label2.grid(row=6,column=0, sticky=tk.W, padx=5,pady=5)
        label3 = tk.Label(self, text="woning gemeente", font=LARGE_FONT)
        label3.grid(row=7,column=0, sticky=tk.W, padx=5,pady=5)
        label4 = tk.Label(self, text="architect", font=LARGE_FONT)
        label4.grid(row=8,column=0, sticky=tk.W, padx=5,pady=5)
        label5 = tk.Label(self, text="architect straat", font=LARGE_FONT)
        label5.grid(row=9,column=0, sticky=tk.W, padx=5,pady=5)
        label6 = tk.Label(self, text="architect gemeente", font=LARGE_FONT)
        label6.grid(row=10,column=0, sticky=tk.W, padx=5,pady=5)
        label7 = tk.Label(self, text="aannemer", font=LARGE_FONT)
        label7.grid(row=11,column=0, sticky=tk.W, padx=5,pady=5)
        label8 = tk.Label(self, text="aannemer straat", font=LARGE_FONT)
        label8.grid(row=12,column=0, sticky=tk.W, padx=5,pady=5)
        label9 = tk.Label(self, text="aannemer gemeente", font=LARGE_FONT)
        label9.grid(row=13,column=0, sticky=tk.W, padx=5,pady=5)
        label10 = tk.Label(self, text="ingenieur", font=LARGE_FONT)
        label10.grid(row=14,column=0, sticky=tk.W, padx=5,pady=5)
    
        #create text widget for CAPS convertor
        self.caps_1 = Text(self, width= 60)
        self.caps_1.grid(row= 3, column= 2, rowspan = 15, padx=5,pady=5)
    
        #create entries
        self.Entry1 = tk.Entry(self, width = 60, textvariable = self.usertext1)
        self.Entry1.grid(row = 3, column = 1)
        self.Entry12 = tk.Entry(self, width = 60, textvariable = self.usertext12)
        self.Entry12.grid(row = 4, column = 1)
        self.Entry13 = tk.Entry(self, width = 60, textvariable = self.usertext13)
        self.Entry13.grid(row = 5, column = 1)
        self.Entry2 = tk.Entry(self, width = 60, textvariable = self.usertext2)
        self.Entry2.grid(row=6,column=1, sticky=tk.W)
        self.Entry3 = tk.Entry(self, width = 60, textvariable = self.usertext3)
        self.Entry3.grid(row=7,column=1, sticky=tk.W)
        self.Entry4 = tk.Entry(self, width = 60, textvariable = self.usertext4)
        self.Entry4.grid(row=8,column=1, sticky=tk.W)
        self.Entry5 = tk.Entry(self, width = 60, textvariable = self.usertext5)
        self.Entry5.grid(row=9,column=1, sticky=tk.W)
        self.Entry6 = tk.Entry(self, width = 60, textvariable = self.usertext6)
        self.Entry6.grid(row=10,column=1, sticky=tk.W)
        self.Entry7 = tk.Entry(self, width = 60, textvariable = self.usertext7)
        self.Entry7.grid(row=11,column=1, sticky=tk.W)
        self.Entry8 = tk.Entry(self, width = 60, textvariable = self.usertext8)
        self.Entry8.grid(row=12,column=1, sticky=tk.W)
        self.Entry9 = tk.Entry(self, width = 60, textvariable = self.usertext9)
        self.Entry9.grid(row=13,column=1, sticky=tk.W)
        self.Entry10 = tk.Entry(self, width = 60, textvariable = self.usertext10)
        self.Entry10.grid(row=14,column=1, sticky=tk.W)   

    def body_buttons(self):
        box_buttons = Frame(self)
        #create dossier reference label
        self.label10 = tk.Label(box_buttons, text="dossier_nummer", font=LARGE_FONT)
        self.label10.grid(row=0,column=3, sticky=tk.W, padx=5,pady=5)
        #create dossier reference entry
        self.Entry11 = tk.Entry(box_buttons, width = 60, textvariable = self.usertext11)
        self.Entry11.grid(row=0,column=4, sticky=tk.W)
        self.Entry11.bind("<Return>", self.get_data)
        self.Entry11.focus_set()
        #create buttons
        self.mbutton_save = ttk.Button(box_buttons, text ='save pdf', command=lambda:  self.save_pdf(self))
        self.mbutton_save.grid(row= 0,column= 0)
        self.mbutton_quit = ttk.Button(box_buttons, text ='Quit', command=quit)
        self.mbutton_quit.grid(row= 0,column= 1)
        self.mbutton_caps = ttk.Button(box_buttons, text = 'convert to caps', command=lambda: self.get_caps(self))
        self.mbutton_caps.grid(row= 0, column= 2)

        box_buttons.grid(row=0,column=0, columnspan=3, sticky= tk.W)

       
    def save_pdf(self, obj):  
        #create new dict
        self.new_dict = {}
        self.new_dict['woning_naam'] = self.usertext1.get()
        newer_dict = self.new_dict  #?
        self.new_dict['werf_straat'] = self.usertext12.get()
        self.new_dict['werf_gemeente'] = self.usertext13.get()
        self.new_dict['woning_straat'] = self.usertext2.get()
        self.new_dict['woning_gemeente'] = self.usertext3.get()
        self.new_dict['architect_naam'] = self.usertext4.get()
        self.new_dict['architect_straat'] = self.usertext5.get()
        self.new_dict['architect_gemeente'] = self.usertext6.get()
        self.new_dict['aannemer_naam'] = self.usertext7.get()
        self.new_dict['aannemer_straat'] = self.usertext8.get()
        self.new_dict['aannemer_gemeente'] = self.usertext9.get()
        self.new_dict['ingenieur_naam'] = self.usertext10.get()  
        self.new_dict['dossier_nummer'] = self.usertext11.get()
        
        get_save(newer_dict)    #imported method from save_a_pdf.py

    #convert data to CAPS data
    def get_caps(self, obj):
        self.caps_1.configure(state="normal")
        self.caps_1.delete(1.0, END)
        self.caps_1.insert(INSERT, "{} \n{} \n\n{} \n{} \n{} \n\n{} \n{} \n{} \n{} \n\n{} \n{} \n\n{} \n\
                           ".format(self.usertext12.get().upper(),
                                    self.usertext13.get().upper(),
                                    self.usertext1.get().upper(),
                                    self.usertext2.get().upper(),
                                    self.usertext3.get().upper(),
                                    self.usertext4.get().upper(),
                                    self.usertext5.get().upper(),
                                    self.usertext6.get().upper(),
                                    self.usertext7.get().upper(),
                                    self.usertext8.get().upper(),
                                    self.usertext9.get().upper(),
                                    self.usertext10.get().upper(),
                                    ))
        self.caps_1.configure(state="disabled")


    #update entry boxes
    def renew_entry_data(self, the_dict):
        self.usertext1.set(the_dict['woning_naam'])
        self.usertext12.set(the_dict['werf_straat'])
        self.usertext13.set(the_dict['werf_gemeente'])
        self.usertext2.set(the_dict['woning_straat'])
        self.usertext3.set(the_dict['woning_gemeente'])
        self.usertext4.set(the_dict['architect_naam'])
        self.usertext5.set(the_dict['architect_straat'])
        self.usertext6.set(the_dict['architect_gemeente'])
        self.usertext7.set(the_dict['aannemer_naam'])
        self.usertext8.set(the_dict['aannemer_straat'])
        self.usertext9.set(the_dict['aannemer_gemeente'])
        self.usertext10.set(the_dict['ingenieur_naam'])


    #user input, dossier reference number
    def get_data(self, event=None):
        s = self.Entry11.get()
        #check for integer
        try:
            int(s)
            print(s)
            self.controller.selecting(None, None) 
            """
            testing function, will change for auto-opening an *.xls file
            trough dossier reference number input, from a folder structure
            with name format "dossier reference number - Name"
            all present folder names will be split up in a dict with
                key: dossier reference number
                value: Name (better: full folder name to append to main dir)
            dict gets loaded at startup with json from *.txt and
            makes a new scan when key(folder) does not exist yet
            [json data gets saved after a scan]

            if key exists, create file path (always has same name)
            or look for (the sole) *.xls in folder (avoid error in filename),
            then get *.xls data like usual
            --need to remove 'open_file' from excel_reader at that point
              as there is no need to make the user select the file anymore            
            """
            
     
        except ValueError:
            messagebox.showwarning("error", "not a number")    

        

class Dialog(Toplevel, CADapp):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title("settings")

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(side="top", fill="both", expand = True)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have initial focus   
        Label_dir = Label(master, text="main directory",  relief = RAISED)
        Label_dir.grid(column=0, row=0)
        self.Label2_dir = Label(master, text = "none", relief = RIDGE)
        self.Label2_dir.grid(column=1, row=0)

    def buttonbox(self):
        # add button box
        box = Frame(self)
        w = Button(box, text="select folder", width=10, command = self.select_folder)
        w.grid(column=2, row=1)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.grid(column= 0, row = 1)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(column= 1, row = 1)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()
    #
    # standard button semantics
    def select_folder(self, event=None):

        print("selecting folder")
        settings = {}
        self.main_dir = askdirectory()
        print(self.main_dir)
        settings['directory'] = self.main_dir
            
        s = json.dumps(settings, indent = 4)
        print(s)
        with open("c://data//settings.txt","w") as f:
            f.write(s)

        print(self.main_dir)

        self.Label2_dir['text'] = self.main_dir
        

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override




if __name__ == "__main__":
    app = CADapp()
    app.mainloop()

            
