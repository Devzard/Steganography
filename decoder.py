from PIL import Image

ascii_str = ''


def extract_least_significant_bit(red, green, blue, str_pos, data_len):
    data_str = ''
    if str_pos < data_len:
        data_str += '{0}'.format(red % 10)
    if str_pos + 1 < data_len:
        data_str += '{0}'.format(green % 10)
    if str_pos + 2 < data_len:
        data_str += '{0}'.format(blue % 10)
    return data_str


def ascii_characters(ascii_str):
    text = ''
    for i in range(0, len(ascii_str), 3):
        temp_str = ascii_str[i:i+3]
        text += chr(int(temp_str))
    return text


def extract_text_from_image(img_path, ascii_str):
    image = Image.open(img_path)
    pixel_map = image.load()

    width = image.size[0]
    height = image.size[1]

    red, green, blue = pixel_map[0, 0]
    data_len = int('{r}{g}{b}'.format(r=red % 10, g=green % 10, b=blue % 10))

    str_pos = 0

    for i in range(1, width):
        if str_pos > data_len:
            break
        for j in range(1, height):
            if str_pos >= data_len:
                break

            red, green, blue = pixel_map[i, j]
            ascii_str += extract_least_significant_bit(
                red, green, blue, str_pos, data_len)
            str_pos += 3
    # print(ascii_str)
    text = ascii_characters(ascii_str)
    print(text)


extract_text_from_image("./output/out_.png", ascii_str)
