import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
import os

# =====================================
# MAIN FUNCTION (IMPORTANT FIX ✅)
# =====================================
def run():

    # =====================================
    # CONFIG (MUST BE FIRST)
    # =====================================

    # =====================================
    # LOAD ENV
    # =====================================
    load_dotenv()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    st.title("🎓 AI Student Performance Analytics Dashboard")

    # =====================================
    # AI FUNCTION
    # =====================================
    def ask_ai(student_df, question):

        context = student_df.to_json(orient="records", indent=2)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an Academic Performance Analyst.

Rules:
- Use ONLY given data
- No guessing
- Keep answers short

Definitions:
- Failed Subject = Total < 30
- Weak = Lowest Total
- Strong = Highest Total
"""
                },
                {
                    "role": "user",
                    "content": f"""
Student Data:
{context}

Question:
{question}
"""
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    # =====================================
    # FILE UPLOAD
    # =====================================
    uploaded_file = st.file_uploader(
        "📂 Upload Student Marksheet",
        type=["xlsx"]
    )

    # =====================================
    # MAIN APP
    # =====================================
    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file)

        st.subheader("📋 Uploaded Student Data")
        st.dataframe(df, use_container_width=True)

        # =====================================
        # STATS
        # =====================================
        st.subheader("📊 Overall Statistics")

        col1, col2 = st.columns(2)

        col1.metric("👨‍🎓 Total Students", df["StudentID"].nunique())
        col2.metric("📈 Average Marks", round(df["Total"].mean(), 2))

        # =====================================
        # SUBJECT GRAPH
        # =====================================
        st.subheader("📚 Subject-wise Analysis")

        subject_avg = df.groupby("Subject")["Total"].mean().reset_index()

        fig = px.bar(
            subject_avg,
            x="Subject",
            y="Total",
            text_auto=True,
            title="Average Marks by Subject"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =====================================
        # STUDENT ANALYSIS
        # =====================================
        st.subheader("👨‍🎓 Student Analysis")

        student = st.selectbox("Select Student", df["Name"].unique())
        student_df = df[df["Name"] == student]

        st.dataframe(student_df, use_container_width=True)

        # =====================================
        # STRONG & WEAK
        # =====================================
        avg = student_df.groupby("Subject")["Total"].mean()

        weak_subject = avg.idxmin()
        strong_subject = avg.idxmax()

        col3, col4 = st.columns(2)
        col3.error(f"📉 Weak Subject: {weak_subject}")
        col4.success(f"🏆 Strong Subject: {strong_subject}")

        # =====================================
        # UNIT GRAPH
        # =====================================
        st.subheader("📖 Unit-wise Performance")

        fig2 = px.bar(
            student_df,
            x="Subject",
            y=["Unit1", "Unit2", "Unit3"],
            barmode="group",
            title=f"{student} Unit-wise Marks"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # =====================================
        # LEARNING GAP
        # =====================================
        st.subheader("🎯 Learning Gap Analysis")

        weak_row = student_df.loc[student_df["Total"].idxmin()]

        st.warning(f"⚠️ Weakest Subject: {weak_row['Subject']}")

        units = {
            "Unit1": weak_row["Unit1"],
            "Unit2": weak_row["Unit2"],
            "Unit3": weak_row["Unit3"]
        }

        weak_unit = min(units, key=units.get)
        st.error(f"📉 Weakest Unit: {weak_unit}")

        # =====================================
        # FAILED SUBJECTS
        # =====================================
        st.subheader("🚨 Subjects Requiring Attention")

        failed_subjects = student_df[student_df["Total"] < 30]

        if not failed_subjects.empty:
            st.error(f"❌ Failed in {len(failed_subjects)} subject(s)")
            st.dataframe(
                failed_subjects[["Subject", "Unit1", "Unit2", "Unit3", "Total"]],
                use_container_width=True
            )
        else:
            st.success("✅ Passed all subjects")

        # =====================================
        # AI ASSISTANT
        # =====================================
        st.subheader("🤖 AI Academic Assistant")

        question = st.text_input("💬 Ask question")

        if st.button("🚀 Ask AI"):

            if question.strip():

                q = question.lower()

                if "fail" in q:
                    failed = student_df[student_df["Total"] < 30]
                    answer = "No failed subjects" if failed.empty else ", ".join(failed["Subject"])

                elif "weak" in q:
                    answer = student_df.loc[student_df["Total"].idxmin(), "Subject"]

                elif "strong" in q or "best" in q:
                    answer = student_df.loc[student_df["Total"].idxmax(), "Subject"]

                else:
                    answer = ask_ai(student_df, question)

                st.success("🤖 AI Response")
                st.write(answer)

            else:
                st.warning("Enter a question")

    else:
        st.info("📂 Upload file to start")