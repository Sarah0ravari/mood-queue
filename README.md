# 🎯 Mood-Queue

This is a lightweight internal tool for logging and visualizing the emotional "vibe" of support tickets throughout the day. Built using **Streamlit**, **Google Sheets**, and **Plotly**, the app enables support agents to track moods in real time and see trends over time.

---

## 🛠 Features

- Log moods with emoji selections (😊 😠 😕 🎉)
- Optionally add a note with each entry
- Store entries in a Google Sheet (timestamp, mood, note)
- Visualize today's mood trends with a bar chart

---

## 💻 Tech Stack

- **Frontend/UI:** Streamlit  
- **Backend Storage:** Google Sheets API (`gspread`)  
- **Charts:** Plotly  
- **Auth:** Google Service Account (`credentials.json`)

---

## 🚀 Setup & Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/mood-queue.git
   cd mood-queue
