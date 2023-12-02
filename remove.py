import os


def sort_and_keep_top_n(directory, n=9000):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Sort the files by name in ascending order
    sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))

    # Keep only the first n files
    files_to_keep = sorted_files[:n]

    # Remove all other files
    for file_name in sorted_files:
        file_path = os.path.join(directory, file_name)
        if file_name not in files_to_keep:
            os.remove(file_path)


if __name__ == "__main__":
    # Specify the directory containing the images
    image_directory = 'data/puzzle_2x2/train'

    # Call the function to sort and keep only the first 100 images
    sort_and_keep_top_n(image_directory, n=9000)
