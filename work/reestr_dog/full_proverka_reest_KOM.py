import os, xlsxwriter, openpyxl, time
import pandas as pd
import xml.etree.ElementTree as ET


start_time = time.time()
name_column_dog = 'Номер договора купли продажи КОМ (02)'
"""Путь к папке с xml дельтами"""
path_to_directory_delta = r""
path_to_directory_m = r""
path_to_directory_m_minus_1 = r""
path_to_RIO = r""

reestr_m_df_plus = pd.DataFrame()
reestr_m_df_minus = pd.DataFrame()
reestr_m_df_full = pd.DataFrame()
xml_df_plus_ngo = pd.DataFrame()
xml_df_minus_ngo = pd.DataFrame()
xml_df_plus = pd.DataFrame()
xml_df_minus = pd.DataFrame()
reestr_m_df_plus_ngo = pd.DataFrame()
reestr_m_df_minus_ngo = pd.DataFrame()
reestr_m_df_full_ngo = pd.DataFrame()
serch_delta_minus = 'ats_reestr_minus'
serch_NGO = 'KOM_NGO'
serch_NGO_minus = 'KOM_NGO_ats_reestr_minus'


 # # # Наименивание файла
now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
name_xlsx_file_reesrt_data = 'Proverka_KOM_01_'
name_xlsx_file_xml_delta = 'xml_delta_11_'
filename_reestr_data = f'{name_xlsx_file_reesrt_data}{now}.xlsx'
filename_xml_delta = f'{name_xlsx_file_xml_delta}{now}.xlsx'
'''Пернеменная для пути к файлу с xml'''
path_to_xml_delta_data = f'{name_xlsx_file_xml_delta}{now}.xlsx'


def search():
    '''Функция для прохода по всем файлам в введенном пути'''
    for adress, dirs, files in os.walk(path_to_directory_delta):
        for file in files:
            if file[-9:] == '.info.xml':  # Критери исключений из поиска
                continue
            elif file[-4:] != '.xml':
                continue
            else:
                output = (f'{adress}\{file}').replace('\\', '/')
                # names_xls.append(output)
            yield output


'''Проверка на отсутствия ДЕЛЬТЫ + в m-1 В НГО'''
reestr_m_df_plus_ngo = pd.read_excel(path_to_directory_m, sheet_name='plus_NGO')
reestr_m_minus_1_df_ngo = pd.read_excel(path_to_directory_m_minus_1, sheet_name='itog_full_NGO')
kolichestvo_delta_plus_ngo = len(reestr_m_df_plus_ngo[name_column_dog])
kolichestvo_m_minus_1_full_ngo = len(reestr_m_minus_1_df_ngo[name_column_dog])
### Проверяем каждый дог. из дельты + в полном реестре m-1 (создаю новую переменную proverka_test для удобства)
proverka_test = reestr_m_minus_1_df_ngo[name_column_dog].isin(reestr_m_df_plus_ngo[name_column_dog]).sum()
if proverka_test == 0:
    print(f'Все корректно!\t(Дельты плюс НГО месяца m не найдены в месяце m-1)')
else:
    print(f'ОШИБКА!!!\t(В месяце m-1  НГО обнаружен договор из дельты плюс месяца m)')


'''Проверка на наличие ДЕЛЬТЫ - в m-1 и соответсвия количества В НГО'''
reestr_m_df_minus_ngo = pd.read_excel(path_to_directory_m, sheet_name='minus_NGO')
kolichestvo_delta_minus_ngo = len(reestr_m_df_minus_ngo['Номер договора купли продажи КОМ'])
proverka_test = reestr_m_minus_1_df_ngo[name_column_dog].isin(reestr_m_df_minus_ngo['Номер договора купли продажи КОМ']).sum()
if proverka_test == kolichestvo_delta_minus_ngo:
    print(f'Все корректно!\t(В месяце m-1  НГО найдено {kolichestvo_delta_minus_ngo} договоров из дельты минус)')
else:
    print(f'ОШИБКА НГО!!!\t(Проверить количество и наличие договоров из дельты минус в реестре m-1)')


