import streamlit as st
import pandas as pd
import plotly.express as px

st.title("DV Assignment")
st.header("Streamlit Data Visualisation App")
st.subheader("By: Sehal Varshney")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)

    # Show preview
    st.write("### Preview of Data", df.head())

    # Dropdowns to choose columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    all_cols = df.columns.tolist()

    x_axis = st.selectbox("Select X-axis", options=all_cols)
    y_axis = st.selectbox("Select Y-axis", options=numeric_cols)

    chart_type = st.radio("Choose chart type", ["Scatter", "Line", "Bar", "Histogram", "Boxplot"])

    # Plotly visualizations
    if chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
    elif chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=y_axis, nbins=20, title=f"Distribution of {y_axis}")
    elif chart_type == "Boxplot":
        fig = px.box(df, x=x_axis, y=y_axis, title=f"Boxplot of {y_axis} by {x_axis}")

    # Show interactive chart
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Misleading Visualisation Section
    # -------------------------------
    st.markdown("## 🚨 Analyse Misleading Visualisations")

    misleading = st.checkbox("Show an example of a misleading chart")
    if misleading:
        # Misleading chart: truncated y-axis
        fig_bad = px.line(df, x=x_axis, y=y_axis, title=f"⚠️ Misleading Chart: Truncated Y-axis")
        fig_bad.update_yaxes(range=[df[y_axis].min()*0.9, df[y_axis].max()*0.95])  # cuts off real range
        st.plotly_chart(fig_bad, use_container_width=True)
        st.write(
            "**Why misleading?**\n"
            "- The Y-axis is truncated, making changes look smaller/larger than reality.\n"
            "- Hides true variation in the data."
        )

        # Correct chart
        fig_good = px.line(df, x=x_axis, y=y_axis, title=f"✅ Correct Chart: Full Y-axis")
        st.plotly_chart(fig_good, use_container_width=True)
        st.write(
            "**Why better?**\n"
            "- Starts from zero or appropriate baseline.\n"
            "- Shows actual scale of the data without exaggeration."
        )
