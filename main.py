# LIBS
# Custom
from settings import *

from utils import open_file, last_month, half_month, create_dir
from collector import Collector

# System
import json
from datetime import date


# INITS
# Период
period = last_month() if date.today().day <= 15 else half_month()


# Создание папок
create_dir(PATH_TO_SOURCE)


# google collector
info = open_file(INFO)
info = json.loads(info)

collector = Collector(period, info, SCOPES, KEY, TITLE, PATH_TO_SOURCE)


# COLLECT
df_utm_base = collector.collect_utm()

query = collector.assemble_query(
    template_query=open_file(TEMPLATE_BIGQUERY),
    lbls=df_utm_base['Source'].unique()
)

df = collector.collect_BQ(query)

print(df)
