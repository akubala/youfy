import sys
import youtube_dl
from initializer import SpotifySession


class Youfy:
    def __init__(self, config_file):
        self.spotify = SpotifySession(config_file=config_file)

    def convert(self):
        youtube_playlist_songs = self._get_youtube_playlist_content_ydl(
            playlist_url=self.spotify.config_data(param="youtube_playlist_id")
        )

        spotify_songs = self._find_spotify_songs(youtube_playlist_songs)

        spotify_playlist_uri = self._create_spotify_playlist(
            username=self.spotify.config_data(param="username"),
            playlist_name=self.spotify.config_data(param="playlist_name"),
            playlist_description=self.spotify.config_data(param="playlist_description")
        )

        self._add_songs_to_spotify_playlist(username=self.spotify.config_data(param="username"),
                                            playlist_id=spotify_playlist_uri,
                                            songs=spotify_songs)

    @staticmethod
    def _get_youtube_playlist_content_ydl(playlist_url):
        print("# [YouTube] Getting songs titles...")

        youtube_playlist_content = []

        ydl_config = {
            'extract_flat': True,
            'quiet': True
        }

        ydl = youtube_dl.YoutubeDL(ydl_config)

        with ydl:
            result = ydl.extract_info(url=playlist_url,
                                      download=False)

        for song in result["entries"]:
            print("* [YouTube] Got '{}'".format(song["title"]))
            youtube_playlist_content.append(song["title"])

        return youtube_playlist_content

    @staticmethod
    def _print_conversion_statistics(youtube_songs, missing_songs_titles, found_songs_uris):
        num_of_youtube_songs = len(youtube_songs)
        num_of_missing_songs = len(missing_songs_titles)
        num_of_found_songs = len(found_songs_uris)

        faulty_requests = num_of_youtube_songs - num_of_found_songs - num_of_missing_songs

        found_percentage = "{0:.0%}".format(num_of_found_songs / num_of_youtube_songs)
        missing_percentage = "{0:.0%}".format(num_of_missing_songs / num_of_youtube_songs)
        faulty_percentage = "{0:.0%}".format(faulty_requests / num_of_youtube_songs)

        print("# [Spotify] Results:\n"
              "* Found {} songs ({})\n"
              "* Missing {} songs ({})\n"
              "* Something bad happend with {} songs ({})".format(num_of_found_songs,
                                                                  found_percentage,
                                                                  num_of_missing_songs,
                                                                  missing_percentage,
                                                                  faulty_requests,
                                                                  faulty_percentage))

    def _find_spotify_songs(self, youtube_songs):
        print("# [Spotify] Searching on Spotify...")

        found_songs_uris = []
        missing_songs_titles = []

        for song_title in youtube_songs:
            try:
                print("* [Spotify] Searching for '{}'...".format(song_title))
                result = self.spotify.session.search(q=song_title, limit=1, type="track",
                                                     market=self.spotify.config_data(param="market"))
                found = result["tracks"]["total"]

                if found != 0:
                    for song in result["tracks"]["items"]:
                        song_uri = song["uri"]
                        print("* [Spotify] Got one! '{}'".format(song_uri))
                        found_songs_uris.append(song_uri)
                else:
                    print("* [Spotify] Got nothing for '{}'".format(song_title))
                    missing_songs_titles.append(song_title)

            except Exception as exc:
                print("# Something bad is happening!\n{}".format(exc))

        if len(found_songs_uris) == 0:
            print("# [Spotify] Got NOTHING!")
            sys.exit()

        self._print_conversion_statistics(youtube_songs, missing_songs_titles, found_songs_uris)

        return found_songs_uris

    def _create_spotify_playlist(self, username, playlist_name, playlist_description):
        print("# [Spotify] Creating playlist...")

        playlist = self.spotify.session.user_playlist_create(user=username,
                                                             name=playlist_name,
                                                             description=playlist_description)
        playlist_id = playlist["uri"]
        print("* [Spotify] Playlist '{}' / {}!".format(playlist_name, playlist_id))

        return playlist_id

    @staticmethod
    def _split_songs_into_chunks(songs_list, chunk_len):
        chunk_len = max(1, chunk_len)

        return [songs_list[i:i + chunk_len] for i in range(0, len(songs_list), chunk_len)]

    def _add_songs_to_spotify_playlist(self, username, playlist_id, songs):
        if len(songs) > 100:
            splitted_songs_list = self._split_songs_into_chunks(songs_list=songs, chunk_len=100)
        else:
            splitted_songs_list = [songs]

        nr_of_chunks = len(splitted_songs_list)

        for chunk_nr, single_chunk in enumerate(splitted_songs_list):
            results = self.spotify.session.user_playlist_add_tracks(user=username,
                                                                    playlist_id=playlist_id,
                                                                    tracks=single_chunk)

            print("# SUCCESS ({} of {})\n{}".format(chunk_nr + 1, nr_of_chunks, results))


if __name__ == "__main__":
    converter = Youfy(config_file="config_data.yaml")
    converter.convert()
