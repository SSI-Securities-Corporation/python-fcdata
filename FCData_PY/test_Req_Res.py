# import ssi_fc_trading
import ssi_fc_data
import config



def md_access_token():
	print(ssi_fc_data.access_token(config))

def md_get_securities_list():
	print(ssi_fc_data.securities(config, 'HNX', 1, 100))

def md_get_securities_details():
	print(ssi_fc_data.securities_details(config, 'HNX', 'ACB', 1, 100))

def md_get_index_components():
	print(ssi_fc_data.index_components(config, 'vn100', 1, 100))

def md_get_index_list():
	print(ssi_fc_data.index_list(config, 'hnx', 1, 100))

def md_get_daily_OHLC():
	print(ssi_fc_data.daily_ohlc(config, 'ssi', '15/10/2020', '15/10/2020', 1, 100, True))

def md_get_intraday_OHLC():
	print(ssi_fc_data.intraday_ohlc(config, 'fpt', '15/10/2020', '15/10/2020', 1, 100, True, 1))

def md_get_daily_index():
	print(ssi_fc_data.daily_index(config, '123', 'VN100', '15/10/2020', '15/10/2020', 1, 100, '', ''))

def md_get_stock_price():
	print(ssi_fc_data.daily_stock_price(config, 'fpt', '15/10/2020', '15/10/2020', 1, 100, 'hose'))



def main():
	while True:
		print('11  - Securities List')
		print('12  - Securities Details')
		print('13  - Index Components')
		print('14  - Index List')
		print('15  - Daily OHLC')
		print('16  - Intraday OHLC')
		print('17  - Daily index')
		print('18  - Stock price')
		print('19  - Get access token')
		value = input('Enter your choice: ')

		if value == '11':
			md_get_securities_list()
		elif value == '12':
			md_get_securities_details()
		elif value == '13':
			md_get_index_components()
		elif value == '14':
			md_get_index_list()
		elif value == '15':
			md_get_daily_OHLC()
		elif value == '16':
			md_get_intraday_OHLC()
		elif value == '17':
			md_get_daily_index()
		elif value == '18':
			md_get_stock_price()
		elif value == '19':
			md_access_token()

if __name__ == '__main__':
	main()