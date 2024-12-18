import json

from django.contrib.auth.backends import BaseBackend

from provider.oauth2.models import AccessToken
from provider.utils import now


class BearerTokenAuthentication(BaseBackend):
    def authenticate_header(self, request):
        return 'Bearer'

    def authenticate(self, headers):
        try:
            headers_dict = dict(headers)
            headers_json = json.dumps(headers_dict)
            bearer_token = json.loads(headers_json)['Authorization']
            bearer_token = bearer_token.split(' ')[1]
            token = AccessToken.objects.filter(token=bearer_token, expires__gt=now(), client__client_id='555861d13a7ab9400654').first()

            return True, token.user
        except AccessToken.DoesNotExist:
            return False, None
        # TODO: remove this when in production
        except Exception as e:
            return False, None
