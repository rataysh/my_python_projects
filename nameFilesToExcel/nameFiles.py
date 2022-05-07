import os, time, xlsxwriter, openpyxl
import pandas as pd
from openpyxl import Workbook


names_xls = []
path_to_directory = input(f'Введите путь к папке начала сбора наименований:')
filename = 'name_all_files_in_directory.xlsx'

list_name_directiry = {}
delList = []
testList = []
row = 1
wb = Workbook()
sheet = wb.active
sheet2 = wb.create_sheet("nameWithoutEx")
sheet.title = 'fullName'
sheet['A' + str(row)] = 'dirs'
sheet['B' + str(row)] = 'files'
sheet2['A' + str(row)] = 'dirs'
sheet2['B' + str(row)] = 'files'


def searchDir(path):
    for adress, dirs, files in os.walk(path):
        list_name_directiry[adress.split('\\')[-1]] = files


def createListDel(dictName):
    for key, value in dictName.items():
        if value == []:
            delList.append(key)

def main():
    searchDir(path_to_directory)
    createListDel(list_name_directiry)
    row = 1
    for key in delList:
        del list_name_directiry[key]
    # С расширением файлов и без
    for key, values in list_name_directiry.items():
        sheet['A' + str(int(row+1))] = key
        sheet2['A' + str(int(row + 1))] = key
        for i in range(0, len(values)):
            row += 1
            sheet['B' + str(row)] = values[i]
            sheet2['B' + str(row)] = '.'.join(values[i].split('.')[0:-1])
    wb.save(filename)


if __name__ == '__main__':
    main()