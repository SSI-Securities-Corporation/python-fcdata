import base64
from datetime import datetime
import json
from .model import AccessToken

class AccessTokenModel(object):

	def __init__(self, access_token: AccessToken):
    
		tokenSplit = access_token.accessToken.split(".")
		s = tokenSplit[1]
		s += "=" * ((4 - len(s) % 4) % 4) #ugh
		jj = json.loads((base64.b64decode(s)).decode("utf-8"))
		self._token_expire_at = datetime.fromtimestamp(jj['exp'])
		self._access_token = access_token.accessToken

	def get_access_token(self):
		return self._access_token

	def is_expired(self):
		delta = self._token_expire_at - datetime.now()
		if delta.total_seconds() < 3600:
			return True
		return False
