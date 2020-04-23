import spotipy
import yaml


class SpotifySession:
    def __init__(self, config_file=None):
        self.yaml_data = {}

        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "config_data.yaml"

        self._read_config()
        self.session = self.init_spotify_session()

    def _read_config(self):
        with open(self.config_file, "r") as stream:
            self.yaml_data = yaml.safe_load(stream)

    def config_data(self, param=None):
        if not self.yaml_data:
            self._read_config()
        if not param:
            return self.yaml_data

        return self.yaml_data[param]

    def init_spotify_session(self, username=None, scope=None, client_id=None, client_secret=None, redirect_uri=None):
        if not username:
            username = self.config_data(param="username")
        if not scope:
            scope = self.config_data(param="scope")
        if not client_id:
            client_id = self.config_data(param="client_id")
        if not client_secret:
            client_secret = self.config_data(param="client_secret")
        if not redirect_uri:
            redirect_uri = self.config_data(param="redirect_uri")

        token = spotipy.util.prompt_for_user_token(username=username,
                                                   scope=scope,
                                                   client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri)
        session = spotipy.Spotify(auth=token)
        session.trace = self.config_data(param="trace")

        return session
