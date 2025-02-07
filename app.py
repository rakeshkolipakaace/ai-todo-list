
# #perfect code

# import streamlit as st
# import pandas as pd
# import joblib
# import spacy
# import random
# from datetime import datetime, timedelta

# # Load NLP model
# nlp = spacy.load("en_core_web_sm")

# # Load ML Model (Check if the model exists)
# try:
#     completion_model = joblib.load("models/task_completion_model.pkl")
# except FileNotFoundError:
#     completion_model = None
#     st.error("⚠️ ML Model not found! Please train it first by running 'train_completion_model.py'.")

# # Initialize session state for tasks & AI-generated tasks
# if 'tasks' not in st.session_state:
#     st.session_state.tasks = pd.DataFrame(columns=['Task', 'Deadline', 'Urgency', 'Days Left', 'Priority'])

# if 'ai_tasks' not in st.session_state:
#     st.session_state.ai_tasks = pd.DataFrame(columns=['Task', 'Suggested Deadline'])

# # NLP Function for Task Analysis
# def analyze_task(task):
#     """Uses NLP to detect urgency in task descriptions."""
#     doc = nlp(task.lower())
#     urgency_score = sum(1 for token in doc if token.text in ["urgent", "asap", "critical", "important", "deadline"])
#     return urgency_score

# # AI-Based Deadline Suggestion (Randomized)
# def suggest_deadline(task):
#     """Assigns a random deadline based on urgency keywords and displays days left."""
#     task = task.lower()
#     days_range = (7, 14)  # Default range

#     if "urgent" in task or "asap" in task:
#         days_range = (1, 3)
#     elif "important" in task:
#         days_range = (3, 7)
#     elif "meeting" in task or "submission" in task:
#         days_range = (5, 10)
    
#     random_days = random.randint(*days_range)
#     suggested_date = datetime.today() + timedelta(days=random_days)
    
#     return f"Complete by {suggested_date.strftime('%Y-%m-%d')} (in {random_days} days)"

# # ML Prediction for Task Completion Time
# def predict_completion_time(urgency, days_left):
#     """Predicts how long a task will take to complete."""
#     if completion_model is None:
#         return "⚠️ Model not available"
    
#     input_data = pd.DataFrame([[urgency, days_left]], columns=["urgency", "days_left"])
#     prediction = completion_model.predict(input_data)[0]
    
#     return round(prediction * 2) / 2  # 🔥 Now it rounds to the nearest 0.5 day

# # Streamlit UI Configuration
# st.set_page_config(page_title="AI To-Do List", layout="wide")
# st.title("🚀 AI-Powered Priority To-Do List 📝")
# st.markdown("**Tasks are automatically prioritized based on urgency keywords and deadlines**")

# # 📌 **Priority Legend**
# st.subheader("📌 Priority Legend")
# col1, col2, col3 = st.columns(3)
# with col1: st.markdown("🔥 **Critical (80+ points)**")
# with col2: st.markdown("⚠️ **High (50-79 points)**")
# with col3: st.markdown("✅ **Normal (0-49 points)**")

# # Sidebar: Add New Task
# st.sidebar.header("➕ Add New Task")
# task = st.sidebar.text_input("Task Description")
# deadline = st.sidebar.date_input("Deadline (Optional)")

# if st.sidebar.button("Add Task"):
#     if task:
#         urgency = analyze_task(task)
#         days_left = (deadline - datetime.today().date()).days if deadline else 999
#         priority = min(100, (urgency * 10) + max(0, 100 - days_left))  # ✅ Fixed priority calculation

#         new_task = pd.DataFrame([{
#             'Task': task,
#             'Deadline': deadline.strftime("%Y-%m-%d") if deadline else "None",
#             'Urgency': urgency,
#             'Days Left': days_left if deadline else "N/A",
#             'Priority': priority
#         }])

#         st.session_state.tasks = pd.concat([st.session_state.tasks, new_task], ignore_index=True)
#         st.rerun()  # 🔥 Ensures the UI refreshes after adding a task

#     else:
#         st.warning("⚠️ Please enter a task description")

# # AI Deadline Assistant
# st.sidebar.subheader("🤖 AI Deadline Assistant")
# task_input = st.sidebar.text_input("Enter Task for Deadline Suggestion")
# suggested_deadline = None  # Initialize variable

