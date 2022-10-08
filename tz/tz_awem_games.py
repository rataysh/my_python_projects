import os, re, xlsxwriter, openpyxl
import pandas as pd


## Парсим файл и содаем из него DataFrame
path = r'C:\Users\armay\Desktop\awem'
mask = 'Game'


def search(path, mask):
    '''Функция поиска файлов по маске в введенном пути'''
    for adress, dirs, files in os.walk(path):
        for file in files:
            if re.search(mask, file):
                output = (f'{adress}\{file}').replace('\\', '/')
                yield output


try:
    for i in search(path, mask):
        # на основании CSV файла создаем Dataframe
        df_data_game_analyst = pd.read_csv(i)
        # убираем данные по игрокам меньше 4 уровня т.к. тестируемые изменения только с 4 уровня
        df_change = df_data_game_analyst[df_data_game_analyst['Level'] > 4]
        # Создаем dataframe для каждой версии
        df_ver_1 = df_change[df_change['Version'] == 'v1']
        df_ver_2 = df_change[df_change['Version'] != 'v1']
        # Собираем статистику по столбцам
        disc_1 = df_ver_1.describe()
        disc_2 = df_ver_2.describe()
        df_ver_1.loc['Sum', :] = df_ver_1.sum(axis=0)
        df_ver_2.loc['Sum', :] = df_ver_2.sum(axis=0)
        # Конкатинируем статистику в конец таблицы
        df_ver_1 = pd.concat([df_ver_1, disc_1], axis=0, join='outer')
        df_ver_2 = pd.concat([df_ver_2, disc_2], axis=0, join='outer')
except ValueError:
    print(f'Произошла ошибка')
finally:
    with pd.ExcelWriter('awem_change.xlsx') as writer:
        df_change.to_excel(writer, sheet_name='data_full')
        df_ver_1.to_excel(writer, sheet_name='ver1')
        df_ver_2.to_excel(writer, sheet_name='ver2')
        df_statistic
    print('Данные собраны')
