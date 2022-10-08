login = ["login", "pass"]
dns_for_riotan = 'serv'
## Изменить дату запроса
target_date = "TO_DATE('01.04.2022', 'DD/MM/YY')"

CONNECT_SCHEMA = f"""alter session set current_schema=crmdb"""

list_change_format = ['KOMMOD_START_DATE', 'KOMMOD_END_DATE', 'KOMMOD_CHANGE_START_DATE',
                      'KOMMOD_SUPPLY_START', 'KOMMOD_SUPPLY_END', 'KOMMOD_CHANGE_SUP_START',
                      'KOMMOD_CHANGE_SUP_END', 'KOMMOD_CHANGE_END_DATE', 'KOMMOD_ORDER_DATE']

RIO_REK = f"""
SELECT        
t.ofFicial_name "Официал. наименование",        
t.ofFicial_name_t "Официал. наим твор падеж",        
t.ur_address "юр адрес",        
t.ur_address_egrul   "адрес юр лица по ЕГРЮЛ",        
t.post_address "почт адрес",        
t.inn "ИНН",        
t.kpp_code "КПП",        
t.trader_code "Код участника",        
s.trader_code "Код станции",        
DECODE(s.station_type, 1, 'ГРЭС', 2, 'ГЭС',  3, 'АЭС',  4, 'ТЭС') "Тип станции",        
DECODE(s.station_category, 1, 'блок-станция', 8, 'ЗаГЭС') "Категория станции",        
g.trader_code "Код ГТП",        
g.is_unpriced_zone "Признак НЦЗ",        
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона",        

g.tariff_pow_up_ges_aes "Надб цены на мощн для ГЭС/АЭС",        
g.tariff_supply_kom_ges "Цена мощности ГЭС по КОМ",        
g.tariff2_supply_forced_mode "Цена ээ ВР (произв)",        
g.tariff3_supply_forced_mode "Цена мощн в ВР (произв)",        

g.tariff3_supply_old_power "Рег цена на мощн РД (old мощн)",        
g.tariff3_supply_new_power "Рег цена на мощн РД (new мощн)",        

g.region_code "Регион РФ",        
g.fst_region_coeff "Регион РФ по балансу ФСТ",        
g.is_blocked "заблокирована",        
g.is_gaes "принадлежность ГАЭС",        
g.is_dpm "участие в ДПМ",        
g.is_dpm_right_not_used "НЕ заключен ДПМ",        
g.is_new_ges_aes "принадлежит к новым АЭС/ГЭС",        
g.is_object_mgi "Принадлежит к МГИ",        
g.is_work_in_forced_mode "вырабатывает ЭЭ в ВР (ЭВР)",        
g.exploitation_mode "Характер эксплуатации",        
g.compelled_mode "Тип вынужденного режима",        
g.is_guarantee_supply_co "гарантирующий поставщик",        
NVL(g.fed_station, 0) "ГТП собственных нужд",        

g.is_fsk "ГТП ФСК",        
g.is_impex "ГТП импорта-экпорта",        
g.is_independ_consume_plan "Планир_потребл",        
g.zsp_links "ЗСП",        
(select max(reg_number) from CRMDB.contract where contract_type=1 and {target_date} between begin_date and end_date and t.real_trader_id=trader_id) "номер ДОП",        
(select trunc(max(reg_date),'dd') from CRMDB.contract where contract_type=1 and {target_date} between begin_date and end_date and t.real_trader_id=trader_id) "дата ДОП",        
(select max(reg_number) from CRMDB.contract where contract_type=23 and {target_date} between begin_date and end_date and t.real_trader_id=trader_id) "номер договора ком представ",        
(select trunc(max(reg_date),'dd') from CRMDB.contract where contract_type=23 and {target_date} between begin_date and end_date and t.real_trader_id=trader_id) "дата договора ком представ"        

FROM        
(SELECT * FROM CRMDB.trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,        
(SELECT * FROM CRMDB.trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,        
(SELECT * FROM CRMDB.trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,        
(SELECT * FROM CRMDB.trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s        
WHERE g.parent_object_id=t.real_trader_id AND g.fst_trader_id=f.real_trader_id AND g.dpg_station_id=s.real_trader_id(+)
"""

