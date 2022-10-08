import re, os


def search(path, mask):
    '''Функция поиска файлов по маске в введенном пути'''
    for adress, dirs, files in os.walk(path):
        for file in files:
            if re.search(mask, file):
                output = (f'{adress}\{file}').replace('\\', '/')
                yield output