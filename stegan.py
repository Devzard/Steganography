from PIL import Image
import argparse
import pathlib


class Steganograph:

    """
    Steganography is the practice of concealing a message within another
    message or a physical object. In computing/electronic contexts, a 
    computer file, message, image, or video is concealed within another
    file, message, image, or video.
    """

    num_least_significant = 2

    def __init__(self, verbose, image):
        self.verbose = verbose
        self.image = Image.open(image)
        self.string = ''
        self.sstream = ''.join(format(ord(i), '08b') for i in self.string)
        self.count = 0
        self.modded_pixels = 0

    def manip_text(self, r, g, b):
        # Storing binary values of R, G, B values in a list
        binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
        final = binary_value
        # Slicing binary value of the text to be stored in this cell
        text_stream = self.sstream[(6 * self.count):(6 * self.count+6)]
        if self.verbose:
            print("6 BIT STREAM: ", text_stream)
        for index, value in enumerate(binary_value):
            if self.verbose:
                print("2 BIT STREAM: ", text_stream[(index * 2):(index * 2+2)])
            if(len(text_stream[(index * 2):(index * 2+2)]) < 2):
                final[index] = int(str(value), 2)
            else:
                # Using two least significant bits for data storage
                modified_binary = int(value/100)*100 + \
                    int(text_stream[(index * 2):(index * 2+2)])

                modified_decimal = int(str(modified_binary), 2)

                final[index] = modified_decimal

                self.modded_pixels += 1

        return final

    def hide(self, string, to_open):
        self.string = string
        self.sstream = ''.join(format(ord(i), '08b') for i in self.string)
        width = self.image.size[0]
        height = self.image.size[1]
        pixel_map = self.image.load()
        for i in range(width):
            for j in range(height):
                if self.count >= len(self.sstream) / 6:
                    break
                red, green, blue = pixel_map[i, j]
                if self.verbose:
                    print("ORIGINAL: ", red, green, blue)
                [red, green, blue] = self.manip_text(red, green, blue)
                if self.verbose:
                    print("MODIFIED: ", red, green, blue,  "\n")
                pixel_map[i, j] = (red, green, blue)
                self.count += 1
        print("{} pixels were modded.".format(self.modded_pixels))
        self.image.save('output/out.png')
        if(to_open):
            self.image.show()


parser = argparse.ArgumentParser(description='Hides information in images.')
parser.add_argument("-H", "--hide", type=ascii,
                    help="Text to be hidden in photo.")
parser.add_argument("-E", "--extract", type=pathlib.Path,
                    help="Specify path to the photo from which data is to be extracted.")
parser.add_argument("path", type=pathlib.Path,
                    help="Specify path to the photo where information is to be hidden.")
parser.add_argument('-O', action='store_true', help="Open processed image.")
parser.add_argument('--verbose', action='store_true',
                    help="provides additional details as to what the program is doing.")
args = parser.parse_args()

if __name__ == "__main__":
    message = args.hide[1:-1]
    path = args.path
    verbose = args.verbose
    S = Steganograph(verbose, path)
    S.hide(message, args.O)
