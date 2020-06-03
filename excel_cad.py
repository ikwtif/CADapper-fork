import xlrd, xlutils
from xlrd import open_workbook
from xlutils.copy import copy2

"""
##################################################
DO NOT REMOVE
##################################################

First you need that patch function by John Machin provided in a very similar question:

from xlutils.filter import process,XLRDReader,XLWTWriter

#
# suggested patch by John Machin
# http://stackoverflow.com/a/5285650/2363712
#
def copy2(wb):
    w = XLWTWriter()
    process(
        XLRDReader(wb,'unknown.xls'),
        w
        )
    return w.output[0][1], w.style_list
"""


def xlstocad(data, xlspath):
    structure = ['ingenieur',
                'ingenieur email',
                'architect',
                'architect straat',
                'architect gemeente',
                'architect tel',
                'architect email',
                'bouwheer',
                'woning straat',
                'woning gemeente',
                'werfadres',
                'werfgemeente'
                ]

    cell = ['8','2',
            '9','2',
            '13','2',
            '14','2',
            '15','2',
            '16','2',
            '17','2',
            '21','2',
            '22','2',
            '23','2',
            '25','2',
            '26','2'
            ]

    print("initiate xlstocad")
    #xlspath = folder_scan[data['dossier']]['path'] + "//Stabiliteit//Stabiliteitsplannen//data.xls"
    inbook = open_workbook(xlspath, formatting_info = True)
    insheet = inbook.sheet_by_index(0)
    outbook, outstyle = copy2(inbook)
    row=0
    column=1
    for item in structure:
        xf_index = insheet.cell_xf_index(int(cell[row]), int(cell[column]))
        saved_style = outstyle[xf_index]
        outbook.get_sheet(0).write(int(cell[row]), int(cell[column]), data[item], saved_style)
        outbook.save(xlspath)
        row += 2
        column += 2

def xlstomeetstaat(data, xlspath):
    structure = ['dossier',
                 'werfadres',
                 'werfgemeente',
                 'bouwheer',
                 'architect',
                 'architect straat',
                 'architect gemeente',
                 'aannemer'
                 ]

    cell = ['0','1',
            '1','1',
            '2','1',
            '3','1',
            '4','1',
            '5','1',
            '6','1',
            '7','1',
            ]
    
    print("initiate xlstomeetstaat")
    #xlspath = folder_scan[data['dossier']]['path'] + "//Stabiliteit//Meetstaat & borderel//data meetstaat&borderel.xls"
    print(xlspath)
    inbook = open_workbook(xlspath, formatting_info = True)
    insheet = inbook.sheet_by_index(0)
    outbook, outstyle = copy2(inbook)
    row=0
    column=1
    print(structure)
    for item in structure:
        print(item)
        xf_index = insheet.cell_xf_index(int(cell[row]), int(cell[column]))
        saved_style = outstyle[xf_index]
        outbook.get_sheet(0).write(int(cell[row]), int(cell[column]), data[item], saved_style)
        outbook.save(xlspath)
        row += 2
        column += 2

