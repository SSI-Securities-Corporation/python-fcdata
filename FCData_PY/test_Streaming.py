# import ssi_fc_data
import config
import json
import ssi_fc_data



#get market data message
def get_market_data(message):
	print(message)


#get error
def getError(error):
	print(error)


#main function
def main():


	selected_channel = input("Please select channel: ")
	ssi_fc_data.Market_Data_Stream(config, get_market_data, getError, selected_channel)

	


main()