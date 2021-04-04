from PIL import Image

image = Image.open('output/out.png')
pixel_map = image.load()

width = image.size[0]
height = image.size[1]

count = 0
text = "python"
text_bin = ''.join(format(ord(i), '08b') for i in text)

yay = ""


def manip_text(r, g, b, count, yay):
    binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
    for value in binary_value:
        yay += str(binary_value % 100)


for i in range(width):
    if count >= len(text_bin) / 6:
        break
    for j in range(height):
        red, green, blue = pixel_map[i, j]
        if count >= len(text_bin) / 6:
            break
        print("OR: ", red, green, blue)
        [red, green, blue] = manip_text(red, green, blue, count, yay)
        print(red, green, blue)
        pixel_map[i, j] = (red, green, blue)
        count += 1

print(yay)
