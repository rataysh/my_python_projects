import os, xlsxwriter, openpyxl, time
import pandas as pd


start_time = time.time()
names_xls = []
choice_calculation = input('Если КОМ - 1\nЕсли ВР - 2\nВыбирите расчет:\n')
path_to_directory = r'' #input('Введите путь старта:\n')
schetchik = 0
schetchik_reestr = 0
schetchik_reestr_itog = 0
schetchik_other = 0
filtr_reestr = 'Реестр'
filtr_reestr_full = '(полный)'
filtr_reestr_plus = '(дельта)'
filtr_reestr_NGO = 'НГО'
filtr_reestr_itog = 'Итоговый'
df_reestr_full = pd.DataFrame()
df_reestr_plus = pd.DataFrame()
df_reestr_minus = pd.DataFrame()
df_reestr_itog_full = pd.DataFrame()
df_reestr_itog_plus = pd.DataFrame()
df_reestr_full_NGO = pd.DataFrame()
df_reestr_plus_NGO = pd.DataFrame()
df_reestr_minus_NGO = pd.DataFrame()
df_reestr_itog_full_NGO = pd.DataFrame()
df_reestr_itog_plus_NGO = pd.DataFrame()



def search():
    '''Функция для прохода по всем файлам в введенном пути'''
    for adress, dirs, files in os.walk(path_to_directory):
        for file in files:
            if file[-9:] == '.info.xml' or file[-4:] == '.xml':  # Критери исключений из поиска
                continue
            else:
                output = (f'{adress}\{file}').replace('\\', '/')
                names_xls.append(output)
            yield output


