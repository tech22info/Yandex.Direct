#!/usr/bin/python3
# encoding=utf-8
import json, requests, psycopg2
import sys, datetime
##########################################
# Нужно написать на Python скрипт который собирает с Yandex.Direct статистику показов и кладет в базу. 
# База - постгрес. Нужна статистика по дням: по кампаниям, объявлениям и отдельным ключевым словам.
#
# Документация по АПИ: https://tech.yandex.ru/direct/
# Сейчас в проекте используются psycopg для работы с базой, и requests для работы с вебом. Желательно использовать их, чтобы избежать "зоопарка" в проекте.
##########################################

# Подготовоительные операции (изменить на реальные значения)  !!!!!!!!!!!
#address for sending JSON requests
url = 'https://api-sandbox.direct.yandex.ru/live/v4/json/'
#data for OAuth authentication
token = '5381078dc2b24f4280059a7735f9d328'

# Получение списка "Клиентов"
def GetClientsList():
	global token
	ClientsListData={}
	data = {
		"method": "GetClientsList",
		'token': token,
		'locale': 'ru',
		"Filter": {
		"StatusArch": "Yes"
		}
		}
	jdata = json.dumps(data, ensure_ascii=False).encode('utf8')
	response = requests.post(url,jdata)
	ClientsListData=response.json()['data']
	return ClientsListData

# Получение списка "Рекламных компаний"
def GetCampaignsList(login):
	global token
	CampaignsListData={}
	data = {
		'method': 'GetCampaignsList',
		'token': token,
		'locale': 'ru',
		'param': [login],
		}
	jdata = json.dumps(data, ensure_ascii=False).encode('utf8')
	response = requests.post(url,jdata)
	CampaignsListData=response.json()['data']
	return CampaignsListData

# Получение списка "Объявлений"
def GetBannersList(CampaignID):
	global token
	CampaignsListData={}
	data = {
		'method': 'GetBanners',
		'token': token,
		'locale': 'ru',
		'param': {"CampaignIDS":[CampaignID]},
		'GetPhrases':'WithPrices'
		}
	jdata = json.dumps(data, ensure_ascii=False).encode('utf8')
	response = requests.post(url,jdata)
	CampaignsListData=response.json()['data']
	return CampaignsListData

# Выборка статистики
def GetBannersStat(CampaignID,StartDate,EndDate):
	global token
	BannersStatData={}
	data = {
		'method': 'GetBannersStat',
		'token': token,
		'locale': 'ru',
		'param': {"CampaignID":CampaignID,
		"StartDate":StartDate,
		"EndDate":EndDate},
		}
	jdata = json.dumps(data, ensure_ascii=False).encode('utf8')
	response = requests.post(url,jdata)
	BannersStatData=response.json()['data']
	return BannersStatData


# Определяемся с датой "Вчера"
# В дальнейшем при обновлении статистики переопределим
DataNow=datetime.datetime.now()-datetime.timedelta(days=1)
Tomorrow=DataNow.strftime('%Y-%m-%d')

# Измените данные на подключение к реальной базе данных
cn_string = "host='192.168.234.7' dbname='yandexdirect' user='yadirect' password='yadirect'"
cn=psycopg2.connect(cn_string)
cr=cn.cursor()

#************************************************************************************
#* Обновляем информацию о всех клиентах/Рекламных компаниях/Банерах/Ключевых словах *
#************************************************************************************
# Если обновление этих сведений не требуется устанавливаем параметр UpdateBanners в False

UpdateBanners=True

