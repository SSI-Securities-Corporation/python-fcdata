# import ssi_fc_trading
from ssi_fc_data import fc_md_client , model
import config


client = fc_md_client.MarketDataClient(config)
def md_access_token():
	print(client.access_token(config))

def md_get_securities_list():
    req = model.securities('HNX', 1,100)
    print(client.securities(config, req))

def md_get_securities_details():
    req = model.securities_details('HNX', 'ACB', 1, 100)
    print(client.securities_details(config, req))

def md_get_index_components():
	print(client.index_components(config, model.index_components('vn100', 1, 100)))

def md_get_index_list():
	print(client.index_list(config, model.index_list('hnx', 1, 100)))

def md_get_daily_OHLC():
	print(client.daily_ohlc(config, model.daily_ohlc('ssi', '15/10/2020', '15/10/2020', 1, 100, True)))

def md_get_intraday_OHLC():
	print(client.intraday_ohlc(config, model.intraday_ohlc('fpt', '15/10/2020', '15/10/2020', 1, 100, True, 1)))

def md_get_daily_index():
	print(client.daily_index(config, model.daily_index( '123', 'VN100', '15/10/2020', '15/10/2020', 1, 100, '', '')))

def md_get_stock_price():
	print(client.daily_stock_price(config, model.daily_stock_price ('fpt', '15/10/2020', '15/10/2020', 1, 100, 'hose')))



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