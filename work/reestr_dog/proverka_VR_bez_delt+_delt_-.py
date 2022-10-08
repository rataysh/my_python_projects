import os, xlsxwriter, openpyxl, time
import pandas as pd
import xml.etree.ElementTree as ET


start_time = time.time()
name_column_dog = 'Номер договора купли продажи ВР(03)'
"""Путь к папке с xml дельтами"""
path_to_directory = r""
path_to_directory_m = r""
path_to_directory_m_minus_1 = r""
path_to_RIO = r""
reestr_m_df_plus = pd.DataFrame()
reestr_m_df_minus = pd.DataFrame()
reestr_m_df_full = pd.DataFrame()
xml_df_plus = pd.DataFrame()
serch_delta_minus = 'ats_reestr_minus'

 # # # Наименивание файла
now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
name_xlsx_file_reesrt_plus = 'Proverka_VR_01_'
name_xlsx_file_xml_delta = 'xml_delta_12_'
filename_reestr_plus = f'{name_xlsx_file_reesrt_plus}{now}.xlsx'
filename_xml_delta = f'{name_xlsx_file_xml_delta}{now}.xlsx'
'''Пернеменная для пути к файлу с xml'''
path_to_xml_delta_data = f'{name_xlsx_file_xml_delta}{now}.xlsx'



def search():
    '''Функция для прохода по всем файлам в введенном пути'''
    for adress, dirs, files in os.walk(path_to_directory):
        for file in files:
            if file[-9:] == '.info.xml':  # Критери исключений из поиска
                continue
            elif file[-4:] != '.xml':
                continue
            else:
                output = (f'{adress}\{file}').replace('\\', '/')
                # names_xls.append(output)
            yield output


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
kolichestvo_delta_minus = len(reestr_m_df_minus[name_column_dog])
proverka_test = reestr_m_minus_1_df[name_column_dog].isin(reestr_m_df_minus[name_column_dog]).sum()
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
for i in search():
    # print('_'.join(i.split('/')[-1].split('_')[1:4]))
    # print(i)
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

# ### Для дельты минус xml оставляю уникальные по договору строки + соединяем df с root арибутами
# df_child_data_minus = df_child_data_minus.drop_duplicates('contract-number', keep='last')
# df_child_data_minus = df_child_data_minus.reset_index(drop=True)
# df_root_data_minus = df_root_data_minus.drop_duplicates('name_file', keep='last')
# df_root_data_minus = df_root_data_minus.reset_index(drop=True)
# """Тут используем прывый join (merge) для того, чтобы файл выглядил идентично оригиналу"""
# df_result_minus = df_root_data_minus.merge(df_child_data_minus, left_on='name_file', right_on='name_file', how='right')
# df_result_minus = df_result_minus.drop('name_file', axis=1)
#
# ### Для дельты минус xml оставляю уникальные по договору строки + соединяем df с root арибутами
# df_child_data_plus = df_child_data_plus.drop_duplicates('contract-number', keep='last')
# df_child_data_plus = df_child_data_plus.reset_index(drop=True)
# df_root_data_plus = df_root_data_plus.drop_duplicates('name_file', keep='last')
# df_root_data_plus = df_root_data_plus.reset_index(drop=True)
# """Тут используем прывый join (merge) для того, чтобы файл выглядил идентично оригиналу"""
# df_result_plus = df_root_data_plus.merge(df_child_data_plus, left_on='name_file', right_on='name_file', how='right')
# df_result_plus = df_result_plus.drop('name_file', axis=1)


# with pd.ExcelWriter(filename_xml_delta) as writer:
    # df_result_plus.to_excel(writer, sheet_name='all_delta_plus_xml')
    # df_result_minus.to_excel(writer, sheet_name='all_delta_minus_xml')



