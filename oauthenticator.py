"""
Custom Authenticator to use GitHub OAuth with JupyterHub

Most of the code c/o Kyle Kelley (@rgbkrk)
"""


import os
import json

from tornado import gen, web

from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join

from mwoauth import ConsumerToken, Handshaker

from IPython.utils.traitlets import Unicode


class MWLoginHandler(BaseHandler):
    def get(self):
        consumer_token = ConsumerToken(
            self.authenticator.mw_consumer_key,
            self.authenticator.mw_consumer_secret
        )

        handshaker = Handshaker(
            self.authenticator.mw_index_url, consumer_token
        )

        redirect, request_token = handshaker.initiate()

        self.set_secure_cookie('mw_oauth_request_token', json.dumps(request_token))
        self.log.info('oauth redirect: %r', redirect)

        self.redirect(redirect)


class MWOAuthHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        consumer_token = ConsumerToken(
            self.authenticator.mw_consumer_key,
            self.authenticator.mw_consumer_secret
        )

        handshaker = Handshaker(
            self.authenticator.mw_index_url, consumer_token
        )
        request_token = json.loads(self.get_secure_cookie('mw_oauth_request_token'))
        access_token = handshaker.complete(request_token, self.request.query)

        identity = handshaker.identify(access_token)
        if identity and 'username' in identity:
            user = self.user_from_username(identity['username'])
            self.set_login_cookie(user)
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))
        else:
            # todo: custom error page?
            raise web.HTTPError(403)


class MWOAuthenticator(Authenticator):
    mw_consumer_key = Unicode(os.environ.get('MW_CONSUMER_KEY', ''),
                              config=True)
    mw_consumer_secret = Unicode(os.environ.get('MW_CONSUMER_SECRET', ''),
                                 config=True)
    mw_index_url = Unicode(
        os.environ.get('MW_INDEX_URL', 'https://meta.wikimedia.org/w/index.php'),
        config=True)

    def login_url(self, base_url):
        return url_path_join(base_url, 'oauth_login')

    def get_handlers(self, app):
        return [
            (r'/oauth_login', MWLoginHandler),
            (r'/oauth_callback', MWOAuthHandler),
        ]