RIO_GTP = f"""
SELECT         
t.full_name "Полное наименование",         
t.trader_code "Код участника",         
s.trader_code "Код станции",         
DECODE(s.station_type, 1, 'ГРЭС', 2, 'ГЭС',  3, 'АЭС',  4, 'ТЭС') "Тип станции",         
DECODE(s.station_category, 1, 'блок-станция', 8, 'ЗаГЭС') "Категория станции",         
g.trader_code "Код ГТП",         
g.is_unpriced_zone "Признак НЦЗ",         
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона",         

g.tariff2_consume_deviation "Индикативная цена на ээ",         
g.tariff3_consume_gtp "Индикативная цена на мощность",         
g.indication_price "Индикативная цена субъекта РФ",         

g.tariff2_consume_other "Индик цена на ээ по ПРОЧИМ",         
g.tariff3_consume_other "Индик цена на мощ по ПРОЧИМ",         
g.indication_price_other "Индик цена СФ по ПРОЧИМ",         

g.tariff2_supply_deviation "Рег цена на ээ РД (стар мощ)",         
g.tariff2_ddpr_deviation "Тариф на параллельную работу",         
g.tariff5_supply_deviation "Рег цена на ээ_2 эт госрег",         
g.tariff6_supply_deviation "Рег цена на ээ_2 эт госрег нов",         
g.water_tax_for_ges "Ставка водного налога",         
g.tariff3_supply_new_ges_aes "Цена мощ new ГЭС/АЭС (произв)",         
g.tariff_pow_up_ges_aes "Надб цены на мощн для ГЭС/АЭС",         
g.tariff_supply_kom_ges "Цена мощности ГЭС по КОМ",         
g.tariff2_supply_forced_mode "Цена ээ ВР (произв)",         
g.tariff3_supply_forced_mode "Цена мощн в ВР (произв)",         
g.tariff_pow_without_dpm "Цена мощн при незакл ДПМ",         
g.tariff_pow_delay_dpm "Цена мощн при просрочке ДПМ",        
g.tariff_pow_delay_dpm_vr "Цена мощн при просрочке ДПМ ВР",         

g.tariff3_supply_old_power "Рег цена на мощн РД (old мощн)",         
g.tariff3_supply_new_power "Рег цена на мощн РД (new мощн)",         
g.tariff2_supply_new_power "Рег цена на ээ РД (new мощн)",         
g.tariff2_supply_mgi "Рег цена на ээ МГИ (руб/кВтч)",         

f.tariff1_supply "ФСТ Тариф одност (произв)",         
f.tariff1_consume "ФСТ Тариф одност (потреб)",         
f.tariff2_supply "ФСТ Рег цена на ээ в НЦЗ",         
f.tariff2_consume "ФСТ Индик цена на ээ в НЦЗ",         
f.tariff3_supply "ФСТ Рег цена на мощн в НЦЗ",         
f.tariff3_consume "ФСТ Индик цена на мощн в НЦЗ",         
f.tariff4_supply "ФСТ Тариф на уст мощн (произв)",         
f.tariff5_supply "ФСТ Тариф на период госрег",         

g.region_code "Регион РФ",         
g.fst_region_coeff "Регион РФ по балансу ФСТ",         
g.is_blocked "заблокирована",         
g.is_gaes "принадлежность ГАЭС",         
g.is_dpm "участие в ДПМ",         
g.is_dpm_right_not_used "НЕ заключен ДПМ",         
g.is_new_ges_aes "принадлежит к новым АЭС/ГЭС",         
g.is_object_mgi "Принадлежит к МГИ",         
g.is_work_in_forced_mode "вырабатывает ЭЭ в ВР (ЭВР)",         
g.exploitation_mode "Характер эксплуатации",         
g.compelled_mode "Тип вынужденного режима",         
g.is_guarantee_supply_co "гарантирующий поставщик",         
NVL(g.fed_station, 0) "ГТП собственных нужд",         

g.is_fsk "ГТП ФСК",         
g.is_impex "ГТП импорта-экпорта",         
g.is_independ_consume_plan "Планир_потребл",         
g.zsp_links "ЗСП",        
xattr.xattr_value "is_ges_sib_new",        
xattr1.xattr_value  "mobile_gen_object"        

FROM         
(SELECT * FROM crmdb.trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,         
(SELECT * FROM crmdb.trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,         
(SELECT * FROM crmdb.trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,         
(SELECT * FROM crmdb.trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s,        

(select * from crmdb.trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date        
and crmdb.xattr.XATTR_type = 'is_ges_sib_new'        
and crmdb.xattr.XATTR_VALUE = 1) xattr,        

(select * from crmdb.trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date        
and xattr.XATTR_type = 'mobile_gen_object'        
and xattr.XATTR_VALUE = 1) xattr1        

WHERE g.parent_object_id=t.real_trader_id AND g.fst_trader_id=f.real_trader_id AND g.dpg_station_id=s.real_trader_id(+)        
and g.real_trader_id = xattr.real_trader_id(+) and g.real_trader_id = xattr1.real_trader_id(+)
"""

