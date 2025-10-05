import streamlit as st
import sqlite3
import os
import pandas as pd
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from rag import rag

# --- Connect to DB ---
from db import get_connection, get_cursor

conn = get_connection()
c = get_cursor()

# --- Sidebar navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["User", "Admin"])

# -----------------------
# User Page
# -----------------------
if page == "User":
    st.title("Norway Tourist Guide")
    st.write("Ask about tourist attractions in Norway")

    query = st.text_input("Ask your question:")

    if st.button("Get Answer"):
        if query.strip() != "":
            with st.spinner("Thinking..."):
                start_time = time.time()
                answer, input_tokens, output_tokens, prompt = rag(query)
                elapsed_time = round(time.time() - start_time, 2)

            # Store in session state
            st.session_state["query"] = query
            st.session_state["answer"] = answer
            st.session_state["elapsed_time"] = elapsed_time

            # Record transaction in DB
            c = conn.cursor()
            c.execute(
                "INSERT INTO monitor (timestamp, query, prompt, answer, feedback, response_time, input_tokens, output_tokens) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (datetime.now(), query, prompt, answer, None, elapsed_time, input_tokens, output_tokens),
            )
            conn.commit()
            st.session_state["last_id"] = c.lastrowid

            # Display result
            st.markdown("### 🧭 Answer")
            st.write(answer)
            
        else:
            st.warning("Please enter a question.")

    # Feedback buttons
    if "answer" in st.session_state:
        st.markdown("---")
        st.markdown("### How was this answer?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Good"):
                c.execute(
                    "UPDATE monitor SET feedback = ? WHERE id = ?",
                    ("Good", st.session_state.get("last_id")),
                )
                conn.commit()
                st.success("Thanks for your feedback!")

        with col2:
            if st.button("👎 Bad"):
                c.execute(
                    "UPDATE monitor SET feedback = ? WHERE id = ?",
                    ("Bad", st.session_state.get("last_id")),
                )
                conn.commit()
                st.success("Thanks for your feedback!")

# -----------------------
# Admin Page
# -----------------------
elif page == "Admin":
    st.title("Admin Dashboard")
    st.write("Overview of recent queries and statistics")

    df = pd.read_sql_query("SELECT * FROM monitor ORDER BY id DESC", conn)
    
    if df.empty:
        st.info("No data in monitor table yet.")
    else:
        # 1️⃣ Last 5 records
        st.subheader("Last 5 records")
        st.dataframe(df.head(5))

        # 2️⃣ Pie chart of feedback
        st.subheader("Feedback Distribution")
        feedback_counts = df['feedback'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(feedback_counts, labels=feedback_counts.index, autopct="%1.1f%%", startangle=90, colors=["#4CAF50","#F44336"])
        ax1.axis('equal')
        st.pyplot(fig1)

        # 3️⃣ Bar plot: average Input/Output tokens
        st.subheader("Average Token Usage")
        avg_input = df['input_tokens'].mean()
        avg_output = df['output_tokens'].mean()
        fig2, ax2 = plt.subplots()
        ax2.bar(["Input Tokens", "Output Tokens"], [avg_input, avg_output], color=["#2196F3","#FFC107"])
        ax2.set_ylabel("Average Tokens")
        st.pyplot(fig2)

        # 4️⃣ Average response time
        st.subheader("Average Response Time")
        avg_response = df['response_time'].mean()
        st.metric("Average Response Time (seconds)", f"{avg_response:.2f}")

        # 5️⃣ Queries in the last 10 minutes (1D scatter)
        st.subheader("Queries in the Last Hour")
        df['timestamp_dt'] = pd.to_datetime(df['timestamp'])

        one_hour_ago = datetime.now() - pd.Timedelta(hours=1)
        df_last_hour = df[df['timestamp_dt'] >= one_hour_ago]

        fig, ax = plt.subplots(figsize=(10, 2))

        # Plot queries as points at y=1
        if not df_last_hour.empty:
            ax.scatter(df_last_hour['timestamp_dt'], [1]*len(df_last_hour), color='blue')

        # Fix x-axis: from now-1h to now
        ax.set_xlim(one_hour_ago, datetime.now())
        ax.set_yticks([])  # hide y-axis
        ax.set_xlabel("Time")
        ax.set_title("Query submissions in the last hour")
        plt.xticks(rotation=45)

        st.pyplot(fig)