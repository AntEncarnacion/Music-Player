from tkinter import *
from pygame import mixer
from pathlib import PureWindowsPath, Path
from time import sleep
import sqlite3
from sqlite3 import Error


#############################################################
# Database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()



def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_song(conn, song):
    """
    Create a new project into the songs table
    :param conn:
    :param song:
    :return: song id
    """
    sql = ''' INSERT INTO songs(title,length,artist_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def insert_album(conn, album):
    """
    Create a new project into the albums table
    :param conn:
    :param album:
    :return: album id
    """
    sql = ''' INSERT INTO albums(title)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def insert_artist(conn, artist):
    """
    Create a new project into the artists table
    :param conn:
    :param artist:
    :return: artist id
    """
    sql = ''' INSERT INTO artists(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def insert_playlist(conn, playlist):
    """
    Create a new project into the playlists table
    :param conn:
    :param playlist:
    :return: playlist id
    """
    sql = ''' INSERT INTO playlists(playlist_id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def insert_playlist_song(conn, playlist_song):
    """
    Create a new project into the playlist_songs table
    :param conn:
    :param playlist_song:
    """
    sql = ''' INSERT INTO playlists(playlist_id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

#############################################################
# Mixer

def load_song(path):
    mixer.music.load(path)

def play_song():
    mixer.music.play()

def volume_song(vol):
    mixer.music.set_volume(vol)

def resume_song():
    mixer.music.unpause()

def stop_song():
    mixer.music.stop()

#############################################################
# Main

if __name__ == '__main__':

    ##########################################
    # Directories
    DIRECTORY = Path(str(PureWindowsPath("C:/Users/Anthony/Music/Spotify/")))
    songs = [Path(i) for i in sorted(DIRECTORY.glob('*.mp3'))]

    ##########################################
    # Database
    create_connection(r".\music_player.db")
    sql_create_songs_table = """ CREATE TABLE IF NOT EXISTS songs (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        length integer,
                                        FOREIGN KEY (artist_id) REFERENCES artists (id)
                                    ); """
    sql_create_album_table = """ CREATE TABLE IF NOT EXISTS album (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    sql_create_artists_table = """ CREATE TABLE IF NOT EXISTS artists (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    sql_create_playlist_songs_table = """ CREATE TABLE IF NOT EXISTS playlist_songs (
                                        FOREIGN KEY (playlist_id) REFERENCES playlists (id)
                                        FOREIGN KEY (artist_id) REFERENCES artists (id)
                                    ); """
    sql_create_playlists_table = """ CREATE TABLE IF NOT EXISTS playlists (
                                        FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                                        name text NOT NULL
                                    ); """

    if conn is not None:
        # create songs table
        create_table(conn, sql_create_songs_table)

        # create album table
        create_table(conn, sql_create_album_table)

        # create artists table
        create_table(conn, sql_create_artists_table)

        # create playlist songs table
        create_table(conn, sql_create_playlist_songs_table)
        
        # create playlists table
        create_table(conn, sql_create_playlists_table)

    else:
        print("Error! cannot create the database connection.")

    ##########################################
    # Mixer
    mixer.init()

    ##########################################
    # Execution/Testing
    load_song(songs[0])
    play_song()

    while mixer.music.get_busy():
        sleep(1)