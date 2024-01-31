#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio

# Set up Spotify credentials
client_id = "19777ac6a5924c0aa8bc8526c9c53f47" 
client_secret = "cd1fc2f482f046a6a8a8937b1382e5ec"
redirect_uri = "http://localhost:3001"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

async def get_recommendations(track_names):
    track_uris = []
    
    # Get track URIs for each track name
    for track_name in track_names:
        results = sp.search(q=track_name, type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)

    # Get recommended tracks
    if track_uris:
        recommendations = sp.recommendations(seed_tracks=track_uris)['tracks']
        return recommendations
    else:
        return []

def main():
    st.title("Music Recommendation System")
    track_names = st.text_input("Enter song names separated by commas (include artist for best result):")

    if track_names:
        track_names_list = [name.strip() for name in track_names.split(',')]
        
        # Explicitly set the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Use the set event loop
        loop = asyncio.get_event_loop()

        # Fetch recommendations based on input type
        recommendations = loop.run_until_complete(get_recommendations(track_names_list))

        st.write("Recommended songs:")
        for i, track in enumerate(recommendations):
            st.write(f"{i + 1}. {track['name']} - {track['artists'][0]['name']}")
            st.image(track['album']['images'][0]['url'])

if __name__ == '__main__':
    main()

