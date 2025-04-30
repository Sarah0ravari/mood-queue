import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import plotly.express as px

# 🔐 Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 📄 Open the correct sheet by key
sheet = client.open_by_key("19ZXAG6iRFdKi9XHnoySLZqWUDpZhKnviFrsi1I8PcRo").sheet1

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
