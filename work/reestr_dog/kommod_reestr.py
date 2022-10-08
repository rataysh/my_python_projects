import os, xlsxwriter, openpyxl, time
import pandas as pd


start_time = time.time()
names_xls = []
filename = f'KOMMOD.xlsx'
path = r''


def search(path_to_dir):
    '''Функция для прохода по всем файлам в введенном пути'''
    for adress, dirs, files in os.walk(path_to_dir):     #path_to_directory):
        for file in files:
            if '_'.join(file.split('_')[2:5]) != 'check_reestr_all':  # Критери исключений из поиска
                continue
            else:
                output = (f'{adress}\{file}').replace('\\', '/')
                names_xls.append(output)
            yield output

kommod_reest_df = pd.DataFrame()
worksheets_df = [] ### Список для всех датафреймов в файле
for i in search(path):
    file_df = pd.ExcelFile(i) ### НЕ read_excel т.к. нам нужно получить наименования листов
    worksheets = file_df.sheet_names
    for worksheet in worksheets:
        if worksheet == 'Лист1':
            test_data_df = pd.read_excel(i, sheet_name=worksheet)
            test_data_df = test_data_df[3:]
            worksheets_df.append(test_data_df)
        else:
            test_data_df = pd.read_excel(i, sheet_name=worksheet)
            test_data_df = test_data_df[4:]
            worksheets_df.append(test_data_df)

filtr_value = '№ п\\п'
filtr_column = '№ п\\п'
kommod_reest_df = pd.concat(worksheets_df)
kommod_reest_df.columns = kommod_reest_df.iloc[0]
kommod_reest_df = kommod_reest_df.reset_index(drop=True)
kommod_reest_df = kommod_reest_df[kommod_reest_df[filtr_column] != filtr_value]
with pd.ExcelWriter(filename) as writer:
    kommod_reest_df.to_excel(writer, sheet_name='all_GTP')


finish_time = time.time() - start_time
print(finish_time)