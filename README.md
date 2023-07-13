[![Semantic Release](https://github.com/SSI-Securities-Corporation/python-fcdata/actions/workflows/publish.yaml/badge.svg)](https://github.com/SSI-Securities-Corporation/python-fcdata/actions/workflows/publish.yaml)
# Installation
#### From tar ball (most stable)
If you download file [fc-data.py.zip](https://github.com/SSI-Securities-Corporation/python-fcdata/releases/latest/download/fc-data.py.zip), we include tarball file:
``` python
pip install dist/ssi-fc-data-2.1.0.tar.gz
```
#### Install behind proxy
```python
pip install --trusted-host pypi.org --trusted-host
files.pythonhosted.org --proxy=http://<username>:<password>@<host>:<port> ssi-fc-data
```
Or
```python
pip install --trusted-host pypi.org --trusted-host
files.pythonhosted.org --proxy=http://<username>:<password>@<host>:<port> dist/ssi-fc-data-2.1.0.tar.gz
```

#### Pypi
``` python
pip install ssi-fc-data
```

# Sample usage
## Config
Get `consumerID` and `consumerSecret` from [iBoard](https://iboard.ssi.com.vn/support/api-service/management)
```python
auth_type = 'Bearer'
consumerID = ''
consumerSecret = ''

url = 'https://fc-data.ssi.com.vn/'
stream_url = 'https://fc-data.ssi.com.vn/'
```
## API
``` python
from ssi_fc_data import fc_md_client , model
import config


client = fc_md_client.MarketDataClient(config)
def md_get_securities_list():
    req = model.securities('HNX', 1, 100)
    print(client.securities(config, req))

def md_get_securities_details():
    req = model.securities_details('HNX', 'ACB', 1, 100)
    print(client.securities_details(config, req))

def main():
    
    md_get_securities_list()
    md_get_securities_details()
        

if __name__ == '__main__':
	main()
```

## Streaming Data
``` python
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
```
