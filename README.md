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

---

## Dependencies and Licenses

This project uses the following open-source libraries:

| Library       | License           | Link                                           |
|---------------|-------------------|------------------------------------------------|
| transformers  | Apache 2.0        | https://github.com/huggingface/transformers/blob/main/LICENSE |
| pandas        | BSD 3-Clause      | https://github.com/pandas-dev/pandas/blob/main/LICENSE |
| yt_dlp        | MIT               | https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE |

Please note that each library is licensed under its own terms. By using this project, you agree to comply with the licenses of these dependencies.

---

You should install these dependencies separately (e.g., via pip) and respect their licenses.

