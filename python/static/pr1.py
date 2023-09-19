#caf1e252-ceeb-4009-8623-408e0230f1ee
import requests 
import json
from tkinter import Tk, Label, Button
import gym

api_key = 'caf1e252-ceeb-4009-8623-408e0230f1ee'  
headers = {'X-CMC_PRO_API_KEY': api_key}
params = {'slug':'bitcoin'}
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
  
window = Tk()

price_lbl = Label(window, text="") 
price_lbl.grid(column=0, row=0)

vol_lbl = Label(window, text="")
vol_lbl.grid(column=1, row=0) 

def update_data():

  response = requests.get(url, headers=headers, params=params)
  print(response.json())
  data = response.json()['data']['1']

  price_usd = data['quote']['USD']['price']
  vol_24h = data['quote']['USD']['volume_24h']

  price_lbl.config(text=str(price_usd) + " USD")
  vol_lbl.config(text=str(vol_24h) + " USD")

  window.after(3000, update_data) 

update_data()
window.mainloop()