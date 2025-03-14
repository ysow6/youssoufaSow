import streamlit as st
import pandas as pd
import plotly.express as px
import json


st.set_page_config(page_title="Performance Tracker", page_icon="🏃‍♂️")

st.title("Performance Tracker Dashboard")
st.subheader("Tracking Sleep, Workouts, and 400m Dash Progress")


data_file = "data.json"

def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "sleep": {"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "hours": [6, 7, 5, 8, 9, 6, 7]},
            "track times": {"age": [12, 13, 14, 15, 16, 17, 18], "time": [62.85, 57.32, 55.00, 53.55, 51.45, 50.9, 50.11]},
            "workouts": {"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "hours": [1, 1.5, 1.2, 1.8, 2, 0.5, 1.5]}
        }

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()


st.markdown("### 🛌 Weekly Sleep Tracker")
sleep_data = pd.DataFrame(data["sleep"])

if "selected_day" not in st.session_state:
    st.session_state.selected_day = sleep_data["day"][0]  

sleep_day = st.selectbox("Select a day:", sleep_data["day"], key="selected_day")
sleep_hours = st.slider("Enter sleep hours:", min_value=0.0, max_value=12.0, step=0.1, key="sleep_input")  # NEW

if st.button("Update Sleep"):
    index = sleep_data["day"].tolist().index(sleep_day)
    data["sleep"]["hours"][index] = sleep_hours
    save_data(data)
    st.success(f"Updated {sleep_day} to {sleep_hours} hours!")
    st.rerun()

fig1 = px.line(sleep_data, x="day", y="hours", title="Sleep Hours Throughout the Week", markers=True, labels={"hours": "Hours"})
st.plotly_chart(fig1)
st.write("This chart allows you to track how many hours you sleep each night. Updating the data helps visualize patterns in your sleep schedule.")


st.markdown("### 🏋️ Weekly Workouts")
workout_data = pd.DataFrame(data["workouts"])

st.markdown("#### Update Your Workout Hours")
day_selected = st.selectbox("Select a day for workouts:", workout_data["day"], key="workout_day")
hours_new = st.number_input("Enter workout hours:", min_value=0.0, max_value=5.0, step=0.1, key="workout_hours")

if st.button("Update Workout"):
    index = workout_data["day"].tolist().index(day_selected)
    data["workouts"]["hours"][index] = hours_new
    save_data(data)
    st.success(f"Updated {day_selected} to {hours_new} hours!")
    st.rerun()


st.markdown("#### Select Workout Intensity")  
intensity = st.radio("Choose intensity:", ["Light", "Moderate", "Intense"], key="workout_intensity")  # NEW

fig2 = px.bar(workout_data, x="day", y="hours", title="Workout Hours per Day", labels={"hours": "Hours"})
st.plotly_chart(fig2)
st.write("This bar chart tracks workout hours throughout the week. Updating the data allows for real-time visualization of training consistency.")


st.markdown("### 📄 Upload Your Workout Plan (Optional)")
uploaded_file = st.file_uploader("Upload a PDF or text file with your workout plan:", type=["pdf", "txt"])  # NEW

if uploaded_file:
    st.success("File uploaded successfully!")
    st.write("You can reference this plan while tracking your workouts.")


st.markdown("### 🏃‍♂️ 400m Dash Progress")
track_data = pd.DataFrame(data["track times"])

fig3 = px.line(track_data, x="age", y="time", markers=True,
               title="400m Dash Performance (Age 12-18)",
               labels={"age": "Age", "time": "Time (Seconds)"})
st.plotly_chart(fig3)
st.write("This chart tracks 400m dash times from ages 12 to 18. The downward trend suggests improved speed over time.")

st.markdown("---")
st.info("This dashboard can track your academic and athletic performance and includes my own personal data about my track times in the 400m Dash.")
