from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import app, db
from models import User, Song, Playlist, Item
from flask import render_template, request, url_for, redirect, flash

#A form for inputing new songs via Dashboard
class SongForm(FlaskForm):
  title = StringField(label = "Song Title:", validators=[DataRequired()])
  artist = StringField(label = "Artist:", validators=[DataRequired()])
  submit = SubmitField("Add Song")

#A function we made to check if an item to be added is already in the playlist
def exists(item, playlist):
  """Return a boolean
    True if playlist contains item. False otherwise.
    """
  for i in playlist: #for each item in playlist
    if i.song_id == item.song_id: #check if the primary key is equal
       return True
  return False

#The home page of FlaskFM
#Lists all the users currently in the database
#renders the home.html template providing the list of current users
@app.route('/profiles')
def profiles():
    current_users = User.query.all()
    return render_template('users.html', current_users = current_users)

#Displays profile pages for a user with the user_id primary key
#renders the profile.html template for a specific user, song library and 
#the user's playlist 
@app.route('/profile/<int:user_id>')
def profile(user_id):
   user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
   songs = Song.query.all()
   my_playlist = Playlist.query.get(user.playlist_id)
   return render_template('profile.html', user = user, songs = songs, my_playlist = my_playlist)

#Adds new songs to a user's playlist from the song library
#redirects back to the profile that issued the addition
@app.route('/add_item/<int:user_id>/<int:song_id>/<int:playlist_id>')
def add_item(user_id, song_id, playlist_id):
   new_item = Item(song_id = song_id, playlist_id = playlist_id)
   user = User.query.filter_by(id = user_id).first_or_404(description = "No such user found.")
   my_playlist = Playlist.query.filter_by(id = user.playlist_id).first()
   if not exists(new_item, my_playlist.items):
      song = Song.query.get(song_id)
      db.session.add(new_item)
      song.n = song.n + 1
      db.session.commit()
   return redirect(url_for('profile', user_id = user_id))


@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):

   db.session.delete(Item.query.get(item_id))
   db.session.commit()

   return redirect(url_for('profile', user_id = user_id))
   
#Display the Dashboard page with a form for adding songs
#Renders the dashboard template
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
  form = SongForm()
  if request.method == 'POST' and form.validate():
    new_song = Song(title= form.title, artist = form.artist, n = 1)
    db.session.add(new_song)
    db.session.commit()
  else:
        flash(form.errors)
  unpopular_songs = Song.query.order_by(Song.n)
  songs = Song.query.all()
  return render_template('dashboard.html', songs = songs, unpopular_songs = unpopular_songs, form = form)