RIO_GTP_PLUS = f"""
SELECT          
t.full_name "Полное наименование", 
t.short_name "Краткое наименование", 
t.trader_code "Код участника",          
s.trader_code "Код станции",          
DECODE(s.station_type, 1, 'ГРЭС', 2, 'ГЭС',  3, 'АЭС',  4, 'ТЭС') "Тип станции",          
DECODE(s.station_category, 1, 'блок-станция', 8, 'ЗаГЭС') "Категория станции",          
g.trader_code "Код ГТП",          
g.is_unpriced_zone "Признак НЦЗ",          
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона",                     

g.tariff2_consume_deviation "Индикативная цена на ээ",          
g.tariff3_consume_gtp "Индикативная цена на мощность",          
g.indication_price "Индикативная цена субъекта РФ",          

g.tariff2_consume_other "Индик цена на ээ по ПРОЧИМ",          
g.tariff3_consume_other "Индик цена на мощ по ПРОЧИМ",          
g.indication_price_other "Индик цена СФ по ПРОЧИМ",          

g.tariff2_supply_deviation "Рег цена на ээ РД (стар мощ)",          
g.tariff2_ddpr_deviation "Тариф на параллельную работу",          
g.tariff5_supply_deviation "Рег цена на ээ_2 эт госрег",          
g.tariff6_supply_deviation "Рег цена на ээ_2 эт госрег нов",          
g.water_tax_for_ges "Ставка водного налога",          
g.tariff3_supply_new_ges_aes "Цена мощ new ГЭС/АЭС (произв)",          
g.tariff_pow_up_ges_aes "Надб цены на мощн для ГЭС/АЭС",          
g.tariff_supply_kom_ges "Цена мощности ГЭС по КОМ",          
g.tariff2_supply_forced_mode "Цена ээ ВР (произв)",          
g.tariff3_supply_forced_mode "Цена мощн в ВР (произв)",          
g.tariff_pow_without_dpm "Цена мощн при незакл ДПМ",          
g.tariff_pow_delay_dpm "Цена мощн при просрочке ДПМ",         
g.tariff_pow_delay_dpm_vr "Цена мощн при просрочке ДПМ ВР",          

g.tariff3_supply_old_power "Рег цена на мощн РД (old мощн)",          
g.tariff3_supply_new_power "Рег цена на мощн РД (new мощн)",          
g.tariff2_supply_new_power "Рег цена на ээ РД (new мощн)",          
g.tariff2_supply_mgi "Рег цена на ээ МГИ (руб/кВтч)",                     

f.tariff1_supply "ФСТ Тариф одност (произв)",          
f.tariff1_consume "ФСТ Тариф одност (потреб)",          
f.tariff2_supply "ФСТ Рег цена на ээ в НЦЗ",          
f.tariff2_consume "ФСТ Индик цена на ээ в НЦЗ",          
f.tariff3_supply "ФСТ Рег цена на мощн в НЦЗ",          
f.tariff3_consume "ФСТ Индик цена на мощн в НЦЗ",          
f.tariff4_supply "ФСТ Тариф на уст мощн (произв)",          
f.tariff5_supply "ФСТ Тариф на период госрег",                     

g.region_code "Регион РФ",          
g.fst_region_coeff "Регион РФ по балансу ФСТ",          
g.is_blocked "заблокирована",          
g.is_gaes "принадлежность ГАЭС",          
g.is_dpm "участие в ДПМ",          
g.is_dpm_right_not_used "НЕ заключен ДПМ",          
g.is_new_ges_aes "принадлежит к новым АЭС/ГЭС",          
g.is_object_mgi "Принадлежит к МГИ",          
g.is_work_in_forced_mode "вырабатывает ЭЭ в ВР (ЭВР)",          
g.exploitation_mode "Характер эксплуатации",          
g.compelled_mode "Тип вынужденного режима",          
g.is_guarantee_supply_co "гарантирующий поставщик",          
NVL(g.fed_station, 0) "ГТП собственных нужд",                    

g.is_fsk "ГТП ФСК",          
g.is_impex "ГТП импорта-экпорта",          
g.is_independ_consume_plan "Планир_потребл",          
g.zsp_links "ЗСП",         
xattr.xattr_value "is_ges_sib_new",         
xattr1.xattr_value  "mobile_gen_object"              

FROM          
(SELECT * FROM crmdb.trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,          
(SELECT * FROM crmdb.trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,          
(SELECT * FROM crmdb.trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,          
(SELECT * FROM crmdb.trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s,         

(select * from crmdb.trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date         
and crmdb.xattr.XATTR_type = 'is_ges_sib_new'         
and crmdb.xattr.XATTR_VALUE = 1) xattr,         

(select * from crmdb.trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date         
and xattr.XATTR_type = 'mobile_gen_object'         
and xattr.XATTR_VALUE = 1) xattr1         

WHERE g.parent_object_id=t.real_trader_id AND g.fst_trader_id=f.real_trader_id AND g.dpg_station_id=s.real_trader_id(+)         
and g.real_trader_id = xattr.real_trader_id(+) and g.real_trader_id = xattr1.real_trader_id(+)
"""

