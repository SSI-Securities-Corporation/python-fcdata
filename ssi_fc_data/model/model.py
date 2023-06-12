from dataclasses import dataclass

@dataclass
class accessToken:
  consumerID: str = ''
  consumerSecret: str = ''

@dataclass
class securities:
  market: str = ''
  pageIndex: int = 1
  pageSize: int = 100

@dataclass
class securities_details:
  market: str = ''
  symbol: str = ''
  pageIndex: str = ''
  pageSize: str = ''

@dataclass
class index_components:
  indexCode: str = ''
  pageIndex: int = 1
  pageSize: int = 100


@dataclass
class index_list:
  exchange: str = ''
  pageIndex: int = 1
  pageSize: int = 100


@dataclass
class daily_ohlc:
  symbol: str = ''
  fromDate: str = ''
  toDate: str = ''
  pageIndex: int = 1
  pageSize: int = 100
  ascending: bool = True

@dataclass
class intraday_ohlc:
  symbol: str = ''
  fromDate: str = ''
  toDate: str = ''
  pageIndex: int = 1
  pageSize: int = 100
  ascending: bool = True
  resolution: int = 1

@dataclass
class daily_index:
  requestId: str = ''
  indexId: str = ''
  fromDate: str = ''
  toDate: str = ''
  pageIndex: int = 1
  pageSize: int = 100
  orderBy: str = ''
  order: str = ''

@dataclass
class daily_stock_price:
  symbol: str = ''
  fromDate: str = ''
  toDate: str = ''
  pageIndex: int = 1
  pageSize: int = 100
  market: str = ''

@dataclass
class backtest:
  selectedDate: str = ''
  symbol: str = ''

@dataclass
class Response():
    status: int = 500
    message: str = ''
    data: object = None

@dataclass
class AccessToken(object):
    accessToken: str



