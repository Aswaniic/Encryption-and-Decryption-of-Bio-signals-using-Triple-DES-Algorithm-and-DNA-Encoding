#import all the libraries
from Crypto.Cipher import DES3
from PIL import Image
import hashlib
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from Crypto.Util.Padding import pad, unpad
import io
global flag

# Define the function to generate the encryption keys
def generate_key():
    key = hashlib.sha256(b"secret key").digest()
    return key[:24]

# Generate the three encryption keys
key1 = generate_key()
key2 = generate_key()
key3 = generate_key()

# Define the function to encrypt the file
def encrypt_file(key1, key2, key3, filename):
    # Read the contents of the file
    # Check if the file is an image
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        # Open the image and convert it to bytes
        img = Image.open(filename)
        data = img.tobytes()
    else:
        # Read the contents of the file
        with open(filename, 'rb') as f:
            data = f.read()

    # Define the initialization vector
    iv = b'inithivg'
    print("Input:",data)

    # Pad the data if necessary
    padded_data = pad(data, DES3.block_size)

    # Encrypt using the first key
    cipher1 = DES3.new(key1, DES3.MODE_CBC, iv)
    ciphertext1 = cipher1.encrypt(padded_data)

    # Decrypt using the second key
    cipher2 = DES3.new(key2, DES3.MODE_CBC, iv)
    decrypted_padded_data = cipher2.decrypt(ciphertext1)

    # Encrypt using the third key
    cipher3 = DES3.new(key3, DES3.MODE_CBC, iv)
    ciphertext2 = cipher3.encrypt(decrypted_padded_data)
    # Write the encrypted data back to the file
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        # Save the encrypted image
        encrypted_img = Image.frombytes(img.mode, img.size, ciphertext2)
        encrypted_img.save('encrypted_ecg.png')
        with open(filename+'.enc', 'wb') as f:
            f.write(ciphertext2)
    else:
        with open(filename+'.enc', 'wb') as f:
            f.write(ciphertext2)
    with open(filename+'.enc', 'rb') as f:
            data = f.read()
    # Return the encrypted data
    return ciphertext2

def encrypt_withDNAencoding(key1, key2, key3, filename):
    ciphertext2=encrypt_file(key1,key2,key3,filename)

    ciphertext_final =dna_encoding(ciphertext2)
    print("Ciphertext:",ciphertext_final)
    # Write the encrypted data back to the file
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        img = Image.open(filename)
        # Save the encrypted image
        encrypted_img = Image.frombytes(img.mode, img.size, ciphertext_final.encode())
        encrypted_img.save('encrypted_ecg.png')
        with open(filename + '.enc', 'wb') as f:
            f.write(ciphertext_final.encode())
        with open(filename + '.enc', 'rb') as f:
            data = f.read()
    else:
        with open(filename + '.enc', 'wb') as f:
            f.write(ciphertext_final.encode())
        with open(filename + '.enc', 'rb') as f:
            data = f.read()
    # Return the encrypted data
    return ciphertext_final


# Define the function to choose the file and encrypt it
def decrypt_file(key1,key2,key3,filename,flag):

    with open(filename + '.enc', 'rb') as f:
            ct = f.read()
    if flag == True:
        ct=dna_decoding(ct)

    iv = b'inithivg'
        # Decrypt the data using Triple DES
    cipher3 = DES3.new(key3, DES3.MODE_CBC, iv)
    decrypted_data = cipher3.decrypt(ct)

    # Decrypt using the second key
    cipher2 = DES3.new(key2, DES3.MODE_CBC, iv)
    decrypted_newdata = cipher2.encrypt(decrypted_data)
    # Decrypt using the first key
    cipher1 = DES3.new(key1, DES3.MODE_CBC, iv)
    plaintext= cipher1.decrypt(decrypted_newdata)
    pt = unpad(plaintext, DES3.block_size)
    print("Decrypted text:",pt)
    if filename.endswith(".jpeg") or filename.endswith(".png"):
        # Save the decrypted image
        img =Image.open(filename)
        decrypted_img = Image.frombytes(img.mode,img.size,data=pt)

        #decrypted_img = Image.open(io.BytesIO(pt))
        decrypted_img.save('decrypted_ecg.png')
    else:
        with open('decrypted_file', 'wb') as f:
            f.write(pt)
        with open('decrypted_file', 'rb') as f:
            data = f.read()


    return pt
def dna_encoding(data):

    # Define the mapping of bytes to DNA base pairs
    mapping = {
        "00": "AT",
        "01": "TA",
        "10": "CG",
        "11": "GC",
    }
    # Convert data bytes to binary string
    binary_string = ''.join(format(byte, '08b') for byte in data)

    # Split binary string into groups of 2

    binary_groups = [binary_string[i:i + 2] for i in range(0, len(binary_string), 2)]

    # Map each binary group to its corresponding DNA base pair
    dna_string= "".join([mapping[pair] for pair in binary_groups])

    return dna_string
def dna_decoding(data):
    # Define the mapping of DNA base pairs to bytes
    mapping = {
        "AT": "00",
        "TA": "01",
        "CG": "10",
        "GC": "11",
    }
    # Convert the byte object to a string of the same content
    datanw = data.decode('latin-1')
    # Map each DNA base pair to its corresponding binary string
    binary_string = [datanw[i:i + 2] for i in range(0, len(datanw), 2)]
    # Map each DNA base group to its corresponding binary pair
    binary_string = "".join([mapping[pair] for pair in binary_string])

    # Convert the binary string to a byte object
    byte_object = bytes(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8))

    return byte_object


def choose_file():
    flag = False
    # Choose the file
    file_path = filedialog.askopenfilename()


    # Encrypt the data
    answer = messagebox.askyesno("Encryption", "Do you want to encrypt the file?")
    if answer:
        answer1 = messagebox.askyesno("DNA Encoding", "Do you want to include DNA encoding during Encryption?")
        if answer1:
                ciphertext = encrypt_withDNAencoding(key1, key2, key3, file_path)
                flag = True
        else:
            ciphertext = encrypt_file(key1,key2,key3,file_path)
        messagebox.showinfo("Success","File encrypted and saved successfully")

    else:
            messagebox.showinfo("Success", "File encrypted successfully, but not saved.")

    # Decrypt the data
    answer = messagebox.askquestion("Decryption", "Do you want to decrypt the file?")
    if answer:
        pt = decrypt_file(key1, key2, key3, file_path,flag)
        messagebox.showinfo("Success", "File decrypted and saved successfully")

    else:
            messagebox.showinfo("Success", "File decrypted successfully, but not saved.")



# Create the GUI
root = tk.Tk()
root.title("Triple DES Encryption")

frame = tk.Frame(root)
frame.pack()

choose_file_button = tk.Button(frame, text="Choose File", command=choose_file)
choose_file_button.pack()

root.mainloop()
