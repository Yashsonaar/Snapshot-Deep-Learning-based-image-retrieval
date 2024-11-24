import os
import pytesseract
from PIL import Image, ImageTk
import shutil
import time
import cv2
from tkinter import Tk, Button, Label, Entry, filedialog, Listbox, Scrollbar, Canvas

# Configuration for Tesseract OCR
my_config = "--psm 11"

# Path to the phone gallery or folder
folder_path = "D:\PD 2"

# Path to the separate folder for images with keywords
output_folder_path = "D:\sorted images"

# List of keywords to search for
keywords = ["good", "happy", "friendship", "diwali"]

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

def delete_images():
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image, config=my_config)
                if any(keyword in text.lower() for keyword in keywords):
                    output_path = os.path.join(output_folder_path, filename)
                    shutil.move(image_path, output_path)
                    if os.path.exists(output_path):
                        output_path = os.path.join(output_folder_path, f"{filename}_{time.time()}")
                    image.save(output_path)
            except Exception as e:
                print(f"Error processing image '{filename}': {str(e)}")
    print("Deletion completed!")

def create_folder():
    folder_path = filedialog.askdirectory(title="Select Destination Folder for Separated Images")
    if folder_path:
        os.makedirs(os.path.join(folder_path, "SeparatedImages"), exist_ok=True)
        print("Folder created for separated images!")

def search_images():
    print("Hello")

def clear_results():
    result_listbox.delete(0, 'end')

root = Tk()
root.title("Image Management App")

# Deletion Section
delete_button = Button(root, text="Delete Images", command=delete_images)
delete_button.pack()

create_folder_button = Button(root, text="Create Folder for Separated Images", command=create_folder)
create_folder_button.pack()

# Retrieval Section
label = Label(root, text="Enter search term:")
label.pack()

search_entry = Entry(root)
search_entry.pack()

search_button = Button(root, text="Search Images", command=search_images)
search_button.pack()

result_label = Label(root, text="Matching Images:")
result_label.pack()

result_listbox = Listbox(root, selectmode="extended")
result_listbox.pack()

scrollbar = Scrollbar(root, command=result_listbox.yview)
scrollbar.pack(side="right", fill="y")
result_listbox.config(yscrollcommand=scrollbar.set)

clear_button = Button(root, text="Clear Results", command=clear_results)
clear_button.pack()

root.mainloop()