if UpdateBanners:
	# Обновляем список клиентов
	for Client in GetClientsList():
		# Запрашиваем список клиентов и добавляем их в БД (уникальное поле Login)
		try:
			# Попытка добавления клиента
			cr.execute('INSERT INTO clients(login) VALUES (%s);',(Client['Login'],))
			cn.commit()
		except:
			# Такой клиент уже есть
			cn.rollback()
		print ('Обновляем сведения о клиенте: '+Client['Login'])
		# Обновляем данные по клиенту (True/False отрабатывает на Yes/No)
		cr.execute('UPDATE clients SET sendaccnews=%s, sharedaccountenabled=%s, fio=%s, \
		datecreate=%s, displaystorerating=%s, sendwarn=%s, email=%s, \
		vatrate=%s, phone=%s, role=%s, overdraftsumavailable=%s, \
		statusarch=%s, clientcurrencies=%s, sendnews=%s, nonresident=%s, \
		discount=%s\
		WHERE login=\''+Client['Login']+'\';',(Client['SendAccNews'],Client['SharedAccountEnabled'],Client['FIO'],Client['DateCreate'],\
		Client['DisplayStoreRating'],Client['SendWarn'],Client['Email'],Client['VATRate'],Client['Phone'],Client['Role'],Client['OverdraftSumAvailable'],\
		Client['StatusArch'],Client['ClientCurrencies'],Client['SendNews'],Client['NonResident'],Client['Discount']))
		cn.commit()
	# Запрос списка рекламных компаний для клиентов
	cr.execute('SELECT login FROM clients;')
	Clients=cr.fetchall()
	for Client in Clients:
		login=Client[0]
		print ('Запрашиваем список рекламных компаний для клиента: '+login)
		for Campaign in GetCampaignsList(login):
			# Добавляем компанию клиенту. Проверка уникальности проводится по связке полей ID-рекламной компании/Клиент
			try:
				cr.execute('INSERT INTO campaigns(login,campaignid) VALUES (%s,%s);',(Campaign['Login'],Campaign['CampaignID'],))
				cn.commit()
			except:
				cn.rollback()
			print ('Обновляем информацию о рекламной компании клиента '+Campaign['Login']+' ID-рекламной компании '+str(Campaign['CampaignID']))
			# Обновление сведений о рекламной комапнии
			cr.execute('UPDATE campaigns SET managername=%s, strategyname=%s, startdate=%s, \
			daybudgetenabled=%s, contextstrategyname=%s, sum=%s, agencyname=%s, \
			sumavailablefortransfer=%s, name=%s, clicks=%s, statusShow=%s, \
			campaigncurrency=%s, statusmoderate=%s, statusactivating=%s, \
			shows=%s, rest=%s, isactive=%s, statusarchive=%s, \
			status=%s \
			WHERE login=\''+Campaign['Login']+'\' AND campaignid='+str(Campaign['CampaignID'])+';', (Campaign['ManagerName'], Campaign['StrategyName']\
			, Campaign['StartDate'], Campaign['DayBudgetEnabled'], Campaign['ContextStrategyName'], Campaign['Sum'], Campaign['AgencyName'], \
			Campaign['SumAvailableForTransfer'], Campaign['Name'], Campaign['Clicks'], Campaign['StatusShow'], Campaign['CampaignCurrency']\
			, Campaign['StatusModerate'], Campaign['StatusActivating'], Campaign['Shows'], Campaign['Rest'], Campaign['IsActive'], Campaign['StatusArchive'], \
			Campaign['Status']))
			cn.commit()
	# Запрос списка объявлений
	cr.execute('SELECT campaignid FROM campaigns;')
	Campaigns=cr.fetchall()
	for Campaign in Campaigns:
		CampaignID=Campaign[0]
		print ('Получаем список объявлений (и ключевых слов) для рекламной компании: '+str(CampaignID))
		Banners=GetBannersList(str(CampaignID))
		for Banner in Banners:
			# Добавляем банер к рекламной компании (связка ID-банера и ID-компании).
			# По идентификатору компании можно найти клиента
			try:
				cr.execute('INSERT INTO banners(bannerid, campaignid) VALUES (%s,%s);',(str(Banner['BannerID']),str(Banner['CampaignID'])))
				cn.commit()
			except:
				cn.rollback()
			print ('Обновляем информацию о объявлении '+str(Banner['BannerID'])+' в рекламной компании '+str(Banner['CampaignID']))
			# Обратите внимание, что данных о дате создания банера не сообщается и датой создания 
			# будет считаться дата первого добавления в базу данных
			cr.execute('UPDATE banners \
			SET adgroupID=%s, statusarchive=%s, statusactivating=%s, \
			title=%s, text=%s, isactive=%s\
			WHERE bannerid='+str(Banner['BannerID'])+' AND campaignid='+str(Banner['CampaignID'])+';',\
			(Banner['AdGroupID'], Banner['StatusArchive'], Banner['StatusActivating'], Banner['Title'], Banner['Text'], Banner['IsActive']))
			cn.commit()
			# Обновляем сведения о ключевых словах
			Phrases=Banner['Phrases']
			for Phrase in Phrases:
				# Связка уникальности для фраз ID-баннера и ID-фразы
				# Добавляем ключевое слово
				try:
					cr.execute('INSERT INTO phrases(phraseid, bannerid)    VALUES (%s,%s);',(Phrase['PhraseID'],Phrase['BannerID']))
					cn.commit()
				except:
					cn.rollback()
				cr.execute('UPDATE phrases SET statusphrasemoderate=%s, autobroker=%s, isrubric=%s, contextprice=%s, \
				adgroupid=%s, campaignid=%s, price=%s,  \
				phrase=%s, autobudgetpriority=%s, statuspaused=%s \
				 WHERE phraseid='+str(Phrase['PhraseID'])+' AND bannerid='+str(Phrase['BannerID'])+';',\
				(Phrase['StatusPhraseModerate'], Phrase['AutoBroker'], Phrase['IsRubric'], Phrase['ContextPrice'],\
				Phrase['AdGroupID'], Phrase['CampaignID'], Phrase['Price'], Phrase['Phrase'], Phrase['AutoBudgetPriority'], Phrase['StatusPaused']))
				cn.commit()

print ('***************************************************')
print ('Обновление статистики по состоянию на: '+Tomorrow)
###################################
# Обновление статистики (по дням) #
###################################
# Сбор агрегирующей статистики по песочнице (по компаниям)
# Выборка только активных компаний!!!!
cr.execute('SELECT campaignid FROM campaigns WHERE isactive=True;')
CampaignIDs=cr.fetchall()
# Удаляем текущую статистику на указанную дату
cr.execute('DELETE FROM statistic WHERE statdate=\''+Tomorrow+'\';')
cn.commit()
# Обновляем статистику
for CampaignID in CampaignIDs:
	CID=CampaignID[0]
	Statistics=GetBannersStat(str(CID),Tomorrow,Tomorrow)['Stat']
	for BannerStat in Statistics:
		# Обновляем данные статистики за указанную дату (по умолчанию "Вчера")
		cr.execute('INSERT INTO statistic(campaignid, bannerid, clicks, showscontext, sumcontext, \
		sumsearch, clickscontext, shows, clickssearch, sum, showssearch, statdate)\
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',(CampaignID, BannerStat['BannerID'], BannerStat['Clicks'], BannerStat['ShowsContext'], BannerStat['SumContext'], \
		BannerStat['SumSearch'], BannerStat['ClicksContext'], BannerStat['Shows'], BannerStat['ClicksSearch'], BannerStat['Sum'], BannerStat['ShowsSearch'], Tomorrow))
		cn.commit()

cr.close()
cn.close()
