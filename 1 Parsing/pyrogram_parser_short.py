from pyrogram import Client
import datetime
import os
import yaml

from tg_news.tg_news import load_tg_news

config_path = 'configs/config_short.yml'
with open(config_path, encoding = 'utf-8') as fh:
    read_config = yaml.load(fh, Loader=yaml.FullLoader)

api_id = os.getenv('telegram_api_id')  
api_hash = os.getenv('telegram_api_hash') 
channels = read_config['channels']
channel_ids = read_config['channel_ids']
keys = read_config['keys']
limit = read_config['limit']
data_path = read_config['data_path']
date_start = read_config['date_start']

if date_start:
    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
else:
    date_start = datetime.date.today() - datetime.timedelta(days = 1)
app = Client('my_account', api_id, api_hash, sleep_threshold = 60) ## my_account is your own session file here

if __name__ == "__main__":
    all_messages = []
    load_tg_news(date_start = date_start, app = app, channels = channels, channel_ids = channel_ids, data_path = data_path, keys = keys, limit = limit)

