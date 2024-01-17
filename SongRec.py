#!/usr/bin/env python
# coding: utf-8

# In[17]:


import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import asyncio

# Set up Spotify credentials
client_id = "19777ac6a5924c0aa8bc8526c9c53f47"
client_secret = "cd1fc2f482f046a6a8a8937b1382e5ec"
redirect_uri = "http://localhost:3001"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="playlist-read-private"))

async def get_recommendations(track_name):
    try:
        results = sp.search(q=track_name, type='track')
        track_uri = results['tracks']['items'][0]['uri']
        recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']
        return recommendations
    except Exception as e:
        st.error(f"Error retrieving recommendations: {str(e)}")
        return []

async def get_recommendations_from_playlist(playlist_name):
    try:
        playlists = sp.user_playlists(sp.me()['id'])
        playlist_id = next((playlist['id'] for playlist in playlists['items'] if playlist['name'] == playlist_name), None)

        if playlist_id:
            tracks = sp.playlist_tracks(playlist_id)['items']
            seed_track_uri = tracks[0]['track']['uri']
            recommendations = sp.recommendations(seed_tracks=[seed_track_uri])['tracks']
            return recommendations
        else:
            st.warning("Playlist not found.")
            return []
    except Exception as e:
        st.error(f"Error retrieving playlist recommendations: {str(e)}")
        return []

def main():
    st.title("Music Recommendation System")
    input_type = st.radio("Select input type", ["Song Name", "Playlist"])
    
    if input_type == "Song Name":
        track_name = st.text_input("Enter a song name:")
        input_value = track_name
    else:
        playlist_name = st.text_input("Enter a playlist name:")
        input_value = playlist_name

    if input_value:
        # Explicitly set the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Use the set event loop
        loop = asyncio.get_event_loop()

        # Fetch recommendations based on input type
        if input_type == "Song Name":
            recommendations = loop.run_until_complete(get_recommendations(input_value))
        else:
            recommendations = loop.run_until_complete(get_recommendations_from_playlist(input_value))

        if recommendations:
            st.write("Recommended songs:")
            for track in recommendations:
                st.write(f"{track['name']} - {track['artists'][0]['name']}")
                st.image(track['album']['images'][0]['url'])

if __name__ == '__main__':
    main()






# In[ ]:




