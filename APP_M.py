import pandas as pd
import streamlit as st

# Load the results file from GitHub (replace with your actual GitHub raw file URL)
RESULTS_FILE = 'https://raw.githubusercontent.com/saidularif/Prize-Bond-Checker/main/Results.xlsx'

def load_data(uploaded_file):
    try:
        # Load and clean the uploaded Excel file
        test_list_df = pd.read_excel(uploaded_file, dtype=str).apply(lambda col: col.astype(str).str.strip())
        return test_list_df
    except Exception as e:
        st.error(f"❌ Error loading your file: {e}")
        return None

def check_matches(results_df, test_list_df):
    # Flatten and clean user-entered numbers
    test_numbers = pd.unique(test_list_df.values.ravel())
    test_numbers = [num for num in test_numbers if str(num).strip().lower() != 'nan']
    
    any_match = False
    result_message = []

    # Match user numbers against result sheet
    for number in test_numbers:
        number = str(number).strip()
        for column in results_df.columns:
            matches = results_df[results_df[column] == number]
            if not matches.empty:
                draw_number = column
                result_message.append(f"🎉 **Congratulations!** Your number `{number}` won in **Draw: {draw_number}**")
                any_match = True
                break  # Stop further checking this number

    if not any_match:
        result_message.append("😞 No winning numbers found this time.")
        result_message.append("Keep trying — your luck may shine next time, In Sha Allah!")

    return "\n\n".join(result_message)

def main():
    st.title("🏆 Prize Bond Checker")
    st.write("Check if your Prize Bond numbers have won in the latest draw results.")

    # Upload field
    uploaded_file = st.file_uploader("📂 Please upload an Excel file containing all your Prize Bond numbers", type=["xlsx"])

    if uploaded_file:
        # Load the official result Excel file from GitHub
        try:
            results_df = pd.read_excel(RESULTS_FILE, dtype=str).apply(lambda col: col.astype(str).str.strip())
        except Exception as e:
            st.error(f"❌ Failed to load results file: {e}")
            return

        # Process uploaded file
        test_list_df = load_data(uploaded_file)
        if test_list_df is not None:
            result = check_matches(results_df, test_list_df)
            st.markdown(result)

if __name__ == "__main__":
    main()
