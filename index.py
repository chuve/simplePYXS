#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
import urllib
import xml.dom.minidom


todayDate = datetime.date.today().isoformat() # Определение текущей даты

proxies = {'http': 'http://188.127.253.195:8080'} # Настройки прокси

siteLink = 'www.promtek-b.ru' # Домен сайта для поиска в SERP Yandex

searchRequests = open('requests.txt', 'r') # Файл с запросами

searchRequestsList = [] # Создание списка и запись запросов из файла 
for line in searchRequests:
	searchRequestsList.append(line)

resultFile = open('result_'+siteLink+'_'+todayDate+'.txt','w+') # Создание файла для записи результатов

searchUrl = 'http://xmlsearch.yandex.ru/xmlsearch?user=echuvelev&key=03.108075721:c7369ceffbf6b8d874ff9de0dfa28c14&query=%s&lr=%s&page=%s' # URL для отправки запросов на сервер xml.yandex.ru

def urlTakerFinder(req,page,region): # Функция отправки запроса и парсинга ответа
	xmlResponse = urllib.urlopen(searchUrl % (req,region,page), proxies=proxies)
	#resultFile.write(xmlResponse.read())
	domScheme = xml.dom.minidom.parse(xmlResponse)
	urls = domScheme.getElementsByTagName("domain") 
	if len(urls) == 0:
		print 'Проблемы с получением выдачи от сервера Yandex'
		sys.exit()
	else:
		return urls # возвращает список всех значений <domain> на странице

def placeFinder(urls): # Функция поиска домена
	for position, url in enumerate(urls):
		#print url.childNodes[0].nodeValue
		if url.childNodes[0].nodeValue == siteLink:
			return position # возвращает позицию на странице или None
			
def handler(req, region): # Функция поиска домена в выдаче (глубина ограничивается числом страниц)
	for page in xrange(0,10,1):
		domainList = urlTakerFinder(req, page, region)
		position = placeFinder(domainList)
		if position != None:
			return (position + 1 + page * 10)
			break
		else: 
			position = '>100'
	return position # возвращает позицию в выдаче

for keyword in searchRequestsList: #цикл для поиска позиций для всех запросов которые есть в файле searchRequests
	resultFile.write('{0} - {1}.\n'.format(keyword.strip(), handler(keyword,213)))
resultFile.close()