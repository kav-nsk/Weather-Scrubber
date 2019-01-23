import requests
import re
import time
import datetime
import csv

def receiver_html(idNumber, firstDay, lastDay, month, year):
    '''Получение html страницы с раздела сайта "Погода и климат" --> "Архив погоды". id следует взять из адресной строки браузера после перехода
    к нужному населенному пункту.
    '''
    params = {'id':idNumber, 'bday':str(firstDay), 'fday':str(lastDay), 'amonth':str(month), 'ayear':str(year), 'bot':'2'}
    r = requests.get('http://www.pogodaiklimat.ru/weather.php', params)
    r.encoding = 'utf-8'
    return(r.text)

def parser_html(t):
    # Выпиливаем нужное из таблицы html файла. То, что нужно, по порядку перечислено в listOfParams.
    tableInString = t[t.find('</tr'):t.find('</table')]
    tableInString = tableInString.strip('</tr>').strip('\n').split('</tr>')
    del tableInString[-1]
    tableInString = [i.split('<td') for i in tableInString] # ...еще нарезка строк.

        # Выбираем строки с нужной информацией, удаляем мешающие извлечению данных тэги.
    tableInString = [[i[1].replace('<b>', ''), i[2].replace('<b>', ''), i[3], i[4],
                    i[6].replace('<i>', ''),
                    i[8].replace('<nobr>', ''), i[10], i[15], i[16].replace('<nobr>', ''),
                    i[17].replace('<nobr>', ''), i[18], i[20]] for i in tableInString]

        # Выборка данных и заполнение итогового списка.
    listOfData = []
    n = 0
    for i in tableInString:
        listOfData.append([])
        for j in i:
            data = j[j.find('>') + 1:j.find('<')]
            listOfData[n].append(data)
            if i.index(j) == 10:       # Получение данных по виду снежного покрова из последней строки.
                dataSnow = j[j.find('"') + 1:j.find('" ')]
                listOfData[n].append(dataSnow)
        n += 1

    # Взятие поправки к UTC из html страницы.
    stringUTC = t[t.find('<p>Внимание!'):t.find('ч.</p>')]
    stringUTC = stringUTC.rstrip()
    regexes = [re.compile(str(i)) for i in range(13)]
    
    for regex in regexes:
        if regex.search(stringUTC):
            deltaTime = int(regex.pattern)
    
    return (listOfData, deltaTime)



# ------------------- MAIN SECTION -------------------
listOfParam = ['Час по местному времени', 'День.Месяц.Год', 'Направление ветра', 'V ветра, м/с', 'Явления', 't воздуха, `C', 'Влажность, %',
                'Давление воздуха на высоте места измерения над уровнем моря, мм рт. ст.', 'min t воздуха, `C', 'max t воздуха, `C',
                'Количество осадков за последние 12ч, мм', 'Высота снежного покрова, см', 'Состояние снега, величина покрытия местности в баллах']

print('''\n
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        Утилита получения архивных данных о погоде с сайта "Погода и климат" /www.pogodaiklimat.ru/
            разработчик Кузовлев Александр /kav.develop@yandex.ru/
            с. Ленинское, Новосибирского р-на
            вер. 1.0, январь 2019 г.
    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\
    ''')

print('''
Для запроса информации вам нужно узнать id населенного пунка или метеостанции.
Для этого следует перейти к разделу сайта: "Погода и климат" --> "Архив погоды" --> Объект (населенный пункт, метеостанция).
id следует взять из адресной строки браузера после перехода к нужному объекту.
По умолчанию будет использован id=29635, для метеостанции "Обская ГМО" (Новосибрская обл.)
''')

while True:
    idNumber = input('Введите id объекта: ')
    if idNumber == '':
        idNumber = '29635'
        break
    if idNumber.isdigit():
        break
    print('Внимание! Допустимо только целое число.')

print('Введите интересующий вас период:')
today = datetime.date.today()

while True:
    year = input('Год (не ранее 2011 года): ')
    month = input('Месяц (цифрой): ')
    firstDay = input('Начальное число периода: ')
    lastDay = input('Конечное число периода: ')
    if year.isdigit() and month.isdigit() and firstDay.isdigit() and lastDay.isdigit():
        year = int(year)
        month = int(month)
        firstDay = int(firstDay)
        lastDay = int(lastDay)
        if year < 2011:
            print('За этот год данных нет.')
            continue
        elif month < 1 or firstDay < 1 or lastDay < 1 or month > 12 or firstDay > 31 or lastDay > 31:
            print('Такой календарной даты нет.')
            continue
        elif firstDay > lastDay:
            print('Начальная дата периода должна быть меньше конечной.')
            continue
        elif datetime.date(year, month, firstDay) > today:
            print('За этот период данных еще нет.')
            continue
        break

t = receiver_html(idNumber, firstDay, lastDay, month, year)
dataFromParser = parser_html(t)
listOfData, deltaTime = dataFromParser[0], dataFromParser[1]

# Поправка на местное время c коррекцией даты. Первод давления из ГПа в мм рт. ст.
for i in listOfData:
    data = i[1].split('.')
    timeEpoch = time.mktime((int(year), int(data[1]), int(data[0]), int(i[0]) + deltaTime, 0, 0, 0, 0, 0))
    parsedTime = time.strptime(time.ctime(timeEpoch))
    i[0] = str(parsedTime.tm_hour)
    i[1] = str(parsedTime.tm_mday) + '.' + str(parsedTime.tm_mon) + '.' + str(parsedTime.tm_year)
    i[6] = '%.1f' % (float(i[6]) * 0.75)   # перевод единиц давления

# Запись в csv файл.
with open('arhive.csv', 'w') as arhFile:
    writer = csv.DictWriter(arhFile, fieldnames=listOfParam)
    writer.writeheader()
    for i in listOfData:
        writer.writerow(dict(zip(listOfParam, i)))

print('OK!')
print('Откройте файл arhive.csv')