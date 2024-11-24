import os
import cv2
import pytesseract
from PIL import Image, ImageTk
import shutil
import time
from tkinter import Tk, Button, Label, Entry, filedialog, Listbox, Scrollbar, Canvas, StringVar,PhotoImage

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
    # result_listbox.delete(0, 'end')
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
    o=[]
    search_term = search_entry.get()
    matching_images = [filename for filename in os.listdir(output_folder_path) if search_term.lower() in filename.lower()]
    result_listbox.delete(0, 'end')
    for filename in os.listdir(output_folder_path):
        output_path = os.path.join(output_folder_path, filename)
        o.append(output_path)
    for image in matching_images:
        result_listbox.insert('end', image)
    for image in o:
        image_path=cv2.imread(image)
        cv2.imshow("Image to be deleted",image_path)
        cv2.waitKey(0)


def create_folder():
    folder_path = filedialog.askdirectory(title="Select Destination Folder for Separated Images")
    if folder_path:
        os.makedirs(os.path.join(folder_path, "SeparatedImages"), exist_ok=True)
        print("Folder created for separated images!")

def retrieve_images():
    query_text = search_entry.get()
    matching_images = retrieve_images_from_folder(folder_path, query_text)
    
    for img in matching_images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((150, 150))
        photo = ImageTk.PhotoImage(img)
        result_listbox.image_create('end', image=photo)
        result_listbox.insert('end', '\n')

def retrieve_images2():
    # result_listbox.delete(0, 'end')
    query_text = search_entry.get()
    matching_images = retrieve_images_from_folder2(folder_path, query_text)
    i = 1
    for img in matching_images:
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = Image.fromarray(img)
        # img.thumbnail((150, 150))
        # photo = ImageTk.PhotoImage(img)
        # result_listbox.image_create('end', image=photo)
        result_listbox.insert(i, img)
        i += 1
    o=[]
    for image in matching_images:
        input_path = os.path.join(folder_path, image)
        o.append(input_path)
    # for image in matching_images:
    #     result_listbox.insert('end', image)
    for image in o:
        image_path=cv2.imread(image)
        cv2.imshow("Matching Image",image_path)
        cv2.waitKey(0)

def retrieve_images_from_folder(folder_path, query_text):
    matching_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray_image, config=my_config)
            if query_text in text:
                matching_images.append(image)
    
    return matching_images

def retrieve_images_from_folder2(folder_path, query_text):
    matching_images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray_image, config=my_config)
            if query_text in text:
                matching_images.append(filename)
    
    return matching_images

def clear_results():
    result_listbox.delete(0, 'end')

root = Tk()
root.title("Snapspot")
bg = PhotoImage(file = "JShine.jpg") 
canvas1 = Canvas( root, width = 400, 
                 height = 400,scrollregion=(0,0,400,400)) 
  
canvas1.pack(fill = "both", expand = True) 
  
# Display image 
canvas1.create_image( 0, 0, image = bg,  
                     anchor = "nw") 
# Deletion Section
delete_button = Button(root, text="Delete Images", command=delete_images)
# delete_button.pack()

create_folder_button = Button(root, text="Create Folder for Separated Images", command=create_folder)
# create_folder_button.pack()

# Retrieval Section
label = Label(root, text="Enter search term:")
# label.pack()
canvas1.create_window(650,140,window=label)

query = StringVar()
query.set("")
search_entry = Entry(root, textvariable = query)
# search_entry.pack()
canvas1.create_window(660,170,window=search_entry)

search_button = Button(root, text="Search Images", command=retrieve_images2)
# search_button.pack()

result_label = Label(root, text="Matching Images:")
# result_label.pack()

result_listbox = Listbox(root, selectmode="extended")
# result_listbox.pack()
canvas1.create_window(660,300,window=result_listbox)

# scrollbar = Scrollbar(root, command=result_listbox.yview)
# scrollbar.pack(side="right", fill="y")
# result_listbox.config(yscrollcommand=scrollbar.set)
# canvas1.create_window()
clear_button = Button(root, text="Clear Results", command=clear_results)
# clear_button.pack()
can_del1=canvas1.create_window(600, 10,  
                                       anchor = "nw", 
                                       window = delete_button)
can_sear=canvas1.create_window(600, 40,  
                                       anchor = "nw", 
                                       window = search_button)
can_fol=canvas1.create_window(600, 70,  
                                       anchor = "nw", 
                                       window = create_folder_button)
can_clear=canvas1.create_window(600, 100,  
                                       anchor = "nw", 
                                       window = clear_button)

root.mainloop()