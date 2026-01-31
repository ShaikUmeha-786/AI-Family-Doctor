from PIL import Image
import pytesseract

# Tell Python where Tesseract is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open test image
img = Image.open("sample.png")

# Extract text
text = pytesseract.image_to_string(img)

print("------ OCR OUTPUT ------")
print(text)
