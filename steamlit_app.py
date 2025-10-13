import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# ------------------------------
# STREAMLIT APP HEADER
# ------------------------------
st.title("🌍 Global Warming Data Visualization App")
st.header("Interactive Data Insights Dashboard")
st.subheader("By: Sehal Varshney")

# ------------------------------
# FILE UPLOAD
# ------------------------------
uploaded_file = st.file_uploader("Upload your Global Warming CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Data Preview
    st.write("### 🧾 Data Preview", df.head())
    st.write(f"Shape of dataset: {df.shape}")
    st.write("### Column Information")
    st.write(df.dtypes)

    # Select numeric and all columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    all_cols = df.columns.tolist()

    # ------------------------------
    # BASIC PLOTLY VISUALIZATIONS
    # ------------------------------
    st.markdown("## 📊 Interactive Chart Explorer")

    x_axis = st.selectbox("Select X-axis", options=all_cols)
    y_axis = st.selectbox("Select Y-axis", options=numeric_cols)
    chart_type = st.radio(
        "Choose chart type",
        ["Scatter", "Line", "Bar", "Histogram", "Boxplot", "Heatmap (Seaborn)"],
        horizontal=True
    )

    if chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram":
        fig = px.histogram(df, x=y_axis, nbins=30, title=f"Distribution of {y_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Boxplot":
        fig = px.box(df, x=x_axis, y=y_axis, title=f"Boxplot of {y_axis} by {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Heatmap (Seaborn)":
        st.write("### 🔥 Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig)

   

    # ------------------------------
    # DEEP INSIGHT CHARTS (SEABORN)
    # ------------------------------
    st.markdown("## 📈 Deep Insights (Seaborn Visuals)")

    insight_type = st.selectbox(
        "Choose advanced insight",
        ["Pairplot", "Trend Over Time", "Distribution Plot"]
    )

    if insight_type == "Pairplot":
        st.write("### Pairwise Relationships")
        fig = sns.pairplot(df[numeric_cols])
        st.pyplot(fig)

    elif insight_type == "Trend Over Time":
        time_col = st.selectbox("Select time/date column", options=all_cols)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df, x=time_col, y=y_axis, ax=ax)
        plt.title(f"Trend of {y_axis} over {time_col}")
        st.pyplot(fig)

    elif insight_type == "Distribution Plot":
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df[y_axis], kde=True, ax=ax)
        plt.title(f"Distribution of {y_axis}")
        st.pyplot(fig)

    

else:
    st.info("📤 Please upload your Global Warming dataset (CSV format) to begin visualization.")
