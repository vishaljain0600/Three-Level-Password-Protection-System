import tkinter as tk
from tkinter import messagebox
import hashlib
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
from skimage.metrics import structural_similarity as compare_ssim
import imageio
import os



user_database = {
    'shubh': {
        'password': '2cf95126b079bbe38bd1e224d56367f47875ea81aa1e1a57ff74ffe1bfe4d166',  # Hashed password
    },
    'harsh': {
        'password': 'd551349041e11f87c0d444c7485c66ee8e6665d521682fb1702d19f4bea50d49',  # Hashed password
}}

# Global variables for Captcha
captcha_code = ""

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    if username in user_database:
        stored_password = user_database[username]['password']
        if stored_password == hash_password(password):
            messagebox.showinfo("Login Successful", "Login successful")
        else:
            messagebox.showerror("Login Failed", "Incorrect password")
    else:
        messagebox.showerror("Login Failed", "User not found")

def generate_captcha():
    global captcha_code
    captcha_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(6))

def create_captcha_image(captcha_code):
    image = Image.new('RGB', (200, 80), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    fnt = ImageFont.load_default()

    d.text((10, 10), captcha_code, fill=(0, 0, 0), font=fnt)

    return image

def verify_captcha(input_text):
    global captcha_code
    if input_text == captcha_code:
        messagebox.showinfo("Captcha Verification", "Captcha matched successfully.")
    else:
        messagebox.showerror("Captcha Verification", "Captcha mismatch.")

    # Regenerate a new Captcha
    generate_captcha()
    update_captcha_image()

def update_captcha_image():
    global captcha_image_label, captcha_code
    captcha_image_label.config(image=None)

    captcha_image = create_captcha_image(captcha_code)
    photo = ImageTk.PhotoImage(captcha_image)
    captcha_image_label.config(image=photo)
    captcha_image_label.image = photo

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    if ret:
        return image
    else:
        messagebox.showerror("Image Capture Error", "Failed to capture an image from the camera.")
        return None



def level_1_ui():
    root = tk.Tk()
    root.title("Level 1 - Username and Password")

    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")  # Hide the password
    password_entry.pack()

    login_button = tk.Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
    login_button.pack()

    root.mainloop()
    
def compare_images(image1, image2):
        # Convert both images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Resize the smaller image to match the dimensions of the larger image
    if gray_image1.shape != gray_image2.shape:
        height, width = max(gray_image1.shape[0], gray_image2.shape[0]), max(gray_image1.shape[1], gray_image2.shape[1])
        gray_image1 = cv2.resize(gray_image1, (width, height))
        gray_image2 = cv2.resize(gray_image2, (width, height))

    similarity = compare_ssim(gray_image1, gray_image2)
    return similarity



def level_2_image_checker():
    root = tk.Tk()
    root.title("Level 2 - Image Checker")

    # Load the reference image
    reference_image = cv2.imread('D:\Major Project\mypic.jpg')

    def check_image():
        captured_image = capture_image()

        if captured_image is not None:
            similarity = compare_images(reference_image, captured_image)
            if similarity > 0.8:  # Adjust the threshold as needed

                messagebox.showerror("Image Check", "Image mismatch.")

            else:
                messagebox.showinfo("Image Check", "Image matched successfully.")

               
                
        else:
            messagebox.showerror("Image Check", "Failed to capture an image from the camera.")

    capture_button = tk.Button(root, text="Capture Image", command=check_image)
    capture_button.pack()

    root.mainloop()


def level_3_captcha_ui():
    global captcha_image_label
    root = tk.Tk()
    root.title("Level 3 - Captcha")

    generate_captcha()
    captcha_image = create_captcha_image(captcha_code)
    photo = ImageTk.PhotoImage(captcha_image)

    captcha_image_label = tk.Label(root, image=photo)
    captcha_image_label.pack()

    entry_label = tk.Label(root, text="Enter Captcha:")
    entry_label.pack()

    captcha_entry = tk.Entry(root)
    captcha_entry.pack()

    verify_button = tk.Button(root, text="Verify", command=lambda: verify_captcha(captcha_entry.get()))
    verify_button.pack()

    regenerate_button = tk.Button(root, text="Regenerate Captcha", command=update_captcha_image)
    regenerate_button.pack()

    root.mainloop()

def open_major_project_folder():
    folder_path = 'D:\Major Project'

    try:
        os.system(f'start explorer {folder_path}')
    except Exception as e:
        messagebox.showerror("Error Opening Major Project Folder", str(e))    

if __name__ == "__main__":
    level_1_ui()
    level_2_image_checker()
    level_3_captcha_ui()
    open_major_project_folder()

