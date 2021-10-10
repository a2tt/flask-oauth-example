import time
import requests
from urllib.parse import urlencode

from flask import Flask, request, url_for, jsonify, abort, redirect

from oauth_config import oauth_config
import settings

app = Flask(__name__)


@app.route('/login/oidc')
def login():
    return f'''
    <h1><a href="{url_for('.oidc_login', provider='twitch')}">트위치</a></h1>
    '''


@app.route('/login/oidc/<provider>')
def oidc_login(provider):
    try:
        auth_uri = oauth_config[provider]['auth_uri']
        params = {
            # 'response_type': 'token+id_token',
            'response_type': 'token',
            'client_id': settings.twitch_client_id,
            'redirect_uri': url_for('oidc_login_callback', provider=provider, _external=True),
            'scope': '+'.join(['openid'])
        }

        login_url = auth_uri + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
        return redirect(login_url)
    except KeyError:
        abort(404)


@app.route('/login/oidc/<provider>/callback')
def oidc_login_callback(provider):
    """ fragment 는 client-side 이기 때문에 서버쪽에 전달되지 않는다. """
    print(request.url)
    print(request.pragma)
    print(request.full_path)
    print(request.path)

    return str(request.url)


if __name__ == '__main__':
    url = 'https://id.twitch.tv/oauth2/authorize'
    params = {
        'response_type': 'token+id_token',
        'client_id': settings.twitch_client_id,
        'redirect_uri': 'http://127.0.0.1:5000',
        'scope': '+'.join(['openid'])
    }

    params = '&'.join([f'{k}={v}' for k, v in params.items()])
    app.run('0.0.0.0', port=5000, debug=True)

