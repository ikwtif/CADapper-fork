import xlrd
import time
from tkinter.filedialog import askopenfilename


class read_excel():      
    def open_file(self):
        file_name = askopenfilename()
        print(file_name)
        return file_name
    
    def split_adress(self, adress):
        self.split_up = adress.split(", ")
        if self.split_up == ['']:
            self.split_up.append('')
            return self.split_up
        else:
            return self.split_up
    def reading(self):
        print("start reading excel")
        self.file_path = self.open_file()    
        self.book = xlrd.open_workbook(self.file_path)
        # get the first worksheet
        self.first_sheet = self.book.sheet_by_index(0)
        #create dict
        self.label_dict = {"woning_naam": "W-naam",
        "woning_straat": "straat",
        "woning_gemeente": "gemeente",
        "werf_straat": "straat",
        "werf_gemeente": "gemeente",
        "architect_naam": "A-naam",
        "architect_straat": "straat",
        "architect_gemeente": "gemeente",
        "aannemer_naam": "Aa-naam",
        "aannemer_straat": "straat",
        "aannemer_adres": "adres",
        "ingenieur_naam": " ",
        "dossier_nummer": " ",
        }
            #werfadres      
        self.werf_full_adress = (self.first_sheet.cell(3,2).value)
        print(self.werf_full_adress)
        werf_adress = self.split_adress(self.werf_full_adress)
        print(werf_adress)
        self.label_dict["werf_straat"] = werf_adress[0]
        print(werf_adress[0])
        self.label_dict["werf_gemeente"] = werf_adress[1]
        print(werf_adress[1])
        
            #bouwheer
        self.label_dict["woning_naam"] = (self.first_sheet.cell(13,1).value)
        self.woning_full_adress = (self.first_sheet.cell(13,2).value)
        w_adress = self.split_adress(self.woning_full_adress)
        self.label_dict["woning_straat"] = w_adress[0]
        self.label_dict["woning_gemeente"] = w_adress[1]
            #architect
        self.label_dict["architect_naam"] = (self.first_sheet.cell(14,1)).value
        self.architect_full_adress = (self.first_sheet.cell(14,2)).value
        arch_adress = self.split_adress(self.architect_full_adress)
        self.label_dict["architect_straat"] = arch_adress[0]
        self.label_dict["architect_gemeente"] = arch_adress[1]
            #aannemer
        self.label_dict["aannemer_naam"] = (self.first_sheet.cell(25,1).value)
        self.aannemer_full_adress = (self.first_sheet.cell(25,2).value)
        aa_adress = self.split_adress(self.aannemer_full_adress)
        self.label_dict["aannemer_straat"] = aa_adress[0]
        self.label_dict["aannemer_gemeente"] = aa_adress[1]
            #ingenieur
        self.label_dict["ingenieur_naam"] = "ingenieur"
            #dossier nummer
        self.label_dict["dossier_nummer"] = "dossier nummer"
        print(self.label_dict)
        print("me")
        the_dictionary = self.label_dict
        print(the_dictionary)
        return the_dictionary
    

if __name__ == "__main__":
    reader=read_excel()
    reader.reading()
    print("test")
    print(the_dictionary)
