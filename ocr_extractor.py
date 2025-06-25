import easyocr
import cv2
import os

# Initialize EasyOCR readers for Spanish and Arabic
reader_es = easyocr.Reader(['es'], gpu=False)
reader_ar = easyocr.Reader(['ar'], gpu=False)

def preprocess_image(image_path):
    """Load and convert the image to grayscale for better OCR accuracy."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def extract_text_with_confidence(image, reader, conf_threshold=0.5):
    """Extract text with a minimum confidence threshold."""
    results = reader.readtext(image, detail=1)  # detail=1 gives bbox, text, confidence
    filtered_texts = []
    for bbox, text, conf in results:
        if conf >= conf_threshold:
            filtered_texts.append(text.strip())
    return filtered_texts

def remove_duplicates(lines):
    """Remove duplicate lines while preserving order."""
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    return unique_lines

def filter_unwanted_words(lines, blacklist):
    """Remove any lines that contain unwanted words (case-insensitive match)."""
    return [line for line in lines if line.lower() not in blacklist]

def process_folder(input_folder, output_file):
    """Process all images in the folder and save clean OCR results."""
    blacklist = {"duolingo"}  # Add other unwanted words if needed

    with open(output_file, 'w', encoding='utf-8') as out:
        for fn in sorted(os.listdir(input_folder)):
            if fn.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Processing {fn}...")
                img_path = os.path.join(input_folder, fn)
                img = preprocess_image(img_path)

                spanish_lines = extract_text_with_confidence(img, reader_es)
                spanish_lines = remove_duplicates(spanish_lines)
                spanish_lines = filter_unwanted_words(spanish_lines, blacklist)

                arabic_lines = extract_text_with_confidence(img, reader_ar)
                arabic_lines = remove_duplicates(arabic_lines)
                arabic_lines = filter_unwanted_words(arabic_lines, blacklist)

                # Write results to file
                out.write(f"--- {fn} ---\n")
                for line in spanish_lines:
                    out.write(f"{line}\n")
                for line in arabic_lines:
                    out.write(f"{line}\n")
                out.write("\n")

    print(f"\n Done! Output saved to: {output_file}")

# ------------------------------------------
# ✅ CHANGE THESE TWO PATHS FOR YOUR SYSTEM
# Place your images in the folder below
input_folder = r"C:\Users\YOUR_USERNAME\Desktop\OCR\Images"

# This is where the output text will be saved
output_file = r"C:\Users\YOUR_USERNAME\Desktop\OCR\ocr_output_filtered.txt"
# ------------------------------------------

process_folder(input_folder, output_file)