RIO_GA = f"""
SELECT 
t.full_name "Полное наименование", 
t.trader_code "Код участника", 
s.trader_code "Код станции", 
s.full_name "Наименование станции", 
g.trader_code "Код ГТП", 
g.full_name "Наименование ГТП", 
g.is_blocked "ГТП заблокирована", 
rge.trader_code "Код РГЕ", 

ga.trader_code "Код ГА", 
ga.full_name "Наименование ГА", 
ga.fixed_power "уст. мощность ГА", 
ga.fixed_power_on_demand "уст. мощность по распоряжению", 
ga.tariff3_supply_forced_mode "цена мощности в ВР (произв)", 
ga.tariff_pow_delay_dpm "цена просрочки ДПМ ГА КОМ", 
ga.tariff_pow_delay_dpm_vr "цена просрочки ДПМ ГА ВР", 
ga.mvr_type "признак тепло/нетепло",
g.is_unpriced_zone "Признак НЦЗ", 
k.xattr_value "Признак ВР на ГА", 
k2.xattr_value "Подано заявление ВР",

g.is_unpriced_zone "Признак НЦЗ",  
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона" 

FROM  
(SELECT * FROM trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,  
(SELECT * FROM trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,  
(SELECT * FROM trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,  
(SELECT * FROM trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s,  
(SELECT * FROM trader WHERE trader_type=103 AND {target_date} BETWEEN begin_date AND end_date) rge,  
(SELECT * FROM trader WHERE trader_type=104 AND {target_date} BETWEEN begin_date AND end_date) ga,  
(select * from trader_xattr where xattr_type='is_vr' AND {target_date} BETWEEN begin_date AND end_date) k,  
(select * from trader_xattr where xattr_type='is_app_vr' AND {target_date} BETWEEN begin_date AND end_date) k2  

WHERE g.parent_object_id=t.real_trader_id AND g.fst_trader_id=f.real_trader_id AND g.dpg_station_id=s.real_trader_id AND rge.parent_object_id=g.real_trader_id AND ga.parent_object_id=rge.real_trader_id AND ga.real_trader_id=k.real_trader_id (+) AND ga.real_trader_id=k2.real_trader_id (+) 
ORDER BY "Ценовая зона", "Код участника", "Код станции", "Код ГТП", "Код РГЕ", "Код ГА"
"""