if choice_calculation == '1':
    name_xlsx_file = 'reestr_KOM_'
    try:
        for i in search():
            df_result = pd.DataFrame()
            # print(i.split('/')[-1].split('_')[4].split()[3])
            schetchik += 1
            if i.split('/')[-1].split('_')[4].split()[0] == filtr_reestr:
                if i.split('/')[-1].split('_')[4].split()[3] == filtr_reestr_NGO:
                    if i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_full:
                        df_result = pd.read_excel(i, header=None, skiprows=1)
                        df_result[34] = i.split('/')[-1]
                        df_reestr_full_NGO = df_result.append(df_reestr_full_NGO, sort=False)
                    elif i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_plus:
                        df_result = pd.read_excel(i, header=None, skiprows=1)
                        df_result[33] = i.split('/')[-1]
                        df_reestr_plus_NGO = df_result.append(df_reestr_plus_NGO, sort=False)
                    else:
                        df_result = pd.read_excel(i, header=None, skiprows=5)
                        df_result[11] = i.split('/')[-1]
                        df_reestr_minus_NGO = df_result.append(df_reestr_minus_NGO, sort=False)
                elif i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_full:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[36] = i.split('/')[-1]
                    df_reestr_full = df_result.append(df_reestr_full, sort=False)
                elif i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_plus:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[34] = i.split('/')[-1]
                    df_reestr_plus = df_result.append(df_reestr_plus, sort=False)
                else:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[11] = i.split('/')[-1]
                    df_reestr_minus = df_result.append(df_reestr_minus, sort=False)
                schetchik_reestr += 1
            elif i.split('/')[-1].split('_')[4].split()[0] == filtr_reestr_itog:
                if i.split('/')[-1].split('_')[4].split()[4] == filtr_reestr_NGO:
                    if i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_full:
                        df_result = pd.read_excel(i, header=None, skiprows=1)
                        df_result[34] = i.split('/')[-1]
                        df_reestr_itog_full_NGO = df_result.append(df_reestr_itog_full_NGO, sort=False)
                    else:
                        df_result = pd.read_excel(i, header=None, skiprows=1)
                        df_result[33] = i.split('/')[-1]
                        df_reestr_itog_plus_NGO = df_result.append(df_reestr_itog_plus_NGO, sort=False)
                elif i.split('/')[-1].split('_')[4].split()[-1] == filtr_reestr_full:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[36] = i.split('/')[-1]
                    df_reestr_itog_full = df_result.append(df_reestr_itog_full, sort=False)
                else:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[34] = i.split('/')[-1]
                    df_reestr_itog_plus = df_result.append(df_reestr_itog_plus, sort=False)
                schetchik_reestr_itog += 1
            else:
                schetchik_other += 1

        # # # Фильтр если понадобится
        if schetchik_reestr > 0 and schetchik_reestr_itog > 0:
            filtr1 = "Номер договора купли продажи КОМ (02)"
            filtr2 = 3
            df_reestr_full.columns = df_reestr_full.iloc[0]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_full = df_reestr_full.reset_index(drop=True)

            df_reestr_plus.columns = df_reestr_plus.iloc[0]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_plus = df_reestr_plus.reset_index(drop=True)

            df_reestr_full_NGO.columns = df_reestr_full_NGO.iloc[0]
            df_reestr_full_NGO = df_reestr_full_NGO[
                df_reestr_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_full_NGO = df_reestr_full_NGO[
                df_reestr_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_full_NGO = df_reestr_full_NGO.reset_index(drop=True)

            df_reestr_plus_NGO.columns = df_reestr_plus_NGO.iloc[0]
            df_reestr_plus_NGO = df_reestr_plus_NGO[
                df_reestr_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_plus_NGO = df_reestr_plus_NGO[
                df_reestr_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_plus_NGO = df_reestr_plus_NGO.reset_index(drop=True)

            # # # Для дельта минус другой фильтр
            filtr1 = "Номер договора купли продажи КОМ"
            df_reestr_minus.columns = df_reestr_minus.iloc[0]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи КОМ"] != filtr1]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи КОМ"] != filtr2]
            df_reestr_minus = df_reestr_minus.reset_index(drop=True)

            df_reestr_minus_NGO.columns = df_reestr_minus_NGO.iloc[0]
            df_reestr_minus_NGO = df_reestr_minus_NGO[
                df_reestr_minus_NGO["Номер договора купли продажи КОМ"] != filtr1]
            df_reestr_minus_NGO = df_reestr_minus_NGO[
                df_reestr_minus_NGO["Номер договора купли продажи КОМ"] != filtr2]
            df_reestr_minus_NGO = df_reestr_minus_NGO.reset_index(drop=True)

            filtr1 = "Номер договора купли продажи КОМ (02)"
            filtr2 = 3
            df_reestr_itog_full.columns = df_reestr_itog_full.iloc[0]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_full = df_reestr_itog_full.reset_index(drop=True)

            df_reestr_itog_plus.columns = df_reestr_itog_plus.iloc[0]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_plus = df_reestr_itog_plus.reset_index(drop=True)

            df_reestr_itog_full_NGO.columns = df_reestr_itog_full_NGO.iloc[0]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO[
                df_reestr_itog_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO[
                df_reestr_itog_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO.reset_index(drop=True)

            df_reestr_itog_plus_NGO.columns = df_reestr_itog_plus_NGO.iloc[0]
            df_reestr_itog_plus_NGO.columns = df_reestr_itog_plus_NGO.iloc[0]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO[
                df_reestr_itog_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO[
                df_reestr_itog_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO.reset_index(drop=True)
        elif schetchik_reestr > 0:
            filtr1 = "Номер договора купли продажи КОМ (02)"
            filtr2 = 3
            df_reestr_full.columns = df_reestr_full.iloc[0]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_full = df_reestr_full.reset_index(drop=True)

            df_reestr_plus.columns = df_reestr_plus.iloc[0]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_plus = df_reestr_plus.reset_index(drop=True)

            df_reestr_full_NGO.columns = df_reestr_full_NGO.iloc[0]
            df_reestr_full_NGO = df_reestr_full_NGO[
                df_reestr_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_full_NGO = df_reestr_full_NGO[
                df_reestr_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_full_NGO = df_reestr_full_NGO.reset_index(drop=True)

            df_reestr_plus_NGO.columns = df_reestr_plus_NGO.iloc[0]
            df_reestr_plus_NGO = df_reestr_plus_NGO[
                df_reestr_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_plus_NGO = df_reestr_plus_NGO[
                df_reestr_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_plus_NGO = df_reestr_plus_NGO.reset_index(drop=True)

            # # # Для дельта минус другой фильтр
            filtr1 = "Номер договора купли продажи КОМ"
            df_reestr_minus.columns = df_reestr_minus.iloc[0]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи КОМ"] != filtr1]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи КОМ"] != filtr2]
            df_reestr_minus = df_reestr_minus.reset_index(drop=True)

            df_reestr_minus_NGO.columns = df_reestr_minus_NGO.iloc[0]
            df_reestr_minus_NGO = df_reestr_minus_NGO[
                df_reestr_minus_NGO["Номер договора купли продажи КОМ"] != filtr1]
            df_reestr_minus_NGO = df_reestr_minus_NGO[
                df_reestr_minus_NGO["Номер договора купли продажи КОМ"] != filtr2]
            df_reestr_minus_NGO = df_reestr_minus_NGO.reset_index(drop=True)
        else:
            filtr1 = "Номер договора купли продажи КОМ (02)"
            filtr2 = 3
            df_reestr_itog_full.columns = df_reestr_itog_full.iloc[0]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_full = df_reestr_itog_full.reset_index(drop=True)

            df_reestr_itog_plus.columns = df_reestr_itog_plus.iloc[0]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_plus = df_reestr_itog_plus.reset_index(drop=True)

            df_reestr_itog_full_NGO.columns = df_reestr_itog_full_NGO.iloc[0]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO[
                df_reestr_itog_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO[
                df_reestr_itog_full_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_full_NGO = df_reestr_itog_full_NGO.reset_index(drop=True)

            df_reestr_itog_plus_NGO.columns = df_reestr_itog_plus_NGO.iloc[0]
            df_reestr_itog_plus_NGO.columns = df_reestr_itog_plus_NGO.iloc[0]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO[
                df_reestr_itog_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr1]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO[
                df_reestr_itog_plus_NGO["Номер договора купли продажи КОМ (02)"] != filtr2]
            df_reestr_itog_plus_NGO = df_reestr_itog_plus_NGO.reset_index(drop=True)

        # # # Наименивание файла
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = f'{name_xlsx_file}{now}.xlsx'

        # # # Выбор кол-ва и наим. листов
        if schetchik_reestr > 0 and schetchik_reestr_itog > 0:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_full.to_excel(writer, sheet_name='full')
                df_reestr_plus.to_excel(writer, sheet_name='plus')
                df_reestr_minus.to_excel(writer, sheet_name='minus')
                df_reestr_full_NGO.to_excel(writer, sheet_name='full_NGO')
                df_reestr_plus_NGO.to_excel(writer, sheet_name='plus_NGO')
                df_reestr_minus_NGO.to_excel(writer, sheet_name='minus_NGO')
                df_reestr_itog_full.to_excel(writer, sheet_name='itog_full')
                df_reestr_itog_plus.to_excel(writer, sheet_name='itog_plus')
                df_reestr_itog_full_NGO.to_excel(writer, sheet_name='itog_full_NGO')
                df_reestr_itog_plus_NGO.to_excel(writer, sheet_name='itog_plus_NGO')
        elif schetchik_reestr > 0:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_full.to_excel(writer, sheet_name='full')
                df_reestr_plus.to_excel(writer, sheet_name='plus')
                df_reestr_minus.to_excel(writer, sheet_name='minus')
                df_reestr_full_NGO.to_excel(writer, sheet_name='full_NGO')
                df_reestr_plus_NGO.to_excel(writer, sheet_name='plus_NGO')
                df_reestr_minus_NGO.to_excel(writer, sheet_name='minus_NGO')
        else:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_itog_full.to_excel(writer, sheet_name='itog_full')
                df_reestr_itog_plus.to_excel(writer, sheet_name='itog_plus')
                df_reestr_itog_full_NGO.to_excel(writer, sheet_name='itog_full_NGO')
                df_reestr_itog_plus_NGO.to_excel(writer, sheet_name='itog_plus_NGO')
    except ValueError:
        print(f'Произошла ошибка через')
    finally:
        finish_time = time.time() - start_time
        print(f'файлов собрано {schetchik} за {finish_time} секунд')
        print(f'Предварительных {schetchik_reestr}')
        print(f'Итоговых {schetchik_reestr_itog}')
        print(f'Остальных {schetchik_other}')



elif choice_calculation == '2':
    name_xlsx_file = 'reestr_BP_'
    try:
        for i in search():
            df_result = pd.DataFrame()
            schetchik += 1
            # print(i.split('/')[-1].split('_')[5].split()[0])
            if i.split('/')[-1].split('_')[5].split()[0] == filtr_reestr:
                if i.split('/')[-1].split('_')[5].split()[-1] == filtr_reestr_full:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[30] = i.split('/')[-1]
                    df_reestr_full = df_result.append(df_reestr_full, sort=False)
                elif i.split('/')[-1].split('_')[5].split()[-1] == filtr_reestr_plus:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[29] = i.split('/')[-1]
                    df_reestr_plus = df_result.append(df_reestr_plus, sort=False)
                else:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[11] = i.split('/')[-1]
                    df_reestr_minus = df_result.append(df_reestr_minus, sort=False)
                schetchik_reestr += 1
            elif i.split('/')[-1].split('_')[5].split()[0] == filtr_reestr_itog:
                # print(i.split('/')[-1].split('_')[5].split()[-1])
                if i.split('/')[-1].split('_')[5].split()[-1] == filtr_reestr_full:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[30] = i.split('/')[-1]
                    df_reestr_itog_full = df_result.append(df_reestr_itog_full, sort=False)
                else:
                    df_result = pd.read_excel(i, header=None, skiprows=1)
                    df_result[29] = i.split('/')[-1]
                    df_reestr_itog_plus = df_result.append(df_reestr_itog_plus, sort=False)
                schetchik_reestr_itog += 1
            else:
                schetchik_other += 1

        # # # Фильтр если понадобится
        if schetchik_reestr > 0 and schetchik_reestr_itog > 0:
            filtr1 = "Номер договора купли продажи ВР(03)"
            df_reestr_full.columns = df_reestr_full.iloc[0]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_full = df_reestr_full.reset_index(drop=True)

            df_reestr_plus.columns = df_reestr_plus.iloc[0]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_plus = df_reestr_plus.reset_index(drop=True)

            df_reestr_minus.columns = df_reestr_minus.iloc[0]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_minus = df_reestr_minus.reset_index(drop=True)

            df_reestr_itog_full.columns = df_reestr_itog_full.iloc[0]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_itog_full = df_reestr_itog_full.reset_index(drop=True)

            df_reestr_itog_plus.columns = df_reestr_itog_plus.iloc[0]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_itog_plus = df_reestr_itog_plus.reset_index(drop=True)

        elif schetchik_reestr > 0:
            filtr1 = "Номер договора купли продажи ВР(03)"

            df_reestr_full.columns = df_reestr_full.iloc[0]
            df_reestr_full = df_reestr_full[
                df_reestr_full["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_full = df_reestr_full.reset_index(drop=True)

            df_reestr_plus.columns = df_reestr_plus.iloc[0]
            df_reestr_plus = df_reestr_plus[
                df_reestr_plus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_plus = df_reestr_plus.reset_index(drop=True)

            df_reestr_minus.columns = df_reestr_minus.iloc[0]
            df_reestr_minus = df_reestr_minus[
                df_reestr_minus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_minus = df_reestr_minus.reset_index(drop=True)
        else:
            filtr1 = "Номер договора купли продажи ВР(03)"
            df_reestr_itog_full.columns = df_reestr_itog_full.iloc[0]
            df_reestr_itog_full = df_reestr_itog_full[
                df_reestr_itog_full["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_itog_full = df_reestr_itog_full.reset_index(drop=True)

            df_reestr_itog_plus.columns = df_reestr_itog_plus.iloc[0]
            df_reestr_itog_plus = df_reestr_itog_plus[
                df_reestr_itog_plus["Номер договора купли продажи ВР(03)"] != filtr1]
            df_reestr_itog_plus = df_reestr_itog_plus.reset_index(drop=True)



        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = f'{name_xlsx_file}{now}.xlsx'

        if schetchik_reestr > 0 and schetchik_reestr_itog > 0:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_full.to_excel(writer, sheet_name='full')
                df_reestr_plus.to_excel(writer, sheet_name='plus')
                df_reestr_minus.to_excel(writer, sheet_name='minus')
                df_reestr_itog_full.to_excel(writer, sheet_name='itog_full')
                df_reestr_itog_plus.to_excel(writer, sheet_name='itog_plus')
        elif schetchik_reestr > 0:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_full.to_excel(writer, sheet_name='full')
                df_reestr_plus.to_excel(writer, sheet_name='plus')
                df_reestr_minus.to_excel(writer, sheet_name='minus')
        else:
            with pd.ExcelWriter(filename) as writer:
                df_reestr_itog_full.to_excel(writer, sheet_name='itog_full')
                df_reestr_itog_plus.to_excel(writer, sheet_name='itog_plus')

    except ValueError:
        print(f'Произошла ошибка через')
    finally:
        finish_time = time.time() - start_time
        print(f'файлов собрано {schetchik} за {finish_time} секунд')
        print(f'Предварительных {schetchik_reestr}')
        print(f'Итоговых {schetchik_reestr_itog}')
        print(f'Остальных {schetchik_other}')
else:
    print('Вы ввели некорректное значение, перезапустите скрипт и будте внимательнее!')
