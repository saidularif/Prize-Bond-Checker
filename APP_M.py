import pandas as pd
import streamlit as st

# Load the results file from GitHub
RESULTS_FILE = 'https://raw.githubusercontent.com/saidularif/Prize-Bond-Checker/main/Results.xlsx'

def load_data(uploaded_file):
    try:
        # Load and clean the uploaded Excel file
        test_list_df = pd.read_excel(uploaded_file, dtype=str).apply(lambda col: col.astype(str).str.strip())
        return test_list_df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def check_matches(results_df, test_list_df):
    # Flatten and clean test numbers
    test_numbers = pd.unique(test_list_df.values.ravel())
    test_numbers = [num for num in test_numbers if str(num).strip().lower() != 'nan']
    
    any_match = False
    result_message = []

    # Check for matches
    for number in test_numbers:
        number = str(number).strip()
        for column in results_df.columns:
            # Check if the number exists in the current column
            matches = results_df[results_df[column] == number]
            
            if not matches.empty:
                # Get the column name which represents the draw number
                draw_number = column
                result_message.append(f'-' * 40)
                result_message.append(f'Congratulations! Your number {number} won!')
                result_message.append(f'   Draw Number: "{draw_number}"')
                result_message.append(f'   Winning Number: {number}')
                result_message.append('-' * 40 + '\n')
                any_match = True
                break  # Stop checking other columns for this number

    if not any_match:
        result_message.append('-' * 40)
        result_message.append("No winning numbers found this time.")
        result_message.append("You will win next time, In Sha Allah!")
        result_message.append('-' * 40)

    return "\n".join(result_message)

def main():
    st.title("Prize Bond Number Matching")

    # File upload widget
    uploaded_file = st.file_uploader("Upload your Test List Excel file", type=["xlsx"])
    
    if uploaded_file:
        # Load and clean the results file from GitHub
        try:
            results_df = pd.read_excel(RESULTS_FILE, dtype=str).apply(lambda col: col.astype(str).str.strip())
        except Exception as e:
            st.error(f"Error loading results file: {e}")
            return

        # Load the user's test list file
        test_list_df = load_data(uploaded_file)
        if test_list_df is not None:
            result = check_matches(results_df, test_list_df)
            st.text(result)

if __name__ == "__main__":
    main()
