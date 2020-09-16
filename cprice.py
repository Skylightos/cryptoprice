import requests
import time
from datetime import datetime


btc_api = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
ifttt = "https://maker.ifttt.com/trigger/{}/with/key/9d6Vsf4-9U2d3bIm2l8yr"

def getBtcPrice():
	btc_response = requests.get(btc_api).json()
	btc_price =  btc_response["bitcoin"]["usd"]
	return btc_price

def sendWebhook(event, value):
	data = {'value1': value}
	ifttt_url = ifttt.format(event)
	requests.post(ifttt_url, json=data)

def formPrice(btc_history):
	rows = []
	for bp in btc_history:
		date = bp["date"].strftime("%d.%m.%Y.%H.%M")
		price = bp["price"]
		row = "{}: $<b>{}</b>".format(date, price)
		rows.append(row)

	return "<br>".join(rows)

btc_min_price = 10000

def main():
	btc_history = []
	while True:
		price = getBtcPrice()
		date = datetime.now()
		notification = btc_history.append({'date':date, 'price':price})

		if price < btc_min_price:
			sendWebhook("btc",price)

		if len(btc_history) == 5:
			sendWebhook("btc_update", formPrice(btc_history))
			btc_history = []

		time.sleep()


if __name__ == "__main__":
	main()




