from PIL import Image

image = Image.open('assets/test.png')
pixel_map = image.load()

width = image.size[0]
height = image.size[1]

count = 0
text = "The WORLD'S FAVOURITE HAHAHA"
text_bin = ''.join(format(ord(i), '08b') for i in text)
print("LENGTH OF BIN: ", len(text_bin))

def manip_text(r, g, b, count):
    # Storing binary values of R, G, B values in a list
    binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
    final = binary_value
    # Slicing binary value of the text to be stored in this cell
    text_stream = text_bin[(6 * count):(6 * count+6)]
    print("6 BIT STREAM: ", text_stream)
    for index, value in enumerate(binary_value):
        print("2 BIT STREAM: ", text_stream[(index * 2):(index * 2+2)])
        if(len(text_stream[(index * 2):(index * 2+2)]) < 2):
            final[index] = int(str(value), 2)
        else:
            # Using two least significant bits for data storage
            modified_binary = int(value/100)*100 + \
                int(text_stream[(index * 2):(index * 2+2)])

            modified_decimal = int(str(modified_binary), 2)

            final[index] = modified_decimal

    return final

for i in range(width):
    for j in range(height):
        if count >= len(text_bin) / 6:
            break
        red, green, blue = pixel_map[i, j]
        print("ORIGINAL: ", red, green, blue)
        [red, green, blue] = manip_text(red, green, blue, count)
        print("MODIFIED: ", red, green, blue,  "\n")
        pixel_map[i, j] = (red, green, blue)
        count += 1

image.save('output/out.png')
image.show()
