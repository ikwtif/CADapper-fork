import sys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import json

from excel_reader import read_excel
from save_a_pdf import GetSave

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

'''The point of a computer is ....
... To do repetitive tasks for you. If you find yourself copy and pasteing
code 13 times, you are doing the computer's job!'''

LARGE_FONT= ("Verdana", 12)

class CADapp(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#-----------------------------------------------------------------------
		#add menu bar
		menubar = Menu(self)
		master.config(menu=menubar)
		#--------------------------------------------------------------------------
		self.frames = {}                            #multiple windows
		for window in [StartPage]: #list of windows
			frame = window(self)     #startpage = initial window
			self.frames[window] = frame
			frame.grid(row= 0, column= 0, sticky="nsew", padx=5,pady=5)
		self.show_frame(StartPage)                  #show starting frame

	def show_frame(self, cont):
		#initialise page
		frame = self.frames[cont]
		frame.tkraise()

	def selecting(self, dossier=None):
		#gets data from *.xls
		the_dict = read_excel(dossier) #imported method from excel_reader.py, returns the_dictionary
		page = self.frames[StartPage]
		page.renew_entry_data(the_dict)

class Menu(tk.Menu):
	def __init__(self, master):
		tk.Menu.__init__(self, master)

		filemenu = tk.Menu(self, tearoff = 0)
		filemenu.add_command(label="select file", command=master.selecting)
		filemenu.add_command(label="settings", command=lambda: Dialog(master))
		filemenu.add_command(label="save settings")
		filemenu.add_separator()    #adding divider
		filemenu.add_command(label="exit", command = quit)
		#add filemenu to menubar
		self.add_cascade(label="File", menu=filemenu)


"""adding pages"""

#Having the fields in a single list with a single name scheme will make editing the fields a lot easier.
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

class StartPage(tk.Frame):

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)             #parent class = CADapp
		self.parent = parent

		self.initialise()
		self.body_buttons()

	def initialise(self):
		self.values = {}
		for row, field in enumerate(FIELDS, start=3):
			label = tk.Label(self, text=field, font=LARGE_FONT)
			label.grid(row=row,column=0, sticky=tk.W, padx=5,pady=5)
			entry = tk.Entry(self, width = 60) #an Entry widget does not require a StringVar, and it does not help you any
			entry.grid(row=row, column = 1)
			self.values[field] = entry

		#create text widget for CAPS convertor
		self.caps = tk.Text(self, width= 60)
		self.caps.grid(row= 3, column= 2, rowspan = 15, padx=5,pady=5)

	def body_buttons(self):
		box_buttons = tk.Frame(self)
		#create dossier reference label
		label = tk.Label(box_buttons, text="dossier_nummer", font=LARGE_FONT)
		label.grid(row=0,column=3, sticky=tk.W, padx=5,pady=5)
		#create dossier reference entry
		self.dossier = tk.Entry(box_buttons, width = 60)
		self.dossier.grid(row=0,column=4, sticky=tk.W)
		self.dossier.bind("<Return>", self.get_data)
		self.dossier.focus_set()
		self.values["dossier_nummer"] = self.dossier
		#create buttons
		self.mbutton_save = ttk.Button(box_buttons, text ='save pdf', command=self.save_pdf)
		self.mbutton_save.grid(row= 0,column= 0)
		self.mbutton_quit = ttk.Button(box_buttons, text ='Quit', command=quit)
		self.mbutton_quit.grid(row= 0,column= 1)
		self.mbutton_caps = ttk.Button(box_buttons, text = 'convert to caps', command=self.get_caps)
		self.mbutton_caps.grid(row= 0, column= 2)

		box_buttons.grid(row=0,column=0, columnspan=3, sticky= tk.W)

	def save_pdf(self):
		#create new dict
		new_dict = {k:v.get() for k,v in self.values.items()}
		GetSave(new_dict)    #imported method from save_a_pdf.py

	#convert data to CAPS data
	def get_caps(self):
		self.caps.configure(state="normal")
		self.caps.delete(1.0, tk.END)
		data = [self.values[field].get().upper() for field in FIELDS]
		template = "{} \n{} \n\n{} \n{} \n{} \n\n{} \n{} \n{} \n{} \n\n{} \n{} \n\n{} \n"
		self.caps.insert(tk.INSERT, template.format(*data))
		self.caps.configure(state="disabled")

	#update entry boxes
	def renew_entry_data(self, the_dict):
		for key, value in the_dict.items():
			if key in self.values:
				self.values[key].delete(0, tk.END)
				self.values[key].insert(0, value)

	#user input, dossier reference number
	def get_data(self, event=None):
		s = self.dossier.get()
		#check for integer
		try:
			int(s)
			print(s)
			self.parent.selecting(dossier=s)
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



class Dialog(tk.Toplevel):
	def __init__(self, parent, title = None):
		tk.Toplevel.__init__(self, parent)

		if title:
			self.title("settings")

		self.body()
		self.buttonbox()

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		#these commands must be last in __init__
		self.transient(parent) #set to be on top of the main window
		self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
		parent.wait_window(self) #pause anything on the main window until this one closes

	def body(self):
		# create dialog body.
		box = tk.Frame(self)
		label = tk.Label(box, text="main directory",  relief = tk.RAISED)
		label.grid(column=0, row=0)
		self.dir_label = tk.Label(box, text = "none", relief = tk.RIDGE)
		self.dir_label.grid(column=1, row=0)
		box.pack()

	def buttonbox(self):
		# add button box
		box = tk.Frame(self)
		w = tk.Button(box, text="select folder", width=10, command = self.select_folder)
		w.grid(column=2, row=1)
		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.grid(column= 0, row = 1)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
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

		with open("settings.txt","w") as f:
			json.dump(f, settings, indent = 4)

		print(self.main_dir)

		self.dir_label['text'] = self.main_dir

	def ok(self, event=None):
		self.cancel()

	def cancel(self, event=None):
		self.destroy()

if __name__ == "__main__":
	app = tk.Tk() #we create the root window here to give us flexibility
	window = CADapp(app)
	window.pack()
	app.mainloop()
