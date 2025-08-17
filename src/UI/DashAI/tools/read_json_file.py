import json
import os

def get_all_financial_data(base_path: str = "/Users/nainnyvijayvargiya/Downloads/UI 4/Data/all_tools_cleaned"):
    """
    Reads all JSON data files starting with 'fetch_' from the given base_path
    and returns their combined content.

    Args:
        base_path (str): The base directory where the JSON files are located.
                         Defaults to "./13131313".
                         Ensure this path is correct relative to where
                         your agent.py is run.

    Returns:
        dict: A dictionary containing all the extracted financial data.
              Keys are derived from the filenames (e.g., 'bank_transactions'
              for 'fetch_bank_transactions.json'), and values are the parsed
              JSON content. If a file is not found, cannot be parsed, or
              is a directory, its value will be None.
    """
    all_data = {}

    print(f"Attempting to load financial data from base_path: {base_path}")
    print(f"Current working directory: {os.getcwd()}")

    if not os.path.exists(base_path):
        print(f"Error: Base path '{base_path}' does not exist.")
        return all_data
    
    if not os.path.isdir(base_path):
        print(f"Error: Base path '{base_path}' is not a directory.")
        return all_data

    # Iterate over all files in the base_path
    for filename in os.listdir(base_path):
        # Check if the file starts with 'fetch_' and ends with '.json'
        if filename.startswith("fetch_") and filename.endswith(".json"):
            file_path = os.path.join(base_path, filename)
            key = filename[len("fetch_"):-len(".json")]  # Extract key from the filename
            print(f"Attempting to read file: {file_path}")

            try:
                if not os.path.isfile(file_path):
                    # Ensure it's a regular file, not a directory or symlink
                    raise IsADirectoryError(f"Error: Path is a directory or not a regular file: '{file_path}'")

                with open(file_path, 'r') as f:
                    data = json.load(f)
                    all_data[key] = data
                    print(f"Successfully loaded {filename}.")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from '{file_path}': {e.msg}. Skipping this data type.")
                all_data[key] = None
            except IsADirectoryError:
                print(f"Error: Expected a file but found a directory at '{file_path}'. Skipping this data type.")
                all_data[key] = None
            except Exception as e:
                print(f"An unexpected error occurred while processing '{filename}' at '{file_path}': {e}. Skipping this data type.")
                all_data[key] = None

    return all_data