RIO_CZP = f"""
SELECT  
t.full_name "Полное наименование",  
t.trader_code "Код участника",  
s.trader_code "Код станции",  
DECODE(s.station_type, 1, 'ГРЭС', 2, 'ГЭС',  3, 'АЭС',  4, 'ТЭС') "Тип станции",  
DECODE(s.station_category, 1, 'блок-станция', 8, 'ЗаГЭС') "Категория станции",  
g.trader_code "Код ГТП",  
g.is_unpriced_zone "Признак НЦЗ",  
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона",  

g.tariff2_consume_deviation "Индикативная цена на ээ",  
g.tariff3_consume_gtp "Индикативная цена на мощность",  
g.indication_price "Индикативная цена субъекта РФ",  

g.tariff2_consume_other "Индик цена на ээ по ПРОЧИМ",  
g.tariff3_consume_other "Индик цена на мощ по ПРОЧИМ",  
g.indication_price_other "Индик цена СФ по ПРОЧИМ",  

g.tariff2_supply_deviation "Рег цена на ээ РД (стар мощ)",  
g.tariff2_ddpr_deviation "Тариф на параллельную работу",  
g.tariff5_supply_deviation "Рег цена на ээ_2 эт госрег",  
g.tariff6_supply_deviation "Рег цена на ээ_2 эт госрег нов",  
g.water_tax_for_ges "Ставка водного налога",  
g.tariff3_supply_new_ges_aes "Цена мощ new ГЭС/АЭС (произв)",  
g.tariff_pow_up_ges_aes "Надб цены на мощн для ГЭС/АЭС",  
g.tariff_supply_kom_ges "Цена мощности ГЭС по КОМ",  
g.tariff2_supply_forced_mode "Цена ээ ВР (произв)",  
g.tariff3_supply_forced_mode "Цена мощн в ВР (произв)",  
g.tariff_pow_without_dpm "Цена мощн при незакл ДПМ",  
g.tariff_pow_delay_dpm "Цена мощн при просрочке ДПМ", 
g.tariff_pow_delay_dpm_vr "Цена мощн при просрочке ДПМ ВР",  

g.tariff3_supply_old_power "Рег цена на мощн РД (old мощн)",  
g.tariff3_supply_new_power "Рег цена на мощн РД (new мощн)",  
g.tariff2_supply_new_power "Рег цена на ээ РД (new мощн)",  
g.tariff2_supply_mgi "Рег цена на ээ МГИ (руб/кВтч)",    

f.tariff1_supply "ФСТ Тариф одност (произв)",  
f.tariff1_consume "ФСТ Тариф одност (потреб)",  
f.tariff2_supply "ФСТ Рег цена на ээ в НЦЗ",  
f.tariff2_consume "ФСТ Индик цена на ээ в НЦЗ",  
f.tariff3_supply "ФСТ Рег цена на мощн в НЦЗ",  
f.tariff3_consume "ФСТ Индик цена на мощн в НЦЗ",  
f.tariff4_supply "ФСТ Тариф на уст мощн (произв)",  
f.tariff5_supply "ФСТ Тариф на период госрег",  

g.region_code "Регион РФ",  
g.fst_region_coeff "Регион РФ по балансу ФСТ",  
g.is_blocked "заблокирована",  
g.is_gaes "принадлежность ГАЭС",  
g.is_dpm "участие в ДПМ",  
g.is_dpm_right_not_used "НЕ заключен ДПМ",  
g.is_new_ges_aes "принадлежит к новым АЭС/ГЭС",  
g.is_object_mgi "Принадлежит к МГИ",  
g.is_work_in_forced_mode "вырабатывает ЭЭ в ВР (ЭВР)",  
g.exploitation_mode "Характер эксплуатации",  
g.compelled_mode "Тип вынужденного режима",  
g.is_guarantee_supply_co "гарантирующий поставщик", 
NVL(g.fed_station, 0) "ГТП собственных нужд",    

g.is_fsk "ГТП ФСК",  
g.is_impex "ГТП импорта-экпорта",  
g.is_independ_consume_plan "Планир_потребл",  
g.zsp_links "ЗСП", 
xattr.xattr_value "is_ges_sib_new", 
xattr1.xattr_value  "mobile_gen_object", 
x3.xattr_value  "GTPP CZP",  
x4.xattr_value "CZP qualified reestr" 

FROM  
(SELECT * FROM trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,  
(SELECT * FROM trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,  
(SELECT * FROM trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,  
(SELECT * FROM trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s, 
(select * from trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date 
and xattr.XATTR_type = 'is_ges_sib_new' 
and xattr.XATTR_VALUE = 1) xattr, 
(select * from trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date 
and xattr.XATTR_type = 'mobile_gen_object' 
and xattr.XATTR_VALUE = 1) xattr1, 
(select * from trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date 
and xattr.XATTR_type = 'is_dpg_dr_cons_decr') x3, 
(select * from trader_xattr xattr where {target_date} BETWEEN xattr.begin_date and xattr.end_date 
and xattr.XATTR_type = 'is_dpg_dr') x4 
WHERE g.parent_object_id=t.real_trader_id AND 
g.fst_trader_id=f.real_trader_id AND 
g.dpg_station_id=s.real_trader_id(+) AND 
g.real_trader_id = xattr.real_trader_id(+) AND 
g.real_trader_id = xattr1.real_trader_id(+) AND 
g.real_trader_id = x3.real_trader_id(+) AND 
g.real_trader_id = x4.real_trader_id(+)
"""