### Третья часть проверки (создание файла с дельта плюс совмещенными с РИО)
# reestr_m_df_plus = pd.read_excel(path_to_directory_m, sheet_name='plus')
rio_df = pd.read_excel(path_to_RIO)
rio_change_df = rio_df.drop_duplicates('Код участника', keep='last')
# df_data_reestr_plus = reestr_m_df_plus.merge(rio_change_df[['номер договора ком представ',
#                                                   'Официал. наим твор падеж',
#                                                   'номер ДОП',
#                                                   'дата ДОП',
#                                                   'Официал. наименование',
#                                                   'адрес юр лица по ЕГРЮЛ',
#                                                   'почт адрес',
#                                                   'ИНН',
#                                                   'КПП',
#                                                   'Код участника',
#                                                   'дата договора ком представ'
#                                                             ]], left_on='Код ПРОДАВЦА(23)',
#                                              right_on='Код участника', how='left')
# df_data_reestr_plus = df_data_reestr_plus.merge(rio_change_df[['номер договора ком представ',
#                                                   'Официал. наим твор падеж',
#                                                   'номер ДОП',
#                                                   'дата ДОП',
#                                                   'Официал. наименование',
#                                                   'адрес юр лица по ЕГРЮЛ',
#                                                   'почт адрес',
#                                                   'ИНН',
#                                                   'КПП',
#                                                   'Код участника',
#                                                   'дата договора ком представ'
#                                                                ]], left_on='Код ПОКУПАТЕЛЯ(24)',
#                                                 right_on='Код участника', how='left')
# ### Добавляем данные из xml
# xml_df_plus = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_plus_xml')
# df_data_reestr_plus = df_data_reestr_plus.merge(xml_df_plus[[
#     'contract-number',
#     'trader-supplier-code',
#     'trader-supplier-name',
#     'contract-date',
#     'trader-consumer-code',
#     'trader-consumer-name'
# ]], left_on='Номер договора купли продажи ВР(03)', right_on='contract-number', how='left')
#
#
#
# df_data_reestr_minus = reestr_m_df_minus.merge(reestr_m_minus_1_df[[
#     'Номер договора купли продажи ВР(03)',
#     'Дата заключения договора ВР(04)',
#     'Полн наимен ПРОДАВ в тв пад(07)',
#     'Полн наимен ПОКУПАТ в тв пад(08)',
#     'Код ПРОДАВЦА(23)',
#     'Код ПОКУПАТЕЛЯ(24)',
#     'Срок начала пост мощн по дог ВР(25)',
#     'Год пост мощн по дог ВР(26)',
#     'Короткий номер договора ВР(27)'
# ]], left_on='Номер договора купли продажи ВР(03)', right_on='Номер договора купли продажи ВР(03)', how='left')
# ### Добавляем данные из xml
# xml_df_minus = pd.read_excel(path_to_xml_delta_data, sheet_name='all_delta_minus_xml')
# df_data_reestr_minus = df_data_reestr_minus.merge(xml_df_minus[[
#     'contract-number',
#     'trader-supplier-code',
#     # 'trader-supplier-name',
#     'contract-date',
#     'trader-consumer-code'
#     # 'trader-consumer-name'
# ]], left_on='Номер договора купли продажи ВР(03)', right_on='contract-number', how='left')



df_data_reestr_full = reestr_m_df_full.merge(reestr_m_minus_1_df[[
    'Номер договора купли продажи ВР(03)',
    'Дата заключения договора ВР(04)',
    'Срок начала пост мощн по дог ВР(25)',
    'Год пост мощн по дог ВР(26)',
    'Короткий номер договора ВР(27)'
]], left_on='Номер договора купли продажи ВР(03)', right_on='Номер договора купли продажи ВР(03)', how='left')

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
                                                            ]], left_on='Код ПРОДАВЦА(23)',
                                             right_on='Код участника', how='left')
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
                                                               ]], left_on='Код ПОКУПАТЕЛЯ(24)',
                                                right_on='Код участника', how='left')
# df_data_reestr_full = df_data_reestr_full.merge(xml_df_plus[[
#     'contract-number'
#     # 'trader-supplier-code',
#     # 'trader-supplier-name',
#     # 'dpg-supplier-code',
#     # 'delivery-start-date',
#     # 'trader-consumer-code',
#     # 'trader-consumer-name'
# ]], left_on='Номер договора купли продажи ВР(03)', right_on='contract-number', how='left')







with pd.ExcelWriter(filename_reestr_plus) as writer:
    df_data_reestr_full.to_excel(writer, sheet_name='delta_full_with_rio')
    # df_data_reestr_plus.to_excel(writer, sheet_name='delta_plus_with_rio')
    # df_data_reestr_minus.to_excel(writer, sheet_name='delta_minus_with_rio')







finish_time = time.time() - start_time
print(f'Скрипт работал {finish_time} секунд')