from PIL import Image
import numpy as np

def get_threshold_ascii(n, symbols, len):
    """
    Given a number, it returns its corresponding ascii character. Symbols on the left are "whiter" than symbols on the
    right, which are "blacker".

    :param n: Number that will be compared, from [0, 255]
    :param symbols: String that will be used as "black intensity" chart
    :return: Return symbol from symbols depending on "black intensity" of n
    """
    for i, symbol in enumerate(symbols):
        if ((i + 1) / len) * 255 >= n:
            return symbol

def image_to_ascii(image_path, output="output", complex=False, resize=True):
    """
    Given an image, it creates an ASCII representation of itself by working with greyscales.

    :param image_path: Path name of the image
    :param output: Name of the .txt output
    :param complex: If True, uses complex symbols to codify the image. Looks kinda ugly
    :param resize: If True, resizes to 256, 256 because otherwise editors can't prettily load that much characters
    :return: None, creates a .txt document
    """
    print("Beginning process...")
    if complex:
        symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " # Looks ugly
    else:
        symbols = " .:-=+*#%@"[::-1] # Looks fine

    threshold_ascii = np.vectorize(get_threshold_ascii)
    image = Image.open(image_path).convert("RGB") # In case of Alpha
    if resize:
        # Resize because otherwise, text editors can't process so much symbols per line and look messy
        w, h = image.size
        if w > 512 or h > 512: # The image is bigger, we will scale it down.
            if w >= h:
                image = image.resize((512, int(512 * (h / w))))
            else:
                image = image.resize((int(512 * (w / h)), 512))
    data_color = np.asarray(image)

    raw_data_monochrome = data_color.sum(axis=2)/3 # Get's greyscale values in a 2D array
    data_monochrome = raw_data_monochrome.astype("int32")
    threshold_data = threshold_ascii(data_monochrome, symbols, len(symbols))
    np.savetxt(f"{output}.txt", threshold_data, fmt="%s") # Saves array into text

    print("Text saved!\n\n")

if __name__ == "__main__":
    image_url = r"test_media/evangelion.jpg"
    image_to_ascii(image_url, resize=True)