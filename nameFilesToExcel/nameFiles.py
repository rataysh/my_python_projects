import os
from openpyxl import Workbook

names_xls = []
path_to_directory = input(f'Enter the start directory:')
filename = 'name_all_files_in_directory.xlsx'

list_name_directiry = {}
row = 1
wb = Workbook()
sheet = wb.active
sheet2 = wb.create_sheet("nameWithoutEx")
sheet.title = 'fullName'
sheet['A' + str(row)] = 'dirs'
sheet['B' + str(row)] = 'files'
sheet['C' + str(row)] = 'size'
sheet2['A' + str(row)] = 'dirs'
sheet2['B' + str(row)] = 'files'
sheet2['C' + str(row)] = 'size'


def createListDir(path):
    for adress, dirs, files in os.walk(path):
        if files != []:
            list_name_directiry[adress] = files


def main():
    createListDir(path_to_directory)
    ## добавляю полный путь к каждому файлу
    for key, values in list_name_directiry.items():
        for i in range(0, len(values)):
            list_name_directiry[key][i] = key + '\\' + values[i]
    ## добавляю размер к каждому файлу
    for key, values in list_name_directiry.items():
        for i in range(0, len(values)):
            list_name_directiry[key][i] = [values[i], os.stat(values[i]).st_size]
    ## go to excel
    row = 1
    for key, values in list_name_directiry.items():
        sheet['A' + str(int(row + 1))], sheet2['A' + str(int(row + 1))] = key.split('\\')[-1], key.split('\\')[-1]
        for i in range(0, len(values)):
            row += 1
            sheet['B' + str(row)], sheet2['B' + str(row)] \
                = values[i][0].split('\\')[-1], ''.join(values[i][0].split('\\')[-1].split('.')[:-1])
            sheet['C' + str(row)], sheet2['C' + str(row)] = str(round(values[i][1] / (1024), 2)) + ' Kb', str(
            round(values[i][1] / (1024), 2)) + ' Kb'

    wb.save(filename)


if __name__ == '__main__':
    main()
