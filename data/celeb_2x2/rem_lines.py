import os
import pandas as pd


def filter_csv_by_folder(csv_path, folder_path):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_path)

    # Iterate through rows starting from the second row
    for index, row in df.iloc[1:].iterrows():
        value_to_check = row.iloc[1]  # Assuming the second column (index 1)

        # Check if the value in the second column exists in the given folder
        file_path_to_check = os.path.join(folder_path, str(value_to_check))

        if not os.path.exists(file_path_to_check):
            # If the file does not exist, remove the entire row
            df = df.drop(index)

    # Write the modified DataFrame back to the CSV file
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file_path = 'D:\Test\Sharing\Jigsaw-Solver\datagen_scripts\celeb\celeb_2x2/train.csv'

    # Specify the path to the folder
    folder_path = 'D:\Test\Sharing\Jigsaw-Solver\datagen_scripts\celeb\celeb_2x2/train'

    # Call the function to filter the CSV file based on the folder contents
    filter_csv_by_folder(csv_file_path, folder_path)
