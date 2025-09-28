import streamlit as st
from main import generate_playlist, df, get_youtube_id, build_youtube_playlist_link

# Page setup
st.set_page_config(page_title="Time Capsule Radio", page_icon="🎵")

# Load and inject CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Time machine side panels
st.markdown("""
<div class="time-machine-panel left-panel">
    <div class="panel-lights"></div>
    <div class="panel-lights"></div>
    <div class="panel-lights"></div>
</div>
<div class="time-machine-panel right-panel">
    <div class="panel-lights"></div>
    <div class="panel-lights"></div>
    <div class="panel-lights"></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Title and instructions
st.title("⏳ Time Capsule Radio ⏳")
st.markdown("Generate a playlist based on your **memories** and **mood**!")

# User inputs
memory = st.text_input("Describe a memory, moment, or time in your life:")

# Prepare artist options for dropdown - handle multi-artist splits
raw_artists = df['artists'].dropna().unique()
artist_set = set()
for entry in raw_artists:
    if ';' in entry:
        parts = entry.split(';')
    elif ',' in entry:
        parts = entry.split(',')
    else:
        parts = [entry]
    for artist in parts:
        artist_set.add(artist.strip())
artist_options = sorted(artist_set)

selected_artists = st.multiselect("Optional: Filter by one or more artists", artist_options)

length = st.slider("Playlist length", 1, 20, 5)

prefer_popular = st.checkbox("Prefer popular songs?")
min_popularity = None
if prefer_popular:
    min_popularity = st.slider("Minimum popularity (0–100)", min_value=0, max_value=100, value=70)

explicit_allowed = st.checkbox("Include explicit songs?", value=True)

# Generate playlist on button click
if st.button("🎶 Generate Playlist"):
    if not memory:
        st.error("⚠️ Please enter a memory to generate your playlist.")
    else:
        mood, playlist = generate_playlist(
            memory,
            artist_filters=selected_artists,
            playlist_length=length,
            min_popularity=min_popularity,
            explicit_allowed=explicit_allowed
        )

        if mood is None:
            st.error("Sorry, something went wrong while generating your playlist.")
        else:
            st.success(f"🎼 Detected mood: **{mood.capitalize()}**")

            if playlist:
                st.subheader("🎵 Your Playlist:")
                for i, (song, artist_name) in enumerate(playlist, 1):
                    st.markdown(f"{i}. **{song.title()}** by *{artist_name}*")

                # Download playlist as txt
                playlist_text = "\n".join([f"{i}. {s.title()} - {a}" for i, (s, a) in enumerate(playlist, 1)])
                st.download_button(
                    label="Download Playlist as TXT",
                    data=playlist_text,
                    file_name="time_capsule_playlist.txt",
                    mime="text/plain"
                )

                # Build YouTube playlist link
                with st.spinner("Fetching YouTube links..."):
                    video_ids = []
                    for song, artist_name in playlist:
                        query = f"{song} {artist_name}"
                        video_id = get_youtube_id(query)
                        video_ids.append(video_id)

                yt_playlist_link = build_youtube_playlist_link(video_ids)
                if yt_playlist_link:
                    st.markdown(f"###  [Open YouTube Playlist]({yt_playlist_link})", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Couldn't build a YouTube playlist link.")
            else:
                st.warning("⚠️ No songs found for that mood and artist combination.")

st.markdown("---")
st.markdown('</div>', unsafe_allow_html=True)