'''Проверка количества В НГО'''
reestr_m_df_full_ngo = pd.read_excel(path_to_directory_m, sheet_name='full_NGO')
kolichestvo_m_full_ngo = len(reestr_m_df_full_ngo[name_column_dog])
if kolichestvo_m_full_ngo == kolichestvo_m_minus_1_full_ngo-kolichestvo_delta_minus_ngo+kolichestvo_delta_plus_ngo:
    print(f'Из количество договор в m-1 {kolichestvo_m_minus_1_full_ngo} '
      f'вычитаем количество дельта минус {kolichestvo_delta_minus_ngo} '
      f'и прибавляем количество дельта плюс {kolichestvo_delta_plus_ngo} '
      f'получаем {kolichestvo_m_minus_1_full_ngo - kolichestvo_delta_minus_ngo + kolichestvo_delta_plus_ngo}'
      f'\nРезультат сравниваем с количеством дог в m {kolichestvo_m_full_ngo}')
else:
    print('ОШИБКА, количество не сошлось')


'''Проверка на отсутствия ДЕЛЬТЫ + в m-1'''
reestr_m_df_plus = pd.read_excel(path_to_directory_m, sheet_name='plus')
reestr_m_minus_1_df = pd.read_excel(path_to_directory_m_minus_1, sheet_name='itog_full')
kolichestvo_delta_plus = len(reestr_m_df_plus[name_column_dog])
kolichestvo_m_minus_1_full = len(reestr_m_minus_1_df[name_column_dog])
### Проверяем каждый дог. из дельты + в полном реестре m-1 (создаю новую переменную proverka_test для удобства)
proverka_test = reestr_m_minus_1_df[name_column_dog].isin(reestr_m_df_plus[name_column_dog]).sum()
if proverka_test == 0:
    print(f'Все корректно!\t(Дельты плюс месяца m не найдены в месяце m-1)')
else:
    print(f'ОШИБКА!!!\t(В месяце m-1 обнаружен договор из дельты плюс месяца m)')


'''Проверка на наличие ДЕЛЬТЫ - в m-1 и соответсвия количества'''
reestr_m_df_minus = pd.read_excel(path_to_directory_m, sheet_name='minus')
kolichestvo_delta_minus = len(reestr_m_df_minus['Номер договора купли продажи КОМ'])
proverka_test = reestr_m_minus_1_df[name_column_dog].isin(reestr_m_df_minus['Номер договора купли продажи КОМ']).sum()
if proverka_test == kolichestvo_delta_minus:
    print(f'Все корректно!\t(В месяце m-1 найдено {kolichestvo_delta_minus} договоров из дельты минус)')
else:
    print(f'ОШИБКА!!!\t(Проверить количество и наличие договоров из дельты минус в реестре m-1)')


'''Проверка количества'''
reestr_m_df_full = pd.read_excel(path_to_directory_m, sheet_name='full')
kolichestvo_m_full = len(reestr_m_df_full[name_column_dog])
if kolichestvo_m_full == kolichestvo_m_minus_1_full-kolichestvo_delta_minus+kolichestvo_delta_plus:
    print(f'Из количество договор в m-1 {kolichestvo_m_minus_1_full} '
      f'вычитаем количество дельта минус {kolichestvo_delta_minus} '
      f'и прибавляем количество дельта плюс {kolichestvo_delta_plus} '
      f'получаем {kolichestvo_m_minus_1_full-kolichestvo_delta_minus+kolichestvo_delta_plus}'
      f'\nРезультат сравниваем с количеством дог в m {kolichestvo_m_full}')
else:
    print(f'Из количество договор в m-1 {kolichestvo_m_minus_1_full} '
          f'вычитаем количество дельта минус {kolichestvo_delta_minus} '
          f'и прибавляем количество дельта плюс {kolichestvo_delta_plus} '
          f'получаем {kolichestvo_m_minus_1_full - kolichestvo_delta_minus + kolichestvo_delta_plus}'
          f'\nРезультат сравниваем с количеством дог в m {kolichestvo_m_full}')
    print('ОШИБКА, количество не сошлось')



### Вторая часть проверки (создание файла из xml дельт)
df_child_data_minus = pd.DataFrame()
df_root_data_minus = pd.DataFrame()
df_child_data_plus = pd.DataFrame()
df_root_data_plus = pd.DataFrame()
df_result_minus = pd.DataFrame()
df_child_data_minus_NGO = pd.DataFrame()
df_root_data_minus_NGO = pd.DataFrame()
df_child_data_plus_NGO = pd.DataFrame()
df_root_data_plus_NGO = pd.DataFrame()