# if st.sidebar.button("Suggest Deadline"):
#     if task_input:
#         suggested_deadline = suggest_deadline(task_input)
        
#         # Store AI Task in Session State
#         ai_task = pd.DataFrame([{'Task': task_input, 'Suggested Deadline': suggested_deadline}])
#         st.session_state.ai_tasks = pd.concat([st.session_state.ai_tasks, ai_task], ignore_index=True)
        
#         st.sidebar.success(f"✅ Suggested Deadline: {suggested_deadline}")
#         st.rerun()  # 🔥 Refresh UI so AI tasks show instantly
#     else:
#         st.sidebar.warning("⚠️ Enter a task first.")

# # Display Both Sections in Two Columns
# col1, col2 = st.columns(2)

# # Left Side: Your Prioritized Tasks
# with col1:
#     if not st.session_state.tasks.empty:
#         sorted_tasks = st.session_state.tasks.sort_values('Priority', ascending=False)
#         st.subheader("📌 Your Prioritized Tasks")
        
#         for _, row in sorted_tasks.iterrows():
#             priority_label = "🔥" if row['Priority'] >= 80 else "⚠️" if row['Priority'] >= 50 else "✅"
            
#             # Display tasks in a larger format
#             st.markdown(f"""
#             <div style='padding:15px; margin:10px; border-radius:5px; font-size:22px;
#                         border-left: 7px solid {"#ff4b4b" if priority_label == "🔥" else "#f0ad4e" if priority_label == "⚠️" else "#5ee584"}'>
#                 <b>{priority_label} {row['Task']}</b> <br>
#                 <span style="color:gray">Deadline: {row['Deadline']} | Priority Score: {row['Priority']}</span>
#             </div>
#             """, unsafe_allow_html=True)

# # Right Side: AI Deadline Assistant Tasks
# with col2:
#     if not st.session_state.ai_tasks.empty:
#         st.subheader("🤖 AI Deadline Assistant Tasks")
#         for _, row in st.session_state.ai_tasks.iterrows():
#             st.markdown(f"""
#             <div style='padding:15px; margin:10px; border-radius:5px; font-size:22px;
#                         border-left: 7px solid #3498db;'>
#                 📌 <b>{row['Task']}</b> <br>
#                 <span style="color:gray">{row['Suggested Deadline']}</span>
#             </div>
#             """, unsafe_allow_html=True)

# # Predict Completion Time
# st.sidebar.subheader("⏳ AI Task Completion Predictor")
# urgency_input = st.sidebar.slider("Urgency (0-3)", 0, 3, 1)
# days_left_input = st.sidebar.number_input("Days Left", min_value=1)

# if st.sidebar.button("Predict Completion Time"):
#     prediction = predict_completion_time(urgency_input, days_left_input)
#     st.sidebar.success(f"⏳ Estimated Completion Time: {prediction} days")

# # Export Tasks (Fixed Date Format Issue)
# if not st.session_state.tasks.empty or not st.session_state.ai_tasks.empty:
#     csv_data = st.session_state.tasks.copy()
#     csv_data["Deadline"] = pd.to_datetime(csv_data["Deadline"], errors="coerce").dt.strftime("%Y-%m-%d")

#     ai_csv_data = st.session_state.ai_tasks.copy()

#     with st.sidebar:
#         st.download_button("📥 Download User Tasks", csv_data.to_csv(index=False).encode("utf-8"), "user_tasks.csv", "text/csv")
#         st.download_button("📥 Download AI Suggested Tasks", ai_csv_data.to_csv(index=False).encode("utf-8"), "ai_tasks.csv", "text/csv")




# import streamlit as st
# import pandas as pd
# import joblib
# import spacy
# import sqlite3
# import random
# from datetime import datetime, timedelta

# # Load NLP model
# nlp = spacy.load("en_core_web_sm")

# # Load ML Model
# try:
#     completion_model = joblib.load("models/task_completion_model.pkl")
# except FileNotFoundError:
#     completion_model = None

# # Initialize SQLite Database
# conn = sqlite3.connect("tasks.db", check_same_thread=False)
# c = conn.cursor()

# # Create Tables
# c.execute("""
# CREATE TABLE IF NOT EXISTS tasks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     task TEXT,
#     deadline TEXT,
#     urgency INTEGER,
#     days_left INTEGER,
#     priority INTEGER
# )
# """)

