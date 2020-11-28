import sqlite3


class db_playlist:
    def __init__(self, title):
        self.title = title
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        self.exist = len(cursor.execute(f'SELECT * FROM playlists '
                                        f'WHERE title = "{title}"').fetchall())
        if not self.exist:
            cursor.execute(f'INSERT INTO playlists(title) VALUES("{title}")')
        self.id = cursor.execute(f'SELECT id FROM playlists '
                                 f'WHERE title = "{title}"').fetchone()[0]
        connect.commit()
        connect.close()

    def is_exist(self):
        return self.exist

    def add_song(self, song):
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute(f'INSERT INTO relations(playlist_id, song_id)'
                       f'VALUES({self.id}, {song.id})')
        connect.commit()
        connect.close()

    def remove_song(self, song_id):
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute(f'DELETE FROM relations WHERE playlist_id == {self.id}'
                       f'AND song_id == {song_id}')
        connect.commit()
        connect.close()

    def delete_playlist(self):
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute(f'DELETE FROM playlists WHERE id == "{self.id}"')
        cursor.execute(f'DELETE FROM relations WHERE playlist_id == {self.id}')
        connect.commit()
        connect.close()


class db_song:
    def __init__(self, path):
        self.path = path
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        exist = len(cursor.execute(f'SELECT id FROM songs '
                                   f'WHERE path = "{path}"').fetchall())
        if not exist:
            cursor.execute(f'INSERT INTO songs(path) VALUES("{path}")')
        self.id = cursor.execute(f'SELECT id FROM songs '
                                 f'WHERE path = "{path}"').fetchone()[0]
        connect.commit()
        connect.close()

    def delete_song(self):
        connect = sqlite3.connect("database.db")
        cursor = connect.cursor()
        cursor.execute(f'DELETE FROM songs WHERE path == "{self.path}"')
        cursor.execute(f'DELETE FROM relations WHERE playlist_id == {self.id}')
        connect.commit()
        connect.close()


def songs_of_playlist(title):
    playlist = db_playlist(title)
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    records = cursor.execute(f"""SELECT path FROM songs
                                 WHERE id IN (SELECT song_id FROM relations 
                                              WHERE playlist_id == {playlist.id})""").fetchall()
    connect.commit()
    connect.close()
    return [song_id[0] for song_id in records]


def get_playlists():
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()
    records = cursor.execute('SELECT title FROM playlists').fetchall()
    connect.close()
    return [playlist_id[0] for playlist_id in records]
