# import ssi_fc_data
import config
import json
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient



#get market data message
def get_market_data(message):
	print(message)


#get error
def getError(error):
	print(error)


#main function
def main():


	selected_channel = input("Please select channel: ")
	mm = MarketDataStream(config, MarketDataClient(config))
	mm.start(get_market_data, getError, selected_channel)
	message = None
	while message != "exit()":
		message = input(">> ")
		if message is not None and message != "" and message != "exit()":
			mm.swith_channel(message)
	


main()