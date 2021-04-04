from PIL import Image

image = Image.open('assets/test.png')
pixel_map = image.load()

width = image.size[0]
height = image.size[1]

count = 0
text = "python"
text_bin = ''.join(format(ord(i), '08b') for i in text)


def manip_text(r, g, b, count):
    binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
    # final = [0, 0, 0]
    i = 6 * count
    j = i + 6
    text_input = text_bin[i:j]
    final = [int(str(int(value/100)*100 + int(text_input[(index * 2):(index * 2+2)])), 2)
             for index, value in enumerate(binary_value)]
    # for index, value in enumerate(binary_value):
    #     final[index] = int(
    #         str(int(value/100)*100 + int(text_input[(index * 2):(index * 2+2)])), 2)
    return final


for i in range(width):
    if count >= len(text_bin) / 6:
        break
    for j in range(height):
        red, green, blue = pixel_map[i, j]
        if count >= len(text_bin) / 6:
            break
        print("OR: ", red, green, blue)
        [red, green, blue] = manip_text(red, green, blue, count)
        print(red, green, blue)
        pixel_map[i, j] = (red, green, blue)
        count += 1

image.save('output/out.png')
image.show()
