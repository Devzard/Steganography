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


    def __init__(self, verbose, n_lasb, image):
        self.num_least_significant = n_lasb
        self.verbose = verbose
        self.image = Image.open(image)
        self.string = ''
        self.sstream = ''.join(format(ord(i), '08b') for i in self.string)
        self.count = 0
        self.modded_pixels = 0

    def manip_text(self, r, g, b):
        n_lsb = self.num_least_significant
        # Storing binary values of R, G, B values in a list
        binary_value = [int(bin(item).replace("0b", "")) for item in (r, g, b)]
        final = binary_value
        # Slicing binary value of the text to be stored in this cell
        i = 3 * n_lsb * self.count
        j = i + 3 * n_lsb
        text_stream = self.sstream[i:j]
        if self.verbose:
            print("A BIT STREAM: ", text_stream)
        for index, value in enumerate(binary_value):
            i = index * n_lsb
            j = i + n_lsb
            if self.verbose:
                print("Z BIT STREAM: ", text_stream[i:j])
            if(len(text_stream[i:j]) < n_lsb):
                final[index] = int(str(value), 2)
            else:
                # Using least significant bits for data storage
                modified_binary = int(value/(10 ** n_lsb))*(10 ** n_lsb) + \
                    int(text_stream[i:j])

                modified_decimal = int(str(modified_binary), 2)

                final[index] = modified_decimal

                self.modded_pixels += 1

        return final

    def hide(self, string, to_open):
        n_lsb = self.num_least_significant
        self.string = string
        self.sstream = ''.join(format(ord(i), '08b') for i in self.string)
        width = self.image.size[0]
        height = self.image.size[1]
        pixel_map = self.image.load()
        for i in range(width):
            for j in range(height):
                if self.count >= len(self.sstream) / (3*n_lsb):
                    break
                red, green, blue = pixel_map[i, j]
                if self.verbose:
                    print("ORIGINAL: ", red, green, blue)
                [red, green, blue] = self.manip_text(red, green, blue)
                if self.verbose:
                    print("MODIFIED: ", red, green, blue,  "\n")
                pixel_map[i, j] = (red, green, blue)
                self.count += 1
        print("{} pixels were coded.".format(self.modded_pixels))
        self.image.save('out.png')
        if(to_open):
            self.image.show()


parser = argparse.ArgumentParser(description='Hides information in images.')
parser.add_argument("--nlsb", type=int,
                    help="Specify number of bits to be modified per RGB value", default=2)
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
    n_lsb = args.nlsb
    S = Steganograph(verbose, n_lsb, path)
    S.hide(message, args.O)
