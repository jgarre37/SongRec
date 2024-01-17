#!/usr/bin/env python
# coding: utf-8

# In[17]:


import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio

# Set up Spotify credentials
client_id = "19777ac6a5924c0aa8bc8526c9c53f47"
client_secret = "cd1fc2f482f046a6a8a8937b1382e5ec"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

async def get_recommendations(track_name):
    # Your implementation for getting recommendations
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']
    recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']
    return recommendations

def main():
    st.title("Music Recommendation System")
    track_name = st.text_input("Enter a song name:")

    if track_name:
        # Explicitly set the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Use the set event loop
        loop = asyncio.get_event_loop()
        recommendations = loop.run_until_complete(get_recommendations(track_name))

        st.write("Recommended songs:")
        for track in recommendations:
            st.write(f"{track['name']} - {track['artists'][0]['name']}")
            st.image(track['album']['images'][0]['url'])

if __name__ == '__main__':
    main()







# In[ ]:




