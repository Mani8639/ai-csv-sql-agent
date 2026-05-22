import streamlit as st
from langchain_ollama import OllamaLLM
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("AI CSV SQL Agent")

# -----------------------------------
# LOAD LOCAL LLM
# -----------------------------------

llm = OllamaLLM(model="llama3")

# -----------------------------------
# UPLOAD CSV
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# -----------------------------------
# PROCESS FILE
# -----------------------------------

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # -----------------------------------
    # CONVERT NUMERIC COLUMNS
    # -----------------------------------

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # -----------------------------------
    # SHOW DATA
    # -----------------------------------

    st.subheader("Uploaded Data")
    st.dataframe(df.head())

    # -----------------------------------
    # SHOW DATA TYPES
    # -----------------------------------

    st.subheader("Column Data Types")
    st.write(df.dtypes)

    # -----------------------------------
    # CREATE DATABASE
    # -----------------------------------

    conn = sqlite3.connect("dynamic_data.db")

    table_name = "uploaded_data"

    # Remove old table
    cursor = conn.cursor()

    cursor.execute(
        f"DROP TABLE IF EXISTS {table_name}"
    )

    conn.commit()

    # Store fresh CSV
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    st.success("CSV uploaded successfully!")

    # -----------------------------------
    # USER QUESTION
    # -----------------------------------

    question = st.text_input(
        "Ask question about your data"
    )

    # -----------------------------------
    # GENERATE ANSWER
    # -----------------------------------

    if st.button("Generate Answer"):

        columns = ", ".join(df.columns)

        question_lower = question.lower()

        # -----------------------------------
        # SPECIAL RULES
        # -----------------------------------

        if (
            "highest" in question_lower
            or "maximum" in question_lower
            or "max" in question_lower
        ):

            if "price" in question_lower:

                sql_query = f"""
                SELECT *
                FROM {table_name}
                ORDER BY price DESC
                LIMIT 1
                """

            else:

                prompt = f"""
                You are an SQL expert.

                Table name:
                {table_name}

                Columns:
                {columns}

                Convert user question into SQLite SQL query.

                Return ONLY SQL query.
                No markdown.
                No explanation.

                User Question:
                {question}
                """

                sql_query = llm.invoke(prompt)

        else:

            # -----------------------------------
            # NORMAL AI FLOW
            # -----------------------------------

            prompt = f"""
            You are an SQL expert.

            Table name:
            {table_name}

            Columns:
            {columns}

            Examples:

            Question:
            Show highest price row

            SQL:
            SELECT * FROM uploaded_data
            ORDER BY price DESC
            LIMIT 1;

            Question:
            Show average price

            SQL:
            SELECT AVG(price) FROM uploaded_data;

            Question:
            Count total rows

            SQL:
            SELECT COUNT(*) FROM uploaded_data;

            Convert user question into SQLite SQL query.

            Return ONLY SQL query.
            No markdown.
            No explanation.

            User Question:
            {question}
            """

            sql_query = llm.invoke(prompt)

        # -----------------------------------
        # CLEAN SQL
        # -----------------------------------

        sql_query = sql_query.replace(
            "```sql",
            ""
        )

        sql_query = sql_query.replace(
            "```",
            ""
        )

        sql_query = sql_query.strip()

        # -----------------------------------
        # SHOW SQL
        # -----------------------------------

        st.subheader("Generated SQL Query")

        st.code(
            sql_query,
            language="sql"
        )

        # -----------------------------------
        # SQL SAFETY CHECK
        # -----------------------------------

        dangerous_words = [
            "DROP",
            "DELETE",
            "TRUNCATE",
            "ALTER",
            "UPDATE"
        ]

        if any(
            word in sql_query.upper()
            for word in dangerous_words
        ):
            st.error(
                "Dangerous SQL detected!"
            )

            st.stop()

        # -----------------------------------
        # EXECUTE SQL
        # -----------------------------------

        try:

            engine = create_engine(
                "sqlite:///dynamic_data.db"
            )

            result = pd.read_sql(
                sql_query,
                engine
            )

            # -----------------------------------
            # SHOW RESULT
            # -----------------------------------

            st.subheader("Query Result")

            st.dataframe(result)

            # -----------------------------------
            # DOWNLOAD RESULT
            # -----------------------------------

            csv = result.to_csv(
                index=False
            )

            st.download_button(
                "Download Results",
                csv,
                "results.csv",
                "text/csv"
            )

            # -----------------------------------
           

        except Exception as e:

            st.error(f"Error: {e}")