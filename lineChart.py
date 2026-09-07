import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="EDA Dashboard",
    page_icon="",
    layout="wide"
)

st.title("Streamlit-Based Exploratory Data Analysis")
st.write("Upload a CSV dataset to explore its structure, statistics, and visual patterns.")


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


# ---------------------------------------------------
# CHECK IF FILE IS UPLOADED
# ---------------------------------------------------

if uploaded_file is None:

    st.info("Please upload a CSV file from the sidebar.")

else:

    # ---------------------------------------------------
    # READ AND VALIDATE CSV
    # ---------------------------------------------------

    try:
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.error("The uploaded CSV file is empty.")
            st.stop()

    except Exception:
        st.error("Invalid CSV file. Please upload a correctly formatted CSV file.")
        st.stop()


    # ---------------------------------------------------
    # DATASET PREVIEW
    # ---------------------------------------------------

    st.header("Dataset Preview")

    st.dataframe(
        df.head(5),
        use_container_width=True
    )


    # ---------------------------------------------------
    # DATASET DIMENSIONS
    # ---------------------------------------------------

    st.header("Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Number of Rows", df.shape[0])

    with col2:
        st.metric("Number of Columns", df.shape[1])


    # ---------------------------------------------------
    # DATA TYPES
    # ---------------------------------------------------

    st.subheader("Column Data Types")

    data_types = pd.DataFrame({
        "Attribute": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(
        data_types,
        use_container_width=True
    )


    # ---------------------------------------------------
    # MISSING VALUES
    # ---------------------------------------------------

    st.subheader("Missing Values")

    missing_values = pd.DataFrame({
        "Attribute": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        missing_values,
        use_container_width=True
    )


    # ---------------------------------------------------
    # NUMERICAL STATISTICS
    # ---------------------------------------------------

    st.subheader("Numerical Statistics")

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:

        statistics = pd.DataFrame({
            "Mean": df[numerical_columns].mean(),
            "Median": df[numerical_columns].median(),
            "Minimum": df[numerical_columns].min(),
            "Maximum": df[numerical_columns].max()
        })

        st.dataframe(
            statistics,
            use_container_width=True
        )

    else:
        st.info("No numerical attributes found in the dataset.")


    # ---------------------------------------------------
    # ATTRIBUTE SELECTION
    # ---------------------------------------------------

    st.sidebar.subheader("Attribute Selection")

    selected_column = st.sidebar.selectbox(
        "Select a column for analysis",
        df.columns
    )


    # ---------------------------------------------------
    # AUTOMATIC ATTRIBUTE TYPE DETECTION
    # ---------------------------------------------------

    selected_data = df[selected_column]

    if pd.api.types.is_numeric_dtype(selected_data):

        attribute_type = "Numerical"

    else:

        attribute_type = "Categorical"


    st.header("Attribute Analysis")

    st.write(
        f"**Selected Attribute:** {selected_column}"
    )

    st.write(
        f"**Detected Attribute Type:** {attribute_type}"
    )


    # ---------------------------------------------------
    # VISUALIZATION
    # ---------------------------------------------------

    st.subheader("Visualization")


    # ---------------------------------------------------
    # NUMERICAL → HISTOGRAM
    # ---------------------------------------------------

    if attribute_type == "Numerical":

        st.write(
            f"Distribution of {selected_column}"
        )

        fig, ax = plt.subplots()

        ax.hist(
            selected_data.dropna(),
            bins=20
        )

        ax.set_title(
            f"Distribution of {selected_column}"
        )

        ax.set_xlabel(
            selected_column
        )

        ax.set_ylabel(
            "Frequency"
        )

        st.pyplot(fig)


    # ---------------------------------------------------
    # CATEGORICAL → BAR CHART
    # ---------------------------------------------------

    else:

        st.write(
            f"Frequency of {selected_column}"
        )

        value_counts = selected_data.value_counts().head(20)

        fig, ax = plt.subplots()

        value_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            f"Frequency of {selected_column}"
        )

        ax.set_xlabel(
            selected_column
        )

        ax.set_ylabel(
            "Frequency"
        )

        plt.xticks(rotation=45)

        st.pyplot(fig)