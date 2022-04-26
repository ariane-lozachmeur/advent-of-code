
class Layer():
    def __init__(self, array):
        self.pixels = array

    def __repr__(self):
        string = ""
        for row in self.pixels:
            string += row + '\n'
        return string   

    def get_pixel(self, x, y):
        return self.pixels[y][x]

    def count_pixels(self, pixel_value, ):
        layer = self.pixels
        c = 0
        for row in layer:
            c += row.count(pixel_value)
        return c 

class Image():
    def __init__(self, height, width, string):
        self.height = height
        self.width = width
        self.fill_layers(height, width, string)

    def __repr__(self):
        string = ""
        for i, layer in enumerate(self.layers):
            string += "Layer {}\n".format(i)
            string += str(layer) +'\n'

        return string

    def fill_layers(self, height, width, string):
        self.layers = []

        new_layer = []
        i = 0
        step = width

        while i <= len(string):
            # Once we filled one layer, start a new one
            if len(new_layer) == height:
                self.layers.append(Layer(new_layer))
                new_layer = []
            
            new_layer.append(string[i:i+step])
            
            i += step

    def find_min_zeroes(self):
        m = 10000
        min_layer = None
        for layer in self.layers:
            n_zeros = layer.count_pixels('0')
            print(n_zeros)
            if n_zeros < m:
                m = n_zeros
                min_layer = layer

        return min_layer

    def render_image(self):
        '''0 is black, 1 is white, and 2 is transparent.'''
        image = [[None for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            current_row = ''
            for x in range(self.width):
                current_pixel = '2'
                current_depth = 0
                while current_pixel == '2':
                    current_pixel = self.layers[current_depth].get_pixel(x, y)
                    current_depth += 1
                current_row += current_pixel
            image[y] = current_row
        self.image = Layer(image)

    def show_image(self):
        string = ""
        for row in self.image.pixels:
            string += row.replace('0', ' ').replace('1', '#') + '\n'
        print(string)  


def question1():
    with open('inputs/day08.txt', 'r') as handle:
        image_str = handle.readline().strip('\n')

    image = Image(6, 25, image_str)
    min_layer = image.find_min_zeroes()
    print(min_layer.count_pixels('1') * min_layer.count_pixels('2'))



if __name__=='__main__':
    with open('inputs/day08.txt', 'r') as handle:
        image_str = handle.readline().strip('\n')

    image = Image(6, 25, image_str)
    image.render_image()
    image.show_image()