for i in search():
    # print('_'.join(i.split('/')[-1].split('_')[1:4]))
    # print(i)
    if '_'.join(i.split('/')[-1].split('_')[0:2]) == serch_NGO:
        if '_'.join(i.split('/')[-1].split('_')[0:5]) == serch_NGO_minus:
            tree = ET.parse(i)
            root = tree.getroot()
            # Получаем метку и аттрибуты файла(тип Словарь)
            root_attribut = root.attrib
            # Получаем метку и аттрибуты ниже в дереве
            for child in root:
                file_df_NGO = pd.DataFrame(data=child.attrib, index=child.attrib)
                file_df_NGO['name_file'] = i.split('/')[-1]
                df_child_data_minus_NGO = df_child_data_minus_NGO.append(file_df_NGO)
                file_df_2_NGO = pd.DataFrame(data=root_attribut, index=root_attribut)
                file_df_2_NGO['name_file'] = i.split('/')[-1]
                df_root_data_minus_NGO = df_root_data_minus_NGO.append(file_df_2_NGO)
        else:
            tree = ET.parse(i)
            root = tree.getroot()
            root_attribut = root.attrib
            for child in root:
                file_df_NGO = pd.DataFrame(data=child.attrib, index=child.attrib)
                file_df_NGO['name_file'] = i.split('/')[-1]
                df_child_data_plus_NGO = df_child_data_plus_NGO.append(file_df_NGO)
                file_df_2_NGO = pd.DataFrame(data=root_attribut, index=root_attribut)
                file_df_2_NGO['name_file'] = i.split('/')[-1]
                df_root_data_plus_NGO = df_root_data_plus_NGO.append(file_df_2_NGO)
    else:
        if '_'.join(i.split('/')[-1].split('_')[1:4]) == serch_delta_minus:
            # Парсим корневые данные xml-файла
            tree = ET.parse(i)
            root = tree.getroot()
            # Получаем метку и аттрибуты файла(тип Словарь)
            root_attribut = root.attrib
            # Получаем метку и аттрибуты ниже в дереве
            for child in root:
                file_df = pd.DataFrame(data=child.attrib, index=child.attrib)
                file_df['name_file'] = i.split('/')[-1]
                df_child_data_minus = df_child_data_minus.append(file_df)
                file_df_2 = pd.DataFrame(data=root_attribut, index=root_attribut)
                file_df_2['name_file'] = i.split('/')[-1]
                df_root_data_minus = df_root_data_minus.append(file_df_2)
        else:
            tree = ET.parse(i)
            root = tree.getroot()
            root_attribut = root.attrib
            for child in root:
                file_df = pd.DataFrame(data=child.attrib, index=child.attrib)
                file_df['name_file'] = i.split('/')[-1]
                df_child_data_plus = df_child_data_plus.append(file_df)
                file_df_2 = pd.DataFrame(data=root_attribut, index=root_attribut)
                file_df_2['name_file'] = i.split('/')[-1]
                df_root_data_plus = df_root_data_plus.append(file_df_2)

### Для дельты минус xml оставляю уникальные по договору строки + соединяем df с root арибутами
df_child_data_minus = df_child_data_minus.drop_duplicates('contract-number', keep='last')
df_child_data_minus = df_child_data_minus.reset_index(drop=True)
df_root_data_minus = df_root_data_minus.drop_duplicates('name_file', keep='last')
df_root_data_minus = df_root_data_minus.reset_index(drop=True)
"""Тут используем правый join (merge) для того, чтобы файл выглядел идентично оригиналу"""
df_result_minus = df_root_data_minus.merge(df_child_data_minus, left_on='name_file', right_on='name_file', how='right')
df_result_minus = df_result_minus.drop('name_file', axis=1)

### Для дельты плюс xml оставляю уникальные по договору строки + соединяем df с root арибутами
df_child_data_plus = df_child_data_plus.drop_duplicates('contract-number', keep='last')
df_child_data_plus = df_child_data_plus.reset_index(drop=True)
df_root_data_plus = df_root_data_plus.drop_duplicates('name_file', keep='last')
df_root_data_plus = df_root_data_plus.reset_index(drop=True)
"""Тут используем правый join (merge) для того, чтобы файл выглядел идентично оригиналу"""
df_result_plus = df_root_data_plus.merge(df_child_data_plus, left_on='name_file', right_on='name_file', how='right')
df_result_plus = df_result_plus.drop('name_file', axis=1)