RIO_KOMMOD = f"""
select 
t.trader_code
,t.KOMMOD_DPG_CODE
,t.KOMMOD_NAME
,t.KOMMOD_PRICE_ZONE
,t.KOMMOD_REGION
,t.KOMMOD_FIXED_POWER
,t.KOMMOD_REDUCED_POWER
,t.KOMMOD_CHANGE_POWER_DATE
,t.KOMMOD_START_DATE
,t.KOMMOD_END_DATE
,t.KOMMOD_CHANGE_START_DATE
,t.KOMMOD_CHANGE_END_DATE
,t.KOMMOD_PERIOD
,t.KOMMOD_CHANGE_PERIOD
,t.KOMMOD_SUPPLY_START
,t.KOMMOD_SUPPLY_END
,t.KOMMOD_CHANGE_SUP_START
,t.KOMMOD_CHANGE_SUP_END
,t.KOMMOD_FUEL_TYPE
,t.KOMMOD_ORDER_NUMBER
,t.KOMMOD_ORDER_DATE
,t.OPK_YEAR
,t.KOMMOD_CAP_EXPENSES
,t.KOMMOD_OPER_EXPENSES
,t.KOMMOD_COMPENSE
,t.KOMMOD_KIUM
,t.KOMMOD_NOTICERSP_DATE
,atr.xattr_type

from 
(select * from crmdb.trader where trader_type=100 and {target_date} between begin_date and end_date) t
join (select * from trader_xattr where xattr_type='is_kommod_selected'     and xattr_value = 1
and {target_date} between begin_date and end_date) attr on t.real_trader_id= attr.real_trader_id 
left join (select * from trader_xattr where xattr_type='is_kommod_innovation'     and xattr_value = 1
and {target_date} between begin_date and end_date) atr on t.real_trader_id=atr.real_trader_id
"""

