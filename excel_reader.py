import xlrd
import time
from tkinter.filedialog import askopenfilename

def open_file():
	file_name = askopenfilename()
	print(file_name)
	return file_name

def split_adress(adress):
	split_up = adress.split(", ")
	if split_up == ['']:
		split_up.append('')
	return split_up

def read_excel(dossier=None):
	print("start reading excel")
	if dossier is not None:
		file_path = "code to find the file path from the dossier number"
	else:
		file_path = open_file()

	book = xlrd.open_workbook(file_path)
	# get the first worksheet
	first_sheet = book.sheet_by_index(0)
	#create dict
	werf_adress = split_adress(first_sheet.cell(3,2).value)
	w_adress = split_adress(first_sheet.cell(13,2).value)
	arch_adress = split_adress(first_sheet.cell(14,2).value)
	aa_adress = split_adress(first_sheet.cell(25,2).value)
	label_dict = {
		"woning straat": werf_adress[0],
		"woning gemeente": werf_adress[1],
		"bouwheer": first_sheet.cell(13,1).value,
		"werfadres": w_adress[0],
		"werfgemeente": w_adress[1],
		"architect": first_sheet.cell(14,1).value,
		"architect straat": arch_adress[0],
		"architect gemeente": arch_adress[1],
		"aannemer": first_sheet.cell(25,1).value,
		"aannemer straat": aa_adress[0],
		"aannemer gemeente": aa_adress[1],
		"ingenieur": "ingenieur",
		"dossier_nummer": "dossier nummer"
		}
	return label_dict


if __name__ == "__main__":
    print(read_excel())
