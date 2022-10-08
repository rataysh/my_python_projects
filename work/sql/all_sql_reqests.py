import cx_Oracle, xlsxwriter, openpyxl
import pandas as pd
from reqests import RIO_REK, dns_for_riotan, login, \
    CONNECT_SCHEMA, RIO_GTP, RIO_GTP_PLUS, RIO_GA, RIO_CZP, RIO_KOMMOD, RIO_KOMMOD_REK, list_change_format


class From_sql_oracle:
    def __init__(self, login_data, dns, sql_request_1, sql_request_2):
        self.login_data = login_data
        self.dns = dns
        self.sql_request_1 = sql_request_1
        self.sql_request_2 = sql_request_2

    def parse_from_sql(self):
        user = self.login_data[0]
        password = self.login_data[1]
        dns = self.dns
        sql_request_1 = self.sql_request_1
        sql_request_2 = self.sql_request_2
        try:
            connection = cx_Oracle.connect(
                user=user,
                password=password,
                dsn=dns,
                encoding='UTF-8')
            print("Successfully connected to Oracle Database")
            cursor_1 = connection.cursor()
            cursor_1.execute(sql_request_1)
            cursor_2 = connection.cursor()
            cursor_2.execute(sql_request_2)
            mydata = [x for x in cursor_2.fetchall()]
            columns = [column[0] for column in cursor_2.description]
            df = pd.DataFrame(data=mydata, columns=columns)
            cursor_1.close()
            cursor_2.close()
            return df
        except cx_Oracle.DatabaseError as err:
            print(f"!!! Проблемы с запросом. Вот ошибка - {err}\n")

## Подключение к схеме (для РИО_ГА и коммод)
connect_to_schema = CONNECT_SCHEMA


sql_request_for_rio_rek = RIO_REK
df_rio_rek = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_rek).parse_from_sql()
df_rio_rek['дата ДОП'] = pd.to_datetime(df_rio_rek['дата ДОП']).dt.strftime('%d-%m-%y')
df_rio_rek['дата договора ком представ'] = pd.to_datetime(df_rio_rek['дата договора ком представ']).dt.strftime('%d-%m-%y')

sql_request_for_rio_gtp = RIO_GTP
df_rio_gtp = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_gtp).parse_from_sql()

sql_request_for_rio_gtp_plus = RIO_GTP_PLUS
df_rio_gtp_plus = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_gtp_plus).parse_from_sql()

sql_request_for_rio_ga = RIO_GA
df_rio_ga = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_ga).parse_from_sql()

sql_request_for_rio_czp = RIO_CZP
df_rio_czp = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_czp).parse_from_sql()

sql_request_for_rio_kommod = RIO_KOMMOD
df_rio_kommod = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_kommod).parse_from_sql()
for i in list_change_format:
    df_rio_kommod[i] = pd.to_datetime(df_rio_kommod[i]).dt.strftime('%d-%m-%y')

sql_request_for_rio_kommod_rek = RIO_KOMMOD_REK
df_rio_kommod_rek = From_sql_oracle(login, dns_for_riotan, connect_to_schema, sql_request_for_rio_kommod_rek).parse_from_sql()


with pd.ExcelWriter('all_RIO_04.xlsx') as writer:
    df_rio_rek.to_excel(writer, sheet_name='RIO_REK')
    df_rio_gtp.to_excel(writer, sheet_name='RIO_GTP')
    df_rio_gtp_plus.to_excel(writer, sheet_name='RIO_GTP_PLUS')
    df_rio_ga.to_excel(writer, sheet_name='RIO_GA')
    df_rio_kommod.to_excel(writer, sheet_name='RIO_KOMMOD')
    df_rio_kommod_rek.to_excel(writer, sheet_name='RIO_KOMMOD_REK')
    df_rio_czp.to_excel(writer, sheet_name='RIO_CZP')