RIO_KOMMOD_REK = f"""
SELECT             
t.full_name "Полное наименование",             
t.trader_code "Код участника",             
s.trader_code "Код станции",             
s.full_name "Наименование станции",             
g.trader_code "Код ГТП",             
g.full_name "Наименование ГТП",             
ga.full_name "Наименование ГА",             
g.is_blocked "ГТП заблокирована",             
g.is_dpm "Признак ДПМ",             
g.is_new_ges_aes "Новые АЭС/ГЭС",             
g.tariff2_supply_deviation "Рег цена на ээ РД",            
g.exploitation_mode "Характер эксплуатации",             
gem.trader_code "Код ГЕМ",             
gem.full_name "Наименование ГЕМ",             
ga.trader_code "Код ГА",             
ga.full_name "Наименование ГА",             
ga.fixed_power "Мощность ГА из рег инф",             
ga.fixed_power_on_demand "Мощность ГА из запрета",             
ga.kommod_dpg_code "Ссылка на ГТПГ КОММод",            
nvl(g.compelled_mode,0) "Тип ВР на ГТП",             
ga.fuel_type_list "Основной вид топлива",            
ga.tariff2_supply_forced_mode "Цена ээ ВР (произв) на ГА",             
ga.tariff3_supply_forced_mode "Цена мощн ВР (произв) на ГА",             
g.is_unpriced_zone "Признак НЦЗ",             
DECODE(g.price_zone_code, 2, 'SIB', 'EUR') "Ценовая зона",             
DECODE(s.station_type, 1, 'ГРЭС', 2, 'ГЭС',  3, 'АЭС',  4, 'ТЭС') "Тип станции",            
g.tariff_pow_up_ges_aes "Надб цены на мощн для ГЭС/АЭС",            
g.tariff_supply_kom_ges "Цена мощности ГЭС по КОМ",            
g.tariff_pow_delay_dpm "Цена мощн при просрочке ДПМ",            
nvl(g.compelled_mode,0) "Тип вынужденного режима",            
g.is_fsk "ГТП ФСК",            
g.is_impex "ГТП импорта-экпорта",            
r.region_name "Регион РФ (назв)",            
g.zsp_links "ЗСП" ,          
t.short_name "Короткое Имя",        
g.kommod_region,       
g.kommod_name,
g.real_trader_id "Первая часть id"
FROM             
(SELECT * FROM trader WHERE trader_type=2 AND {target_date} BETWEEN begin_date AND end_date) t,             
(SELECT * FROM trader WHERE trader_type=3 AND {target_date} BETWEEN begin_date AND end_date) f,             
(SELECT * FROM trader WHERE trader_type=100 AND {target_date} BETWEEN begin_date AND end_date) g,             
(SELECT * FROM trader WHERE trader_type=102 AND {target_date} BETWEEN begin_date AND end_date) s,             
(SELECT * FROM trader WHERE trader_type=104 AND {target_date} BETWEEN begin_date AND end_date) ga,             
(SELECT * FROM trader WHERE trader_type=105 AND {target_date} BETWEEN begin_date AND end_date) gem,            
region r            
WHERE g.parent_object_id=t.real_trader_id AND g.fst_trader_id=f.real_trader_id AND g.dpg_station_id=s.real_trader_id AND ga.gem_parent_id=gem.real_trader_id AND g.region_code=r.region_code AND gem.parent_object_id=g.real_trader_id (+)            
ORDER BY "Ценовая зона", "Код участника", "Код станции", "Код ГТП", "Код ГЕМ", "Код ГА"
"""