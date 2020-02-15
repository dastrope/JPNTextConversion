from tesserocr import PyTessBaseAPI
from PIL import Image
import pykakasi

# JPNTextConversion
# Destin Astrope
#
# Initial attempt at using Tesseract OCR to scan an image of a block of Japanese text, then convert using pykakasi.
#
# Useful Tesseract notes:
# Can use (lang='jpn_vert') as an argument to the API to read Japanese text vertically instead of horizontally
# Can pipe more than one language together using (lang='eng+jpn') argument, order DOES affect accuracy
# Can also affect accuracy by giving the psm (page segmentation mode) to the API with these values format: psm=1
#
#     0 : OSD_ONLY Orientation and script detection only.
#     1 : AUTO_OSD Automatic page segmentation with orientation and script detection. (OSD)
#     2 : AUTO_ONLY Automatic page segmentation, but no OSD, or OCR.
#     3 : AUTO Fully automatic page segmentation, but no OSD. (default mode for tesserocr)
#     4 : SINGLE_COLUMN-Assume a single column of text of variable sizes.
#     5 : SINGLE_BLOCK_VERT_TEXT-Assume a single uniform block of vertically aligned text.
#     6 : SINGLE_BLOCK-Assume a single uniform block of text.
#     7 : SINGLE_LINE-Treat the image as a single text line.
#     8 : SINGLE_WORD-Treat the image as a single word.
#     9 : CIRCLE_WORD-Treat the image as a single word in a circle.
#     10 : SINGLE_CHAR-Treat the image as a single character.
#     11 : SPARSE_TEXT-Find as much text as possible in no particular order.
#     12 : SPARSE_TEXT_OSD-Sparse text with orientation and script detection
#     13 : RAW_LINE-Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
#
# Useful pykakasi notes:
# Input mode values: “J” (Japanese: kanji, hiragana and katakana), “H” (hiragana), “K” (katakana).
# Output mode values: “H” (hiragana), “K” (katakana), “a” (alphabet / rōmaji), “aF” (furigana in rōmaji).


# setup kakasi converter
kakasi = pykakasi.kakasi()
kakasi.setMode("J", "aF")
kakasi.setMode("K", "aF")
kakasi.setMode("H", "aF")
conv = kakasi.getConverter()

# set images
images = ['imgs/pg305.png']

with PyTessBaseAPI(lang='jpn+eng') as api:
    for img in images:
        # image preprocessing
        column = Image.open(img)
        gray = column.convert('L')
        blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
        # save as jpg to remove alpha channel
        blackwhite.save("imgs/temp_bw.jpg")
        img = "imgs/temp_bw.jpg"

        # OCR convert image to text
        api.SetImageFile(img)
        OCRText = api.GetUTF8Text()

        # convert text to desired type using kakasi converter
        convertedText = conv.do(OCRText)

        # display result
        print("Original Text")
        print(OCRText)
        print(api.AllWordConfidences())
        print("Converted Text")
        print(convertedText)

# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.