# c.execute("""
# CREATE TABLE IF NOT EXISTS ai_tasks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     task TEXT,
#     suggested_deadline TEXT
# )
# """)

# conn.commit()

# # Function to Analyze Task Urgency
# def analyze_task(task):
#     doc = nlp(task.lower())
#     urgency_score = sum(1 for token in doc if token.text in ["urgent", "asap", "critical", "important", "deadline"])
#     return urgency_score

# # Function to Suggest AI Deadline
# def suggest_deadline(task):
#     task = task.lower()
#     days_range = (7, 14)
#     if "urgent" in task or "asap" in task:
#         days_range = (1, 3)
#     elif "important" in task:
#         days_range = (3, 7)
#     elif "meeting" in task or "submission" in task:
#         days_range = (5, 10)
    
#     random_days = random.randint(*days_range)
#     suggested_date = datetime.today() + timedelta(days=random_days)
#     return f"Complete by {suggested_date.strftime('%Y-%m-%d')} (in {random_days} days)"

# # **✅ FIXED: Function to Predict Completion Time**
# def predict_completion_time(urgency, days_left):
#     if completion_model is None:
#         return "⚠️ Model Not Available"
    
#     input_data = pd.DataFrame([[urgency, days_left]], columns=["urgency", "days_left"])
#     prediction = completion_model.predict(input_data)[0]

#     # ✅ Round to nearest 0.5 or whole number (e.g., 1, 1.5, 2, 2.5)
#     adjusted_prediction = max(1, round(prediction * 2) / 2)  # Rounds to the nearest 0.5

#     return adjusted_prediction

# # Streamlit UI Setup
# st.set_page_config(page_title="AI To-Do List", layout="wide")
# st.title("🚀 AI-Powered Priority To-Do List 📝")
# st.markdown("**Tasks are automatically prioritized based on urgency keywords and deadlines.**")

# # 📌 Priority Legend (Better Formatting)
# st.subheader("📌 Priority Legend")
# st.markdown("""
# - 🔥 **Critical (80+ points)**  
# - ⚠️ **High (50-79 points)**  
# - ✅ **Normal (0-49 points)**
# """)

# # Sidebar: Add New Task
# st.sidebar.header("➕ Add New Task")
# task = st.sidebar.text_input("Task Description")
# deadline = st.sidebar.date_input("Deadline (Optional)")

# if st.sidebar.button("Add Task"):
#     if task:
#         urgency = analyze_task(task)
#         days_left = (deadline - datetime.today().date()).days if deadline else 999
#         priority = min(100, (urgency * 10) + max(0, 100 - days_left))

#         c.execute("INSERT INTO tasks (task, deadline, urgency, days_left, priority) VALUES (?, ?, ?, ?, ?)",
#                   (task, deadline.strftime("%Y-%m-%d") if deadline else "None", urgency, days_left, priority))
#         conn.commit()
        
#         st.success("✅ Task Added Successfully!")
#         st.rerun()
#     else:
#         st.warning("⚠️ Please enter a task description")

# # Sidebar: AI Deadline Assistant
# st.sidebar.subheader("🤖 AI Deadline Assistant")
# task_input = st.sidebar.text_input("Enter Task for AI Deadline")

# if st.sidebar.button("Suggest Deadline"):
#     if task_input:
#         suggested_deadline = suggest_deadline(task_input)
#         c.execute("INSERT INTO ai_tasks (task, suggested_deadline) VALUES (?, ?)", (task_input, suggested_deadline))
#         conn.commit()

#         st.sidebar.success(f"✅ Suggested Deadline: {suggested_deadline}")
#         st.rerun()
#     else:
#         st.sidebar.warning("⚠️ Enter a task first.")

# # **✅ FIXED: AI Task Completion Predictor**
# st.sidebar.subheader("⏳ AI Task Completion Predictor")
# urgency_input = st.sidebar.slider("Urgency (0-3)", 0, 3, 1)
# days_left_input = st.sidebar.number_input("Days Left", min_value=1)

# if st.sidebar.button("Predict Completion Time"):
#     prediction = predict_completion_time(urgency_input, days_left_input)
#     st.sidebar.success(f"⏳ Estimated Completion Time: {prediction} days")

# # **✅ Two-Column Layout**
# col1, col2 = st.columns(2)

# # **Left Column: Your Prioritized Tasks**
# with col1:
#     st.subheader("📌 Your Prioritized Tasks")
    
