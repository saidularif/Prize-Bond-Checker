import streamlit as st
import pandas as pd

def check_matches(results_df, test_list_df):
    test_numbers = pd.unique(test_list_df.values.ravel())
    test_numbers = [num for num in test_numbers if str(num).strip().lower() != 'nan']

    matches = []
    any_match = False

    for number in test_numbers:
        number = str(number).strip()
        for column in results_df.columns:
            matches_found = results_df[results_df[column] == number]
            
            if not matches_found.empty:
                draw_number = column
                matches.append({
                    'message': f'Congratulations! Your number {number} won!',
                    'draw_number': draw_number,
                    'winning_number': number
                })
                any_match = True
                break  # Stop checking other columns for this number

    if not any_match:
        matches.append({
            'message': "No winning numbers found this time. You will win next time, In Sha Allah!"
        })

    return matches


def main():
    st.title("Prize Bond Match Checker")

    # File upload
    results_file = st.file_uploader("Upload the Results File", type=["xlsx"])
    test_list_file = st.file_uploader("Upload your Test List File", type=["xlsx"])

    if results_file and test_list_file:
        try:
            # Load and clean the Excel files
            results_df = pd.read_excel(results_file, dtype=str).apply(lambda col: col.astype(str).str.strip())
            test_list_df = pd.read_excel(test_list_file, dtype=str).apply(lambda col: col.astype(str).str.strip())

            # Check for matches
            matches = check_matches(results_df, test_list_df)

            # Display results
            for match in matches:
                st.write('-' * 40)
                st.write(match['message'])
                if 'draw_number' in match:
                    st.write(f'Draw Number: {match["draw_number"]}')
                    st.write(f'Winning Number: {match["winning_number"]}')
                st.write('-' * 40)

        except FileNotFoundError as e:
            st.error(f"Error: File not found - {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