### Для дельт НГО xml оставляю уникальные по договору строки + соединяем df с root арибутами
df_child_data_minus_NGO = df_child_data_minus_NGO.drop_duplicates('contract-number', keep='last')
df_child_data_minus_NGO = df_child_data_minus_NGO.reset_index(drop=True)
df_root_data_minus_NGO = df_root_data_minus_NGO.drop_duplicates('name_file', keep='last')
df_root_data_minus_NGO = df_root_data_minus_NGO.reset_index(drop=True)
"""Тут используем правый join (merge) для того, чтобы файл выглядел идентично оригиналу"""
df_result_minus_NGO = df_root_data_minus_NGO.merge(df_child_data_minus_NGO, left_on='name_file', right_on='name_file', how='right')
df_result_minus_NGO = df_result_minus_NGO.drop('name_file', axis=1)


df_child_data_plus_NGO = df_child_data_plus_NGO.drop_duplicates('contract-number', keep='last')
df_child_data_plus_NGO = df_child_data_plus_NGO.reset_index(drop=True)
df_root_data_plus_NGO = df_root_data_plus_NGO.drop_duplicates('name_file', keep='last')
df_root_data_plus_NGO = df_root_data_plus_NGO.reset_index(drop=True)
"""Тут используем прывый join (merge) для того, чтобы файл выглядел идентично оригиналу"""
df_result_plus_NGO = df_root_data_plus_NGO.merge(df_child_data_plus_NGO, left_on='name_file', right_on='name_file', how='right')
df_result_plus_NGO = df_result_plus_NGO.drop('name_file', axis=1)




with pd.ExcelWriter(filename_xml_delta) as writer:
    df_result_plus.to_excel(writer, sheet_name='all_delta_plus_xml')
    df_result_minus.to_excel(writer, sheet_name='all_delta_minus_xml')
    df_result_plus_NGO.to_excel(writer, sheet_name='all_delta_plus_NGO_xml')
    df_result_minus_NGO.to_excel(writer, sheet_name='all_delta_minus_NGO_xml')


#
# ### Третья часть проверки (создание файла с дельта плюс совмещенными с РИО)
reestr_m_df_plus = pd.read_excel(path_to_directory_m, sheet_name='plus')
rio_df = pd.read_excel(path_to_RIO)
rio_change_df = rio_df.drop_duplicates('Код участника', keep='last')
df_data_reestr_plus = reestr_m_df_plus.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                            ]], left_on='Код ПРОДАВЦА(26)',
                                             right_on='Код участника', how='left')
df_data_reestr_plus = df_data_reestr_plus.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                               ]], left_on='Код ПОКУПАТЕЛЯ(27)',
                                                right_on='Код участника', how='left')
