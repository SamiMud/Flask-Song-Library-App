from app import app, db


class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50), index = True, unique = True) 
  playlist_id = db.Column(db.Integer,  db.ForeignKey('playlist.id'))
  
  def __repr__(self):
        return "{}".format(self.username)

class Song(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  artist = db.Column(db.String(80), index = True, unique = False)
  title = db.Column(db.String(50), index = True, unique = False)
  n = db.Column(db.Integer, index = False, unique = False)

  def __repr__(self):
    return "{} by {}".format(self.title, self.artist)


class Item(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
  playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))


class Playlist(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  items = db.relationship('Item', backref='playlist', lazy='dynamic')
