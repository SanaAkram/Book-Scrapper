import os
import requests
import tempfile
import pdfplumber
from PIL import Image

def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    else:
        print("Failed to download the file.")
        return None


def extract_text_and_images(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text_content = ""
        images = []

        for page in pdf.pages:
            text_content += page.extract_text()
            images.extend(page.images)

        return text_content, images


def save_to_document(text_content, images, output_path):
    with open(output_path, "w") as doc_file:
        doc_file.write(text_content)
        doc_file.write("\n\n")

        for idx, img_data in enumerate(images):
            img = Image.open(img_data["src"])
            img_path = f"{output_path[:-4]}_{idx}.png"  # Assuming PNG format
            img.save(img_path)
            doc_file.write(f"Image {idx + 1}: {img_path}\n\n")


def main(url, output_path):
    pdf_file = download_file(url)
    if pdf_file:
        text_content, images = extract_text_and_images(pdf_file)
        save_to_document(text_content, images, output_path)
        print(f"Data saved to {output_path}")
        os.remove(pdf_file)  # Remove the temporary PDF file


if __name__ == "__main__":
    url = input("Enter the URL of the PDF file: ")
    output_path = 'books/example.txt'
    main(url, output_path)
