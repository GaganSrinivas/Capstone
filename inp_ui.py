import tkinter as tk
from tkinter import filedialog, Text, Scrollbar
from PIL import Image, ImageTk
import replicate
import os

# Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = "r8_Z8EpWfn92Uz86LhfTKzJZqepm0MIo1E3c8oO3"


def resize_image(image_path, target_size=(512, 512)):
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open the image using Pillow
    image = Image.open(image_path)
    # Resize the image to the target size
    resized_image = image.resize(target_size, Image.BICUBIC)
    return resized_image


def run_prediction():
    # Get the user input and mask file paths
    image_path = selected_image_path.get()
    mask_option = mask_var.get()

    # Set the folder where the model will read input and mask images
    input_folder = "D:/Test/Capstone/Jigsaw-Solver/inp_and_masks"

    # Map mask options to corresponding filenames
    mask_file_mapping = {
        "Top Right": "tr_mask.jpg",
        "Top Left": "tl_mask.jpg",
        "Bottom Right": "br_mask.jpg",
        "Bottom Left": "bl_mask.jpg",
    }

    # Check if the user selected a predefined mask option
    if mask_option in mask_file_mapping:
        mask_filename = mask_file_mapping[mask_option]
    else:
        # User selected the custom option, use the file selected by the user
        mask_filename = os.path.basename(filedialog.askopenfilename(
            title="Select Mask", filetypes=[("Image files", "*.jpg;*.png")]))

    mask_folder_path = "D:/Test/Capstone/Jigsaw-Solver/inp_and_masks"
    os.makedirs(mask_folder_path, exist_ok=True)  # Ensure the folder exists

    # Resize input image to 512x512 pixels
    resized_input_image = resize_image(image_path, target_size=(512, 512))
    # Save resized input image
    resized_input_image.save(os.path.join(
        input_folder, "resized_user_input.jpg"))

    # Resize mask image to 512x512 pixels
    resized_mask_image = resize_image(os.path.join(
        mask_folder_path, mask_filename), target_size=(512, 512))
    # Save resized mask image
    resized_mask_image.save(os.path.join(
        mask_folder_path, "resized_user_mask.jpg"))

    # Run prediction using the model hosted on Replicate
    deployment = replicate.deployments.get("gagansrinivas/faceinpainter")
    prediction = deployment.predictions.create(
        input={"image": open(os.path.join(input_folder, "resized_user_input.jpg"), "rb"),
               "mask": open(os.path.join(mask_folder_path, "resized_user_mask.jpg"), "rb"),
               "model": "celeba"}
    )
    prediction.wait()
    print(prediction.output)

    # Get the output image URL from the prediction output
    output_image_url = prediction.output

    if output_image_url:
        # Display the output URL in the result_text box
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(
            tk.END, f"Prediction complete. Output URL: {output_image_url}")
        # Tag the clickable portion
        result_text.tag_add("clickable", "1.43", "1.end")
        result_text.tag_config("clickable", foreground="blue", underline=True)
        result_text.config(state=tk.DISABLED)
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(
            tk.END, "Error: Output image URL not found in prediction output.")
        result_text.config(state=tk.DISABLED)


def on_click(event):
    # Open the output image URL in a web browser
    output_image_url = prediction.output
    if output_image_url:
        import webbrowser
        webbrowser.open(output_image_url)


def browse_image():
    file_path = filedialog.askopenfilename(
        title="Select Image", filetypes=[("Image files", "*.jpg;*.png")])

    # Update the selected_image_path variable and display the preview
    selected_image_path.set(file_path)
    display_image_preview(file_path)


def display_image_preview(image_path):
    if image_path:
        # Open the image using Pillow
        image = Image.open(image_path)
        # Resize the image to fit in a small preview
        image = image.resize((150, 150), Image.BICUBIC)
        # Convert the image to PhotoImage format
        photo_image = ImageTk.PhotoImage(image)
        # Update the label with the new image
        image_preview_label.config(image=photo_image)
        image_preview_label.image = photo_image


# Create the main window
root = tk.Tk()
root.title("Inpainter")
root.configure(bg="#0099cc")

# Create StringVar to store the selected image path
selected_image_path = tk.StringVar(root)

# Create Entry widgets for image path
entry_image = tk.Entry(
    root, width=30, textvariable=selected_image_path, state="readonly")
entry_image.grid(row=0, column=1, padx=10, pady=10)

# Create Label and Entry widget for mask dropdown
tk.Label(root, text="Image Path:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Mask Option:").grid(row=1, column=0, padx=10, pady=10)

# Define mask options
mask_options = ["Top Right", "Top Left", "Bottom Right", "Bottom Left"]

# Create a StringVar to store the selected mask option
mask_var = tk.StringVar(root)
mask_var.set(mask_options[0])  # Set the default mask option

# Create a dropdown menu for mask selection
mask_dropdown = tk.OptionMenu(root, mask_var, *mask_options)
mask_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Create Browse button for selecting image
tk.Button(root, text="Browse", command=browse_image).grid(
    row=0, column=2, padx=10, pady=10)

# Create Run button for running the prediction
tk.Button(root, text="Inpaint", command=run_prediction).grid(
    row=2, column=1, pady=20)

# Display the result of the prediction in a Text widget
# Adjust the height here
result_text = Text(root, height=5, width=40, wrap=tk.WORD)
result_text.grid(row=3, column=1, padx=10, pady=10)
result_text.config(state=tk.DISABLED)  # Make it read-only

# Bind the click event to the clickable portion
result_text.tag_bind("clickable", "<Button-1>", on_click)

# Create a label for displaying the image preview
image_preview_label = tk.Label(root)
image_preview_label.grid(row=4, column=1, pady=10)

# Use custom mask button
tk.Button(root, text="Use custom mask", command=browse_image).grid(
    row=5, column=0, padx=10, pady=10)

# Help button


def help():
    new_window = tk.Toplevel(root)
    new_window.title("Help")
    new_window.geometry("400x200")
    msg = (
        "Please upload the image to be inpainted - only image inputs allowed!\n"
        "Please wait for a few minutes after you upload to get your results."
    )
    tk.Label(new_window, text=msg, wraplength=400).pack()


tk.Button(root, text="Help!", command=help).grid(row=5, column=6, pady=10)

root.mainloop()
