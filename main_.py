from PIL import Image


def replace_least_significant_bit(num, bin_str, str_pos):
    if str_pos < len(bin_str):
        num = (int(num / 10) * 10) + int(bin_str[str_pos])
    return num


def hide_text_into_image(text, img_path):
    image = Image.open(img_path)
    pixel_map = image.load()

    width = image.size[0]
    height = image.size[1]

    # bin_text = ''.join(format(ord(i), '08b') for i in text)
    bin_text = ''.join(format(ord(i)).zfill(3) for i in text)
    # bin_text_len_bin = bin(len(bin_text)).replace("0b", "").zfill(6)
    bin_text_len_bin = str(len(bin_text)).zfill(3)

    str_pos = 0

    red, green, blue = pixel_map[0, 0]
    red = replace_least_significant_bit(red, bin_text_len_bin, 0)
    green = replace_least_significant_bit(green, bin_text_len_bin, 1)
    blue = replace_least_significant_bit(blue, bin_text_len_bin, 2)
    pixel_map[0, 0] = (red, green, blue)

    # print("Length mod: ", red, green, blue)

    for i in range(1, width):
        if str_pos > len(bin_text):
            break
        for j in range(1, height):
            if str_pos >= len(bin_text):
                break

            red, green, blue = pixel_map[i, j]

            # print("Original : ", red, green, blue)

            red = replace_least_significant_bit(red, bin_text, str_pos)
            green = replace_least_significant_bit(green, bin_text, str_pos + 1)
            blue = replace_least_significant_bit(blue, bin_text, str_pos + 2)
            str_pos += 3

            # print("Modified : ", red, green, blue)

            pixel_map[i, j] = (red, green, blue)

    # print("Binary text", bin_text)
    # print("Binary text length", bin_text_len_bin)

    # image.show()
    image.save("./output/out_.png")
    print("Successful")


hide_text_into_image(
    "Please do not read this line. Damn you!", "./assets/test.png")
