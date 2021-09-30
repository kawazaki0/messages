import os
import json
import pdb
import pprint

path = '../messages_new/inbox'
list_of_files = []
for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith('.json'):
            list_of_files.append(os.sep.join([dirpath, filename]))


def recurisve_decode(root):
    if isinstance(root, str):
        return root.encode('iso-8859-1').decode('utf-8')
    if isinstance(root, list):
        return list(map(recurisve_decode, root))
    if isinstance(root, dict):
        return dict((k, recurisve_decode(v)) for k, v in root.items())
    return root


messages = []

for f in list_of_files:
    with open(f, 'r') as ff:
        conversation = recurisve_decode(json.load(ff))

        for message in conversation['messages']:
            if message['type'] == 'Generic':
                messages.append({
                    # 'sender_name': message['sender_name'],
                    # 'participants': [p['name'] for p in conversation['participants']],
                    'count': 1,
                    'timestamp_ms': message['timestamp_ms'],
                    # 'type': message['type'],
                    'content_length': len(message.get('content', ''))
                })


# with open('messages.json', 'w') as f:
#     json.dump(messages, f)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_json(json.dumps(messages))
df["timestamp_ms"].astype("datetime64")
# print(df["timestamp_ms"].dt.month)
df.groupby([df["timestamp_ms"].dt.year,df["timestamp_ms"].dt.month]).count().plot.bar(y='count')
# df['']
# df.drop('content_length', axis=1, )
# df.drop(columns='sender_name')
# print(df.head())
# df.hist()
plt.show()

