# Youfy

Youfy is a simple Python project that will gather your YouTube playlist content and in a dummy way will try to convert it to Spotify playlist.
This script is based on [youtube-dl](https://github.com/ytdl-org/youtube-dl/) and [Spotipy](https://github.com/plamere/spotipy). Big thanks to [Michał](https://github.com/Ernold11) for his contribution!

## Prequietes
* Spotify account and API credentials

## Usage

1. Prepare Python Virtual Environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.cfg
```

2. Fulfil all config data that is stored in one YAML file called `config_data.yaml`.

Necessary, default config values:
* `scope: playlist-modify-public`
* `trace: False`

Values to be fulfilled:
* `username` - Spotify user name
* `client_id` - Private client ID obtained from Spotify API
* `client_secret` - Private client secret number
* `redirect_uri` - Your configured redirect URI (e.g. `http://localhost/`)
* `market` - An ISO 3166-1 alpha-2 country code (e.g. `PL`)
* `playlist_name` - Future Spotify playlist name
* `playlist_description` - Future Spotify playlist description
* `youtube_playlist_id` - YouTube playlist ID

3. Run Youfy main script
```
python youfy.py
```

Be aware of notice below:
```
User authentication requires interaction with your
web browser. Once you enter your credentials and
give authorization, you will be redirected to
a url. Paste that url you were directed to to
complete the authorization.
```

## Note
Feel free to contribute!
