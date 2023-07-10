import json
import requests


from .model import constants
from .model import api
from .model import model
from .model import AccessTokenModel
from dataclasses import asdict

class MarketDataClient(object):

	def __init__(self, _config):

		self._config = _config
		self._header = {'Content-Type': 'application/json',
				'Accept': 'application/json'
			}
		self._access_token: AccessTokenModel = None
		self._get_access_token()

	def _make_post_request(self, _url, data: object = None):

		_header = self._header
		payload = json.dumps(asdict(data))
		_api_url = self._config.url + _url
		_response_obj = requests.post(_api_url, headers = _header, data = payload)
		_response = json.loads(_response_obj.content)
		return _response

	def _make_get_request(self, _url: str, req: object):

		_header = self._header
		_header["Authorization"] = "Bearer " + self._get_access_token()
		_api_url = self._config.url + _url
		_response_obj = requests.get(_api_url, params = asdict(req), headers = _header)
		_response = json.loads(_response_obj.content)
		return _response

	def _get_access_token(self):
		if self._access_token == None or self._access_token.is_expired():
			req = model.accessToken(self._config.consumerID, self._config.consumerSecret)
			payload = json.dumps(asdict( req))
			res = requests.post(self._config.url + api.MD_ACCESS_TOKEN , payload, headers=self._header)
			res_obj = model.Response(**(res.json()))
			if res_obj.status == 200:
				ac = model.AccessToken(**res_obj.data)
				self._access_token = AccessTokenModel(ac)
				return self._access_token.get_access_token()
			else:
				raise NameError(res_obj.message)
		return self._access_token.get_access_token()
     
	def access_token(self, _input_data: model.accessToken):
		return self._make_post_request(api.MD_ACCESS_TOKEN, data = _input_data)


	def securities(self, _input_data, _object: model.securities):
		return self._make_get_request(api.MD_SECURITIES, _object)

	def securities_details(self, _input_data,_object: model.securities_details):
		return self._make_get_request(api.MD_SECURITIES_DETAILS, _object)

	def index_components(self, _input_data,_object:model.index_components):
		return self._make_get_request(api.MD_INDEX_COMPONENTS,  _object)

	def index_list(self,_input_data, _object: model.index_list):
		return self._make_get_request(api.MD_INDEX_LIST,   _object)

	def daily_ohlc(self, _input_data, _object: model.daily_ohlc):
		return self._make_get_request(api.MD_DAILY_OHLC,  _object)

	def intraday_ohlc(self, _input_data, _object: model.intraday_ohlc):
		return self._make_get_request(api.MD_INTRADAY_OHLC,  _object)

	def daily_index(self, _input_data, _object: model.daily_index):
		return self._make_get_request(api.MD_DAILY_INDEX,  _object)

	def daily_stock_price(self, _input_data, _object: model.daily_stock_price):
		return self._make_get_request(api.MD_DAILY_STOCK_PRICE,  _object)

	def backtest(self, _input_data, _object: model.backtest):
		return self._make_get_request(api.MD_BACKTEST,  _object)