### Добавляем данные из xml
xml_df_plus = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_plus_xml')
df_data_reestr_plus = df_data_reestr_plus.merge(xml_df_plus[[
    'contract-number',
    'trader-supplier-code',
    'trader-supplier-name',
    'dpg-supplier-code',
    'contract-date',
    'trader-consumer-code',
    'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='contract-number', how='left')



reestr_m_df_minus = pd.read_excel(path_to_directory_m, sheet_name='minus')  # уже есть
reestr_m_minus_1_df = pd.read_excel(path_to_directory_m_minus_1, sheet_name='itog_full')  # уже есть
df_data_reestr_minus = reestr_m_df_minus.merge(reestr_m_minus_1_df[[
    'Номер договора купли продажи КОМ (02)',
    'Полн наимен ПРОДАВ в тв пад(06)',
    'Полн наимен ПОКУПАТ в тв пад(07)',
    'Дата заключения договора КОМ (03)',
    'Код ПРОДАВЦА(26)',
    'Код ПОКУПАТЕЛЯ(27)',
    'Срок нач пост мощн по дог КОМ(28)',
    'Год пост мощн по дог КОМ (29)',
    'Код ГТП ПРОДАВЦА (33)'
]], left_on='Номер договора купли продажи КОМ', right_on='Номер договора купли продажи КОМ (02)', how='left')
# ### Добавляем данные из RIO для проверки xml
# df_data_reestr_minus = df_data_reestr_minus.merge(rio_change_df[['Код участника',
#                                                   'Официал. наименование'
#                                                             ]], left_on='Код ПРОДАВЦА',
#                                              right_on='Код участника', how='left')
# df_data_reestr_minus = df_data_reestr_minus.merge(rio_change_df[['Код участника',
#                                                   'Официал. наименование'
#                                                             ]], left_on='Код ПОКУПАТЕЛЯ',
#                                              right_on='Код участника', how='left')
### Добавляем данные из xml
xml_df_minus = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_minus_xml')
df_data_reestr_minus = df_data_reestr_minus.merge(xml_df_minus[[
    'contract-number',
    'trader-supplier-code',
    'trader-supplier-name',
    'dpg-supplier-code',
    'contract-date',
    'trader-consumer-code',
    'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ', right_on='contract-number', how='left')



reestr_m_df_full = pd.read_excel(path_to_directory_m, sheet_name='full') # Уже есть
df_data_reestr_full = reestr_m_df_full.merge(reestr_m_minus_1_df[[
    'Номер договора купли продажи КОМ (02)',
    'Дата заключения договора КОМ (03)',
    'Срок нач пост мощн по дог КОМ(28)',
    'Год пост мощн по дог КОМ (29)',
    'Краткий номер дог КП КОМ(30)',
    'Код ГТП ПРОДАВЦА (33)'
    # 'Флаг:\n0 - договоры пред. расч. месяца;\n1 - договоры расч. месяца'
    # 'Тип договора:\n1- договор по введ. объектам,\n2 – договор по неввед. объектам, 3 – договор по объектам из перечня РП РФ 2699'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='Номер договора купли продажи КОМ (02)', how='left')

df_data_reestr_full = df_data_reestr_full.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                            ]], left_on='Код ПРОДАВЦА(26)',
                                             right_on='Код участника', how='left')
### Для ФСК меняю код "10001004" на FSKEESRU, для корректного заполнения
df_data_reestr_full['Код ПОКУПАТЕЛЯ(27)'] = df_data_reestr_full['Код ПОКУПАТЕЛЯ(27)'].replace('10001004', 'FSKEESRU')
df_data_reestr_full = df_data_reestr_full.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                               ]], left_on='Код ПОКУПАТЕЛЯ(27)',
                                                right_on='Код участника', how='left')
### Для ФСК меняю обратно на "10001004", для корректного заполнения
df_data_reestr_full['Код ПОКУПАТЕЛЯ(27)'] = df_data_reestr_full['Код ПОКУПАТЕЛЯ(27)'].replace('FSKEESRU', '10001004')
### Добавляем данные из xml
df_data_reestr_full = df_data_reestr_full.merge(xml_df_plus[[
    'contract-number'
    # 'trader-supplier-code',
    # 'trader-supplier-name',
    # 'dpg-supplier-code',
    # 'contract-date',
    # 'trader-consumer-code',
    # 'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='contract-number', how='left')



### Данные для НГО
reestr_m_df_plus_ngo = pd.read_excel(path_to_directory_m, sheet_name='plus_NGO')
rio_df = pd.read_excel(path_to_RIO)
rio_change_df = rio_df.drop_duplicates('Код участника', keep='last')
df_data_reestr_plus_ngo = reestr_m_df_plus_ngo.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                                    ]], left_on='Код ПРОДАВЦА(26)',
                                                     right_on='Код участника', how='left')
df_data_reestr_plus_ngo = df_data_reestr_plus_ngo.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                                       ]], left_on='Код ПОКУПАТЕЛЯ(27)',
                                                        right_on='Код участника', how='left')
