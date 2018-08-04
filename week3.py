# Create a Musical Track database. Multi-Table relational SQL. Makes a final database table that includes linked artist, genre, album, track
# Homework assignment done as part of Using Databases with Python Coursera course.

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('tracksdb.sqlite')
cu = conn.cursor()

cu.executescript('''DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)
''')

def lookfor(d, k):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == k :
            found = True
    return None


xml_file = input('Enter file: ')
if len(xml_file) < 1: xml_file = 'Library.xml'
data = ET.parse(xml_file)
all_data = data.findall('dict/dict/dict')

for entry in all_data:
    if (lookfor(entry, 'Track ID') is None): continue

    name = lookfor(entry, 'Name')
    artist = lookfor(entry, 'Artist')
    album = lookfor(entry, 'Album')
    count = lookfor(entry, 'Play Count')
    rating = lookfor(entry, 'Rating')
    length = lookfor(entry, 'Total Time')
    genre = lookfor(entry,'Genre')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, genre, count, rating, length)

    cu.execute('''INSERT OR IGNORE INTO Artist (name) VALUES ( ? )''', (artist,))
    cu.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    artist_id = cu.fetchone()[0]

    cu.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )''', (album, artist_id))
    cu.execute('SELECT id FROM Album WHERE title = ? ', (album,))
    album_id = cu.fetchone()[0]

    cu.execute('''INSERT OR IGNORE INTO Genre (name) VALUES ( ? )''', (genre,))
    cu.execute('SELECT id FROM Genre WHERE name = ? ', (genre,))
    genre_id = cu.fetchone()[0]

    cu.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES ( ?, ?, ?, ?, ?, ? )''', (name, album_id, genre_id, length, rating, count))

conn.commit()

sqlstr = 'SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Genre JOIN Album JOIN Artist ON Track.genre_id = Genre.ID and Track.album_id = Album.id AND Album.artist_id = Artist.id ORDER BY Artist.name, Track.title LIMIT 3'

cu.execute(sqlstr)
table = cu.fetchall()

""" USE 'CREATE TABLE AS' TO SAVE NEW TABLE CREATED BY USING JOIN """

cu.close()