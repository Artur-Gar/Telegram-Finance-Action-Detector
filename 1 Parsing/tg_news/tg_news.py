import pandas as pd
import os

def get_needed_keys(message, keys) -> dict:
    '''
    объект pyrogram.message -> словарь с нужными ключами keys (id, date, text)
    '''
    new_message = {}
    needed_keys = [(attr, getattr(message, attr)) for attr in dir(message) if attr in keys] # extract only specific keys
    #needed_keys = [(attr, getattr(message, attr)) for attr in dir(message)] # extract all keys
    new_message = { key: value for key, value in needed_keys }
    print()
    return new_message

# Checks for an Excel file here: if it exists, the data has already been exported
def save_tg_data(data, data_path):
    for date in data.date.unique():
        data_prom = data[data.date == date]
        if len(data_prom) > 0:
            fl_name = date.strftime('%Y-%m-%d') + '.xlsx'
            fl_name = os.path.join(data_path, fl_name)
            if os.path.isfile(fl_name):
                data_existed = pd.read_excel(fl_name)
                data_prom = pd.concat([data_existed, data_prom])
                del data_existed
                data_prom = data_prom.drop_duplicates(subset = ['text_id'])
                data_prom.to_excel(fl_name, index = False)
            else:
                data_prom.to_excel(fl_name, index = False)
        del data_prom

# loads messages from the channel
def load_tg_news(date_start, app, channels, channel_ids, data_path, keys, limit):
    with app:
        print('start')
        offset_msg = 0
        limit = limit
        i = 0
        for i in range(len(channels)):
            channel = channels[i]
            channel_id = channel_ids[i]
            print(channel)
            print(channel_id)
            messages = list(app.get_chat_history(chat_id = channel_id, limit = limit, offset_id = offset_msg)) # pyrogram.message object
            messages_to_df = []
            for message in messages:
                messages_to_df.append(get_needed_keys(message, keys = keys))
            df = pd.DataFrame(messages_to_df)
            df['text'] = df.apply(lambda x: x['caption'] if x['text'] is None else x['text'], axis = 1)  ## if text is emoty, then put message text into caption
            df = df[df.text.apply(lambda x: x is not None)]
            df = df[df.text.apply(lambda x: len(x)>=5)]
            ## adjust dates
            df['datetime'] = df.date
            df['date'] = df['datetime'].dt.date
            df['time'] = df['datetime'].dt.time
            df = df.drop(columns = ['datetime'])
            df = df[df.date >= date_start].reset_index().drop(columns = 'index')
            df['source'] = channel
            df['source_id'] = channel_id
            df['text_id'] = df.apply(lambda x: str(x.source_id) + '_' + str(x.id), axis = 1)
            save_tg_data(data = df, data_path = data_path)
    print('end')