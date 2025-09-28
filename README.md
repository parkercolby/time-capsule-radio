# ⏳ Time Capsule Radio

**Time Capsule Radio** is an AI-powered music app that generates mood-based playlists from your memories. Just describe a memory, select some filters, and get a curated playlist that you can either download as a csv file or open in youtube as a playlist.

---

##Features

- Describe a memory and get a playlist that matches its **mood**
- Uses a transformer-based **zero-shot classifier** (`facebook/bart-large-mnli`)
- Mood-based playlist creation from a **Spotify-style dataset**
- Optional filters:
  - Filter by **artists**
  - Filter by **popularity**
  - Filter out **explicit** songs
- Auto-generates a **YouTube playlist** using [`yt_dlp`](https://github.com/yt-dlp/yt-dlp) (no login required)
- **time machine-themed UI** with glowing side panels
- Download your playlist as a `.txt` file

---

##Project Structure

- app.py #Streamlit frontend app
- main.py #Backend logic and ML pipeline
- dataset.csv/ #Folder containing the dataset.csv file that the songs are curated from
  - dataset.csv
- style.css #Custome styling for side panels and layout
- requirements.txt #Python dependencies

---

##Setup Instructions