#     df_tasks = pd.read_sql("SELECT * FROM tasks ORDER BY priority DESC", conn)
#     if not df_tasks.empty:
#         for _, row in df_tasks.iterrows():
#             priority_label = "🔥" if row["priority"] >= 80 else "⚠️" if row["priority"] >= 50 else "✅"
#             st.markdown(f"""
#             <div style='padding:15px; margin:10px; border-radius:5px; font-size:18px;
#                         border-left: 7px solid {"#ff4b4b" if priority_label == "🔥" else "#f0ad4e" if priority_label == "⚠️" else "#5ee584"}'>
#                 <b>{priority_label} {row['task']}</b> <br>
#                 Deadline: {row['deadline']} | Priority Score: {row['priority']}
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No tasks added yet!")

# # **Right Column: AI Deadline Assistant Tasks**
# with col2:
#     st.subheader("🤖 AI Deadline Assistant Tasks")

#     df_ai_tasks = pd.read_sql("SELECT * FROM ai_tasks", conn)
#     if not df_ai_tasks.empty:
#         for _, row in df_ai_tasks.iterrows():
#             st.markdown(f"""
#             <div style='padding:15px; margin:10px; border-radius:5px; font-size:18px;
#                         border-left: 7px solid #3498db;'>
#                 📌 <b>{row['task']}</b> <br>
#                 {row['suggested_deadline']}
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No AI tasks added yet!")

# # **✅ Fixed: Sidebar Download Buttons**
# st.sidebar.subheader("📥 Download Your Tasks")

# if not df_tasks.empty:
#     user_csv = df_tasks.to_csv(index=False).encode("utf-8")
#     st.sidebar.download_button(
#         label="📂 Download User Tasks",
#         data=user_csv,
#         file_name="user_tasks.csv",
#         mime="text/csv"
#     )

# if not df_ai_tasks.empty:
#     ai_csv = df_ai_tasks.to_csv(index=False).encode("utf-8")
#     st.sidebar.download_button(
#         label="📂 Download AI Tasks",
#         data=ai_csv,
#         file_name="ai_tasks.csv",
#         mime="text/csv"
#     )



# deploy code

import streamlit as st
import pandas as pd
import joblib
import spacy
import sqlite3
import random
from datetime import datetime, timedelta

# ✅ Move set_page_config to the first line!
st.set_page_config(page_title="AI To-Do List", layout="wide")

# ✅ Load NLP model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("⚠️ spaCy model not found! Using a basic NLP model instead.")
    nlp = spacy.blank("en")  # Loads a minimal NLP pipeline

# ✅ Load ML Model
try:
    completion_model = joblib.load("models/task_completion_model.pkl")
except FileNotFoundError:
    completion_model = None

# ✅ Initialize SQLite Database
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

