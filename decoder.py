from PIL import Image
import binascii

information = '' # coded data

def extract_information(red, green, blue):
    extracted_data = ''
    binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
    for digit in binary_value:
        extracted_data += str(digit % 100)
    return extracted_data

def extract_text(image_path, text_length, information):
    image = Image.open(image_path)
    pixel_map = image.load()

    width = image.size[0]
    height = image.size[1]

    for i in range(width):
        for j in range(height):
            # extract rgb
            red, green, blue = pixel_map[i, j]
            # convert each to binary and copy the last two bits to information string
            information += extract_information(red, green, blue)

    # divide the information string by 8 characters and covert it to corresponding ASCII character
    for binary_idx in range(len(information), 8):
        bin_str = information[binary_idx:binary_idx + 8]
        ascii_char = binascii.b2a_uu(bin_str)
        print(ascii_char)

extract_text('output/out.png', 48, information)