import os
import shutil


def sort_and_keep_top_n(input_folder, n=27060):
    # Get a list of all files in the input folder
    file_list = os.listdir(input_folder)

    # Sort the files by name in ascending order
    sorted_files = sorted(file_list, key=lambda x: int(x.split('.')[0]))

    # Keep only the first n files
    files_to_keep = sorted_files[:n]

    # Delete the remaining files
    for file_name in sorted_files[n:]:
        file_path = os.path.join(input_folder, file_name)
        os.remove(file_path)


if __name__ == "__main__":
    # Specify the path to your input folder containing images
    input_folder_path = 'D:\Test\Sharing\Jigsaw-Solver\datagen_scripts\celeb\celeb_2x2/train'

    # Call the function to sort, keep the top 27,060 images, and delete the rest
    sort_and_keep_top_n(input_folder_path, n=27060)
