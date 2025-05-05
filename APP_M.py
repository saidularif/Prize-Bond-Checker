import streamlit as st
import pandas as pd

st.title("💸 Prize Bond Checker")

# Upload Test List
uploaded_file = st.file_uploader("Upload your Test List Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Load fixed Results file
        results_df = pd.read_excel("Results.xlsx", dtype=str)
        test_list_df = pd.read_excel(uploaded_file, dtype=str)

        # Clean both files
        results_df = results_df.astype(str).apply(lambda col: col.str.strip())
        test_list_df = test_list_df.astype(str).apply(lambda col: col.str.strip())

        # Flatten and deduplicate test numbers
        test_numbers = pd.unique(test_list_df.values.ravel())
        any_match = False

        st.write("### 🎯 Matching Results:")
        for number in test_numbers:
            if number == "" or number.lower() == "nan":
                continue
            for idx, column in enumerate(results_df.columns):
                if number in results_df[column].values:
                    st.success(f'{number} found in Result file column {idx + 1}')
                    any_match = True
                    break

        if not any_match:
            st.warning("You will Win Next Time, In Sha Allah ✨")

    except Exception as e:
        st.error(f"Error: {e}")
