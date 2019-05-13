from settings import START_DATE, FINISH_DATE, PROJECT
from global_settings import API_KEY, BASE_URL, counters_id, segments
import requests

#######################ФУНКЦИИ ДЛЯ ПОЛУЧЕНИЯ БАЗОВЫХ МЕТРИК###################################
def basic_request (**kwargs):
    r_params = {'ids': counters_id.get(PROJECT),
                'date1': START_DATE,
                'date2': FINISH_DATE,
    }

    headers = {
        'Authorization': 'OAuth '+API_KEY
    }

    r_params.update(kwargs)
    r = requests.get(BASE_URL, params = r_params, headers=headers).json()
    return r


#общее количество визитов
def total_visits(**kwargs):
    value = basic_request(metrics = 'ym:s:visits', **kwargs)
    return int(value['totals'][0])

#общее количество просмотров
def total_views(**kwargs):
    value = basic_request(metrics = 'ym:s:pageviews', **kwargs)
    return int(value['totals'][0])

#общее количество посетителей
def total_users(**kwargs):
    value = basic_request(metrics = 'ym:s:users', **kwargs)
    return int(value['totals'][0])

#средня глубина просмотра
def depth_of_view(**kwargs):
    value = basic_request(metrics = 'ym:s:pageDepth', **kwargs)
    return round(value['totals'][0], 2)

#Среднее время на сайте
def time_in_visit(**kwargs):
    value = basic_request(metrics = 'ym:s:avgVisitDurationSeconds', **kwargs)
    time = str(int(value['totals'][0] // 60)) + ' мин и ' + str(int(round(value['totals'][0] % 60, 0))) + ' сек'
    return time

#Процент отказов
def bounce_rate(**kwargs):
    value = basic_request(metrics = 'ym:s:bounceRate', **kwargs)
    return round(value['totals'][0], 2)




#######################НАДСТРОЙКИ ДЛЯ СЕГМЕНТАЦИИ###################################

#Базовая метрика, но из поиска
def from_search(basic_metric_function):
    val = basic_metric_function(dimensions='ym:s:searchEngine')
    return val


#######################ШАБЛОНЫ ОТЧЕТА###################################

# Источники трафика: поисковые системы (возвращает детальную инфу)
def sources_searchengine():
    value = basic_request(preset = 'search_engines', metrics = 'ym:s:visits', dimensions='ym:s:searchEngine')
    detail_search_trafic = {}
    for elem in value['data']:
        detail_search_trafic.update({str(elem['dimensions'][0]['name']): int(elem['metrics'][0])})

    return detail_search_trafic


# Источники: сводка
def sources_summary():
    value = basic_request(preset = 'sources_summary', metrics = 'ym:s:visits', limit='10000')
    organic = 0
    direct = 0
    ad = 0
    internal = 0
    social = 0
    referral = 0

    print(value)

    for elem in value['data']:
        if elem['dimensions'][0].get('id') == 'organic':
            organic += int(elem['metrics'][0])
        if elem['dimensions'][0].get('id') == 'direct':
            direct += int(elem['metrics'][0])
        if elem['dimensions'][0].get('id') == 'ad':
            ad += int(elem['metrics'][0])
        if elem['dimensions'][0].get('id') == 'internal':
            internal += int(elem['metrics'][0])
        if elem['dimensions'][0].get('id') == 'social':
            social += int(elem['metrics'][0])
        if elem['dimensions'][0].get('id') == 'referral':
            referral += int(elem['metrics'][0])

    result = {
        'organic': organic, #Органический трафик
        'direct': direct, #Прямые заходы
        'ad': ad, #Рекламные системы
        'internal': internal, #Внутренние переходы
        'social': social, #Социальные сети
        'referral': referral #Переходы с других сайтов
    }

    return result

#Поисковый трафик по дням
def days_search_trafic():
    value = basic_request(preset = 'traffic', metrics = 'ym:s:visits', group='Day', limit='1000', filters="ym:s:trafficSource=='organic'")
    every_day_search_trafic = {}
    for i in value['data']:
        every_day_search_trafic.update({i['dimensions'][0]['from']: int(i['metrics'][0])})

    #Отсортируем дни по порядку
    days = []
    for key in every_day_search_trafic:
        days.append(key)
    days.sort()

    sort_dict = {}
    for day in days:
        sort_dict.update({day: every_day_search_trafic[day]})


    return sort_dict



# География посетителей. Возвращает дикт вида город: кол-во визитов
def geo():
    value = basic_request(preset = 'geo_country', metrics = 'ym:s:visits', limit='10000', filters="ym:s:trafficSource=='organic'")
    city_list = {}
    for g in value['data']:
        if g['dimensions'][2]['name'] != None:
            city_list.update({str(g['dimensions'][2]['name'])+', '+ str(g['dimensions'][0]['name']): int(g['metrics'][0])})
    return city_list


# Типы устройств
def devices():
    value = basic_request(preset = 'tech_devices', metrics = 'ym:s:visits', limit='10000', filters="ym:s:trafficSource=='organic'")
    desktop = 0
    tablet = 0
    mobile = 0
    for d in value['data']:
        if d['dimensions'][0].get('id') == 'desktop':
            desktop += int(d['metrics'][0])
        if d['dimensions'][0].get('id') == 'tablet':
            tablet += int(d['metrics'][0])
        if d['dimensions'][0].get('id') == 'mobile':
            mobile += int(d['metrics'][0])
    return [desktop, tablet, mobile]



#Считаем все сегменты, заданные вручную в настройках проекта
def segments_info():
    total = {}
    for segment in segments[PROJECT]:
        r = basic_request(**segments[PROJECT][segment])
        try:
            total.update({segment: int(r['totals'][0])})
        except:
            total.update({'залупа': 'в этом месте вы получили волосатый хуй'})
    return total