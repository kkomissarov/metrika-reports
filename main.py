from settings import START_DATE, FINISH_DATE, PROJECT
from global_settings import API_KEY, BASE_URL, counters_id, segments
import functions
import requests
import csv




get_distribution = functions.sources_summary()
organic_trafic = get_distribution['organic']
direct_trafic = get_distribution['direct']
ad_trafic = get_distribution['ad']
internal_trafic = get_distribution['internal']
social_trafic = get_distribution['social']
referral_trafic = get_distribution['referral']



#######################ДАННЫЕ ЗА ПРОШЛЫЙ ГОД###################################
last_year_start_date = START_DATE.replace(START_DATE[0:4],str(int(START_DATE[0:4])-1))
last_year_finish_date = FINISH_DATE.replace(FINISH_DATE[0:4],str(int(FINISH_DATE[0:4])-1))


#######################ЗАПИСЫВАЕМ ОТЧЕТ В CSV###################################
report_data = []
print('Готовим отчет по проекту', PROJECT)
print('...Выгрузка общих показателей')
report_data.append(('ОБЩИЕ БАЗОВЫЕ ПОКАЗАТЕЛИ', ))
report_data.append(('Общее количество визитов:', str(functions.total_visits())))
report_data.append(('Общее количество просмотров:', str(functions.total_views())))
report_data.append(('Общее количество посетителей:', str(functions.total_users())))
report_data.append(('Средняя глубина просмотра:', str(functions.depth_of_view()).replace('.', ',')))
report_data.append(('Среднее время на сайте:', str(functions.time_in_visit())))
report_data.append(('Процент отказов:', str(functions.bounce_rate()).replace('.', ',')))
report_data.append(('\n', ))

print('...Выгрузка общих показателей для поискового трафика')
report_data.append(('БАЗОВЫЕ ПОКАЗАТЕЛИ ЧИСТО ДЛЯ ПОИСКОВОГО ТРАФИКА', ))
report_data.append(('Визиты из поиска:', str(functions.from_search(functions.total_visits))))
report_data.append(('Просмотры из поиска:', str(functions.from_search(functions.total_views))))
report_data.append(('Посетители из поиска:', str(functions.from_search(functions.total_users))))
report_data.append(('Глубина просмотров из поиска:', str(functions.from_search(functions.depth_of_view)).replace('.', ',')))
report_data.append(('Среднее время на сайте из поиска:', str(functions.from_search(functions.time_in_visit))))
report_data.append(('Процент отказов из поиска:', str(functions.from_search(functions.bounce_rate)).replace('.', ',')))
report_data.append(('\n', ))

print('...Выгрузка источников трафика')
report_data.append(('ИСТОЧНИКИ ТРАФИКА', ))
report_data.append(('Переходы из поисковых систем:', str(organic_trafic)))
report_data.append(('Переходы по рекламе:', str(ad_trafic)))
report_data.append(('Прямые заходы:', str(direct_trafic)))
report_data.append(('Внутренние переходы:', str(internal_trafic)))
report_data.append(('Переходы по ссылкам на сайтах:', str(referral_trafic)))
report_data.append(('Переходы из социальных сетей:', str(social_trafic, )))
report_data.append(('\n',))

print('...Выгрузка распределения по поисковым системам')
report_data.append(('РАСПРЕДЕЛЕНИЕ ПО ПОИСКОВЫМ СИСТЕМАМ', ))

ps = functions.sources_searchengine()
for key in ps:
    report_data.append((key+':', str(ps[key])))
report_data.append(('\n',))


print('...Выгрузка поискового трафика по дням')
report_data.append(('ПОИСКОВЫЙ ТРАФИК ПО ДНЯМ',))
ds = functions.days_search_trafic()
for key in ds:
    report_data.append((str(key), str(ds[key])))
report_data.append(('\n', ))


print('...Выгрузка географии посетителей')
report_data.append(('ГЕОГРАФИЯ ПОСЕТИТЕЛЕЙ (10 главных регионов)',))
cities = functions.geo()
i = 0
for g in cities:
    if i<10:
        report_data.append((g, cities[g]))
        i += 1
report_data.append(('\n', ))

print('...Выгрузка типов устройств')
report_data.append(('ТИПЫ УСТРОЙСТВ, ПО КОТОРЫМ ПЕРЕХОДИЛИ ИЗ ПОИСКА',))
dev = functions.devices()
report_data.append(('ПК:', str(dev[0])))
report_data.append(('Смартфоны:', str(dev[2])))
report_data.append(('Планшеты:', str(dev[1])))
report_data.append(('\n',))


if segments[PROJECT]:
    print('...Выгрузка сегментов, добавленных вручную')
    report_data.append(('СЕГМЕНТЫ, ДОБАВЛЕННЫЕ ВРУЧНУЮ',))
    sgmnts = functions.segments_info()
    for s in sgmnts:
        report_data.append((s, str(sgmnts[s])))
    report_data.append(('\n',))

print('...Формирование отчета')


with open('Отчет '+PROJECT+' с '+START_DATE+' по '+FINISH_DATE+'.csv', "w", newline='', encoding='utf-8') as report:
    writer = csv.writer(report, delimiter=';')
    for line in report_data:
        writer.writerow(line)
print('\nГотово!')