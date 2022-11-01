my_url = 'https://api.gurbaninow.com/v2/hukamnama/today'


import requests
import pandas as pd

response = requests.get(my_url)
dictr = response.json()

# recs = dictr['result']['records']
# df = 

# ==== banis
# print( pd.json_normalize(dictr) )
# pd.json_normalize( dictr ).to_csv('banis.csv', index=False, encoding='utf-8-sig')

# ==== banis 1
# print( pd.json_normalize( dictr['bani'] ) )
# pd.json_normalize( dictr['bani'] ).to_csv('banis1.csv', index=False, encoding='utf-8-sig')

# ==== today
print(pd.json_normalize( dictr ))

# pd.json_normalize( dictr['hukamnama'] ).to_csv('today.csv', index=False, encoding='utf-8-sig')