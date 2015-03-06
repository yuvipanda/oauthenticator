# MWOAuthenticator

MediaWiki OAuth + JuptyerHub Authenticator = MWOAuthenticator

Based off of (GitHubOAuthenticator](https://github.com/jupyter/oauthenticator)

## Installation

First, install dependencies:

    pip install -r requirements.txt

Then, install the package:

    python setup.py install

## Setup

First, you'll need to create a [Mediawiki OAuth
application](https://www.mediawiki.org/wiki/Special:OAuthConsumerRegistration/propose).
Make sure the callback URL is:

    http[s]://[your-host]/hub/oauth_callback

Where `[your-host]` is where your server will be running. Such as
`example.com:8000`.

Then, add the following to your `jupyterhub_config.py` file:

    c.JupyterHub.authenticator_class = 'oauthenticator.MWOAuthenticator'


You will additionally need to specify the consumer token, consumer secret, and
full URL to the index.php of your mediawiki installation. For example,

    c.MWOAuthenticator.mw_consumer_key = 'galkshfgljshgflsagafg'
    c.MWOAuthenticator.mw_consumer_secret = 'gjlhsdglfjhdgljhsdljfghfldsjghjdlghg'
    c.MWOAuthenticator.mw_index_url = 'https://meta.wikimedia.org/w/index.php'
