# LIBS
import re
import os
import gspread
import pandas as pd

from datetime import timedelta
from google.oauth2.service_account import Credentials
from google.cloud.bigquery import Client


class Collector:

    def __init__(self, period, info, scopes, key, title, path_save=None):
        """
        Проводит сбор данных. Собирает UTM-метки из гугл таблицы, и по ним собирает данные из bigquery

        Params:
            :info: google info в формате json для доступа к google табоицам и bigquery
            :scopes: ссылки на google ресурысы (google таблица и bigquery)
            :key: идентификатор таблици
            :title: название таблици
            :save_path: путь куда надо сохранить результат
        """
        self.__period = period
        self.__path_save = path_save

        # Авторизация на google
        __cred = Credentials.from_service_account_info(info, scopes=scopes)
        __gc = gspread.authorize(__cred)

        # Подключение к базам
        # UTM-база
        self.__ws = __gc.open_by_key(key).worksheet(title)
        # Bigquery
        self.__big_client = Client(credentials=__cred)

    def collect_utm(self, save=True):
        """
        Собирает DataFrame с utm метками

        Return: DataFrame с ресурсами их названиями и контентом
        """
        utm = self.__ws.get_all_values()

        utm = pd.DataFrame(utm[1:]).loc[:, :2]
        utm.columns = ['Source', 'Name', 'Content']
        utm.loc[utm['Content'].str.len() < 2, 'Content'] = None

        utm['Source'] = utm['Source'].str.replace('\t', '')
        utm['Source'] = utm['Source'].str.replace('"', '')
        utm['Source'] = utm['Source'].str.replace(' ', '')
        utm['Source'] = utm['Source'].str.split('/', expand=True)[0]

        if save:
            utm.to_csv(f'{self.__path_save}/utm-base.csv', index=False)

        return utm

    def assemble_query(self, template_query, lbls):
        """
        Собирает запрос для bigquery из шаблона

        Params:
            :template_query: шаблон запроса где 
                <period_order1> и <period_order2> - это период ставки, 
                <period_hit1> и <period_hit2> - это период прохода по рекламе
                <source> - это ресурсы по поторым будет проходить поиск
            :lbls: список ресурсов по которым будет проходить поиск

        Return: готовый запрос
        """
        query = re.sub('<period_order1>', str(self.__period[0]), template_query)
        query = re.sub('<period_order2>', str(self.__period[1] + timedelta(days=1)), query)

        query = re.sub('<period_hit1>', str(self.__period[0] - timedelta(days=15)), query)
        query = re.sub('<period_hit2>', str(self.__period[1] + timedelta(days=1)), query)

        query = re.sub('<source>', ', '.join([f"'{lbl}'" for lbl in lbls]), query)

        return query

    def collect_BQ(self, query, save=True):
        """
        Собирает данные из bigquery по запросу

        Params:
            :query: запрос по которому будет проходить поиск

        Return: DataFrame с результатами запроса
        """
        df = self.__big_client.query(query).result().to_dataframe().drop_duplicates().rename(columns={'id': 'BARCODE'})

        if save:
            df.to_csv(f'{self.__path_save}/bq_data_{self.__period[0]}-{self.__period[1]}.csv', index=False)

        return df
