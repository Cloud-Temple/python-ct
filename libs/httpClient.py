"""
Http client to facilitate communication of API services
"""

from json.decoder import JSONDecodeError
from requests import Request, Response, Session, RequestException
import requests
import jwt
from datetime import datetime


class HttpClientException(Exception):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        if self.reason is not None:
            return "%s - %s" % (self.message, str(self.reason))
        return self.message


class HttpClient:
    def __init__(self, url: str, token_id: str, token_secret: str):
        self.url = url
        self.token_id = token_id
        self.token_secret = token_secret
        self.bearer_token = None
        self.jwt_decoded = None

    def get(self, url: str):
        """Execution of a GET type request"""
        return self.__execute(Request("get", url))

    def post(self, url: str, data: {} = None):
        """Execution of a POST type request"""
        return self.__execute(Request("post", url, json=data))

    def patch(self, url: str, data: {} = None):
        """Execution of a PATCH type request"""
        return self.__execute(Request("patch", url, json=data))

    def delete(self, url: str, data: {} = None):
        """Execution of a DELETE type request"""
        return self.__execute(Request("delete", url, json=data))

    def json_response(self, resp: Response):
        """Convert the HTTP response to a json type response"""
        try:
            return resp.json()
        except JSONDecodeError as err:
            if hasattr(self, 'logger'):
                self.logger.error("invalid json (%s - %s - %s)", resp.request.method, resp.url, err.msg)
            raise HttpClientException("invalid json", err.msg) from err

    def error_response(self, resp: Response):
        """Throws an exception of type "HttpClientException"""
        if hasattr(self, 'logger'):
            self.logger.error("invalid response (%s - %s - %d - %s)", resp.request.method, resp.url, resp.status_code,
                              resp.content)
        raise HttpClientException("invalid response", resp.content)

    def auth(self):
        if not self.bearer_token:
            self.__login()
        else:
            exp_epoch = datetime.fromtimestamp(self.jwt_decoded['exp'])
            time_now = datetime.now()
            diff = (exp_epoch - time_now).total_seconds() / 60
            if 10 > diff > 1:
                if hasattr(self, 'logger'):
                    self.logger.debug("10 > diff > 1 - token is valide")
                self.__refresh()
            elif diff < 1:
                self.__login()

    def __login(self):
        try:
            self.headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }

            pat = {
                'id': self.token_id,
                'secret': self.token_secret
            }

            bearer_request = requests.post(url=self.url + "/api/iam/v2/auth/personal_access_token", headers=self.headers,
                                           json=pat)

            if bearer_request.status_code != 200:
                raise HttpClientException("Cannot generate bearer token", bearer_request.reason)
            else:
                self.jwt_decoded = jwt.decode(bearer_request.text, options={"verify_signature": False})
                self.bearer_token = bearer_request.text

        except RequestException as err:
            if hasattr(self, 'logger'):
                self.logger.error("request exception %s", err)
            raise HttpClientException("request exception", err) from err

    def __refresh(self):
        try:
            headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json',
                'Authorization': "Bearer " + self.bearer_token
            }

            refreshToken = {
                'refreshToken': self.bearer_token
            }

            # Retrieve bearer
            bearer_request = requests.post(url=self.url + "/api/iam/v2/auth/refresh", headers=headers,
                                           json=refreshToken)

            if bearer_request.status_code != 200:
                raise HttpClientException("Cannot generate bearer token", bearer_request.reason)
            else:
                self.bearer_token = bearer_request.json()['refresh_token']

        except RequestException as err:
            if hasattr(self, 'logger'):
                self.logger.error("request exception %s", err)
            raise HttpClientException("request exception", err) from err

    def __execute(self, req: Request) -> Response:
        self.auth()
        try:
            self.headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json',
                'Authorization': "Bearer " + self.bearer_token
            }

            req.url = self.url + req.url
            req.headers = self.headers
            req_prepare = req.prepare()
            return Session().send(req_prepare, timeout=10)
        except RequestException as err:
            if hasattr(self, 'logger'):
                self.logger.error("request exception %s", err)
            raise HttpClientException("request exception", err) from err