# ✅ Create Tables if they don’t exist
c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    deadline TEXT,
    urgency INTEGER,
    days_left INTEGER,
    priority INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS ai_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    suggested_deadline TEXT
)
""")

conn.commit()

# ✅ Function to Analyze Task Urgency
def analyze_task(task):
    doc = nlp(task.lower())
    urgency_score = sum(1 for token in doc if token.text in ["urgent", "asap", "critical", "important", "deadline"])
    return urgency_score

# ✅ Function to Suggest AI Deadline
def suggest_deadline(task):
    task = task.lower()
    days_range = (7, 14)
    if "urgent" in task or "asap" in task:
        days_range = (1, 3)
    elif "important" in task:
        days_range = (3, 7)
    elif "meeting" in task or "submission" in task:
        days_range = (5, 10)
    
    random_days = random.randint(*days_range)
    suggested_date = datetime.today() + timedelta(days=random_days)
    return f"Complete by {suggested_date.strftime('%Y-%m-%d')} (in {random_days} days)"

# ✅ Function to Predict Completion Time
def predict_completion_time(urgency, days_left):
    if completion_model is None:
        return "⚠️ Model Not Available"
    
    input_data = pd.DataFrame([[urgency, days_left]], columns=["urgency", "days_left"])
    prediction = completion_model.predict(input_data)[0]

    # ✅ Round to nearest 0.5 or whole number
    adjusted_prediction = max(1, round(prediction * 2) / 2)

    return adjusted_prediction

# ✅ Streamlit UI Setup
st.title("🚀 AI-Powered Priority To-Do List 📝")
st.markdown("**Tasks are automatically prioritized based on urgency keywords and deadlines.**")

# ✅ Priority Legend
st.subheader("📌 Priority Legend")
st.markdown("""
- 🔥 **Critical (80+ points)**  
- ⚠️ **High (50-79 points)**  
- ✅ **Normal (0-49 points)**
""")

# ✅ Sidebar: Add New Task
st.sidebar.header("➕ Add New Task")
task = st.sidebar.text_input("Task Description")
deadline = st.sidebar.date_input("Deadline (Optional)")

if st.sidebar.button("Add Task"):
    if task:
        urgency = analyze_task(task)
        days_left = (deadline - datetime.today().date()).days if deadline else 999
        priority = min(100, (urgency * 10) + max(0, 100 - days_left))

        c.execute("INSERT INTO tasks (task, deadline, urgency, days_left, priority) VALUES (?, ?, ?, ?, ?)",
                  (task, deadline.strftime("%Y-%m-%d") if deadline else "None", urgency, days_left, priority))
        conn.commit()
        
        st.success("✅ Task Added Successfully!")
        st.rerun()
    else:
        st.warning("⚠️ Please enter a task description")

# ✅ Sidebar: AI Deadline Assistant
st.sidebar.subheader("🤖 AI Deadline Assistant")
task_input = st.sidebar.text_input("Enter Task for AI Deadline")

if st.sidebar.button("Suggest Deadline"):
    if task_input:
        suggested_deadline = suggest_deadline(task_input)
        c.execute("INSERT INTO ai_tasks (task, suggested_deadline) VALUES (?, ?)", (task_input, suggested_deadline))
        conn.commit()

        st.sidebar.success(f"✅ Suggested Deadline: {suggested_deadline}")
        st.rerun()
    else:
        st.sidebar.warning("⚠️ Enter a task first.")

# ✅ Sidebar: AI Task Completion Predictor
st.sidebar.subheader("⏳ AI Task Completion Predictor")
urgency_input = st.sidebar.slider("Urgency (0-3)", 0, 3, 1)
days_left_input = st.sidebar.number_input("Days Left", min_value=1)

if st.sidebar.button("Predict Completion Time"):
    prediction = predict_completion_time(urgency_input, days_left_input)
    st.sidebar.success(f"⏳ Estimated Completion Time: {prediction} days")

# ✅ Two-Column Layout
col1, col2 = st.columns(2)

# ✅ Left Column: User Prioritized Tasks
with col1:
    st.subheader("📌 Your Prioritized Tasks")
    
    df_tasks = pd.read_sql("SELECT * FROM tasks ORDER BY priority DESC", conn)
    if not df_tasks.empty:
        for _, row in df_tasks.iterrows():
            priority_label = "🔥" if row["priority"] >= 80 else "⚠️" if row["priority"] >= 50 else "✅"
            st.markdown(f"""
            <div style='padding:15px; margin:10px; border-radius:5px; font-size:18px;
                        border-left: 7px solid {"#ff4b4b" if priority_label == "🔥" else "#f0ad4e" if priority_label == "⚠️" else "#5ee584"}'>
                <b>{priority_label} {row['task']}</b> <br>
                Deadline: {row['deadline']} | Priority Score: {row['priority']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks added yet!")

# ✅ Right Column: AI Deadline Assistant Tasks
with col2:
    st.subheader("🤖 AI Deadline Assistant Tasks")

    df_ai_tasks = pd.read_sql("SELECT * FROM ai_tasks", conn)
    if not df_ai_tasks.empty:
        for _, row in df_ai_tasks.iterrows():
            st.markdown(f"""
            <div style='padding:15px; margin:10px; border-radius:5px; font-size:18px;
                        border-left: 7px solid #3498db;'>
                📌 <b>{row['task']}</b> <br>
                {row['suggested_deadline']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No AI tasks added yet!")

# ✅ Sidebar: Download Buttons
st.sidebar.subheader("📥 Download Your Tasks")

if not df_tasks.empty:
    user_csv = df_tasks.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("📂 Download User Tasks", user_csv, "user_tasks.csv", "text/csv")

if not df_ai_tasks.empty:
    ai_csv = df_ai_tasks.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("📂 Download AI Tasks", ai_csv, "ai_tasks.csv", "text/csv")
