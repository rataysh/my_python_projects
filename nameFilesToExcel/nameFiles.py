import os
from openpyxl import Workbook


names_xls = []
path_to_directory = input(f'Введите путь к папке начала сбора наименований:')
filename = 'name_all_files_in_directory.xlsx'

list_name_directiry = {}
listDir = []
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



def createLidtDir(path):
    for adress, dirs, files in os.walk(path):
    ##Создаем масив с директориями
        for dir in dirs:
            listDir.append(f"{adress}\\{dir}")


def nameAndSizeForEachDir(path):
    ## Для каждой директории создаю список словарей {Имя: размер}
    for adress, dirs, files in os.walk(path):
        if len(files) > 0:
            list_name_directiry[adress.split('\\')[-1]] = [{file: os.stat(f'{adress}\\{file}').st_size} for file in files]


def main():
    createLidtDir(path_to_directory)
    for dir in listDir:
        nameAndSizeForEachDir(dir)
    row = 1
    # С расширением файлов и без
    for key, values in list_name_directiry.items():
        sheet['A' + str(int(row+1))], sheet2['A' + str(int(row + 1))] = key, key
        for i in range(0, len(values)):
            row += 1
            for k, v in values[i].items():
                sheet['B' + str(row)], sheet2['B' + str(row)] = k, '.'.join(k.split('.')[0:-1])
                sheet['C' + str(row)], sheet2['C' + str(row)] = str(round(v / (1024), 2))+ ' Kb', str(round(v / (1024), 2)) + ' Kb'

    wb.save(filename)


if __name__ == '__main__':
    main()