xml_df_plus_ngo = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_plus_NGO_xml')
df_data_reestr_plus_ngo = df_data_reestr_plus_ngo.merge(xml_df_plus_ngo[[
    'contract-number',
    'trader-supplier-code',
    'trader-supplier-name',
    'dpg-supplier-code',
    'delivery-start-date',
    'trader-consumer-code',
    'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='contract-number', how='left')



reestr_m_df_minus_ngo = pd.read_excel(path_to_directory_m, sheet_name='minus_NGO')  # уже есть
reestr_m_minus_1_df_ngo = pd.read_excel(path_to_directory_m_minus_1, sheet_name='itog_full_NGO')  # уже есть
df_data_reestr_minus_ngo = reestr_m_df_minus_ngo.merge(reestr_m_minus_1_df_ngo[[
    'Номер договора купли продажи КОМ (02)',
    'Номер договора комм пред ПОКУПАТ (04)',
    'Номер договора комм пред ПРОДАВЦА (05)',
    'Полн наимен ПРОДАВ в тв пад(06)',
    'Полн наимен ПОКУПАТ в тв пад(07)',
    'Дата заключения договора КОМ (03)',
    'Код ПРОДАВЦА(26)',
    'Код ПОКУПАТЕЛЯ(27)',
    'Код ГТП ПРОДАВЦА (33)'
]], left_on='Номер договора купли продажи КОМ', right_on='Номер договора купли продажи КОМ (02)', how='left')
xml_df_minus_ngo = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_minus_NGO_xml')
df_data_reestr_minus_ngo = df_data_reestr_minus_ngo.merge(xml_df_minus_ngo[[
    'contract-number',
    'trader-supplier-code',
    'trader-supplier-name',
    'dpg-supplier-code',
    'delivery-start-date',
    'trader-consumer-code',
    'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ', right_on='contract-number', how='left')



reestr_m_df_full_ngo = pd.read_excel(path_to_directory_m, sheet_name='full_NGO') # Уже есть
df_data_reestr_full_ngo = reestr_m_df_full_ngo.merge(reestr_m_minus_1_df_ngo[[
    'Номер договора купли продажи КОМ (02)',
    'Дата заключения договора КОМ (03)',
    'Срок нач пост мощн по дог КОМ(28)',
    'Краткий номер дог КП КОМ(30)',
    'Код ГТП ПРОДАВЦА (33)'
    # 'Флаг:\n0 - договоры пред. расч. месяца;\n1 - договоры расч. месяца'
    # 'Тип договора:\n1- договор по введ. объектам,\n2 – договор по неввед. объектам, 3 – договор по объектам из перечня РП РФ 2699'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='Номер договора купли продажи КОМ (02)', how='left')

df_data_reestr_full_ngo = df_data_reestr_full_ngo.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                                       ]], left_on='Код ПРОДАВЦА(26)',
                                                        right_on='Код участника', how='left')
### Для ФСК меняю код "10001004" на FSKEESRU, для корректного заполнения
df_data_reestr_full_ngo['Код ПОКУПАТЕЛЯ(27)'] = df_data_reestr_full_ngo['Код ПОКУПАТЕЛЯ(27)'].replace('10001004', 'FSKEESRU')
df_data_reestr_full_ngo = df_data_reestr_full_ngo.merge(rio_change_df[['номер договора ком представ',
                                                  'Официал. наим твор падеж',
                                                  'номер ДОП',
                                                  'дата ДОП',
                                                  'Официал. наименование',
                                                  'адрес юр лица по ЕГРЮЛ',
                                                  'почт адрес',
                                                  'ИНН',
                                                  'КПП',
                                                  'Код участника',
                                                  'дата договора ком представ'
                                                                       ]], left_on='Код ПОКУПАТЕЛЯ(27)',
                                                        right_on='Код участника', how='left')
### Для ФСК меняю обратно на "10001004", для корректного заполнения
df_data_reestr_full_ngo['Код ПОКУПАТЕЛЯ(27)'] = df_data_reestr_full_ngo['Код ПОКУПАТЕЛЯ(27)'].replace('FSKEESRU', '10001004')
df_data_reestr_full_ngo = df_data_reestr_full_ngo.merge(xml_df_plus_ngo[[
    'contract-number'
    # 'trader-supplier-code',
    # 'trader-supplier-name',
    # 'dpg-supplier-code',
    # 'delivery-start-date',
    # 'trader-consumer-code',
    # 'trader-consumer-name'
]], left_on='Номер договора купли продажи КОМ (02)', right_on='contract-number', how='left')






with pd.ExcelWriter(filename_reestr_data) as writer:
    df_data_reestr_full.to_excel(writer, sheet_name='data_full')
    df_data_reestr_plus.to_excel(writer, sheet_name='data_plus')
    df_data_reestr_minus.to_excel(writer, sheet_name='data_minus')
    df_data_reestr_full_ngo.to_excel(writer, sheet_name='data_full_NGO')
    df_data_reestr_plus_ngo.to_excel(writer, sheet_name='data_plus_NGO')
    df_data_reestr_minus_ngo.to_excel(writer, sheet_name='data_minus_NGO')






finish_time = time.time() - start_time
print(f'Скрипт работал {finish_time} секунд')