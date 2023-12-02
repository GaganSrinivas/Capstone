from PIL import Image
import os


def create_masks(output_dir, num_masks, bar_width_percentage, bar_length, distance_between_masks):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a white background mask
    mask_size = (512, 512)
    white_mask = Image.new("L", mask_size, color=255)  # 255 for white

    for i in range(num_masks):
        # Calculate the distance from the top for each mask
        distance_from_top = i * distance_between_masks

        # Create a new mask by pasting a black bar onto the white mask
        current_mask = white_mask.copy()
        # Reduce the width by percentage
        bar_width = int(bar_width_percentage * mask_size[1])
        current_mask.paste(Image.new("L", (bar_length, bar_width), color=0), (
            (mask_size[0] - bar_length) // 2, distance_from_top))

        # Save the current mask
        mask_name = f'mask_{i+1}.jpg'
        current_mask.save(os.path.join(output_dir, mask_name))


# Example usage with user input
output_directory = 'D:/IRDBT/mask_images'
num_masks = int(input("Enter the number of masks: "))
bar_width_percentage = float(
    input("Enter the bar width percentage (e.g., 0.7 for 70%): "))
bar_length = int(input("Enter the bar length: "))
distance_between_masks = int(input("Enter the distance between masks: "))

create_masks(output_directory, num_masks, bar_width_percentage,
             bar_length, distance_between_masks)
