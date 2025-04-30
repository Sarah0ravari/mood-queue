import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px

# Authenticate and connect to Google Sheets
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", 
             "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)  
    return spreadsheet.worksheet(sheet_name)  # Access specific sheet by name

# Google Sheet credentials and details
SPREADSHEET_NAME = 'MoodLog'
SHEET_NAME = 'Sheet1'
CREDENTIALS_FILE = './credentials.json'

# Connect to the Google Sheet
sheet = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, SHEET_NAME)

# 🌟 Streamlit UI
st.title("🎯 Mood of the Queue")

mood = st.selectbox("Select your mood", ["😊", "😠", "😕", "🎉"])
note = st.text_input("Optional note")

if st.button("Log Mood"):
    try:
        sheet.append_row([datetime.now().isoformat(), mood, note])
        st.success("Mood logged!")
    except Exception as e:
        st.error(f"Failed to log mood: {e}")

# 📊 Fetch and visualize today's mood data
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and 'timestamp' in df.columns:
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])  # remove rows with bad timestamps
            today_df = df[df['timestamp'].dt.date == datetime.today().date()]

            if not today_df.empty:
                mood_counts = today_df['mood'].value_counts().reset_index()
                mood_counts.columns = ['Mood', 'Count']
                fig = px.bar(mood_counts, x='Mood', y='Count', title="Today's Mood Trend")
                st.plotly_chart(fig)
            else:
                st.info("No moods logged yet today.")
        except Exception as e:
            st.error(f"Error processing timestamps: {e}")
    else:
        st.info("Waiting for first mood log...")
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")
