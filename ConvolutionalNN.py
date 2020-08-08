import random
import simple_neural_network


class Layer:
    pad = ["full", "same", "shrink"]

    def __init__(self, kernel_size, pad="same", step=1, dilusion=0, activation_function=None):
        self.kernel_size, self.pad, self.step, self.dilusion = kernel_size, pad, step, dilusion,
        self.activation_function = activation_function if activation_function is not None else simple_neural_network.NeuralNetwork.relu
        self.weights = []
        self.input_shape = None
        self._num_neighbors = self.kernel_size[0] * self.kernel_size[1]  # number of pixels connected to the output
        self._expanded_size = self.kernel_size[0] + (self.kernel_size[0]-1)*self.dilusion, self.kernel_size[1] + (self.kernel_size[1]-1)*self.dilusion

    def get_output_shape(self):
        if self.input_shape is None:
            raise Exception("input size has not been set up yet")
        w, h = self.input_shape  # width and height of input
        dw, dh = self._expanded_size  # width and height of kernel
        if self.pad == "full":
            return (w+(dw-1)*2)// self.step, (h+(dh-1)*2)  // self.step
        if self.pad == "same":
            return self.input_shape
        if self.pad == "shrink":
            return (w - (dw - 1) * 2) // self.step, (h - (dh - 1) * 2)  // self.step
        return None

    def set_up_random_weights(self):
        if self.input_shape is None:
            raise Exception("input size has not been set up yet")
        w, h = self.get_output_shape()



    def propagate(self, input):
        if len(self.weights) < 1:
            raise Exception("Layer has not been set up yet")
        w, h = self.input_shape
        dw, dh = self._expanded_size
        start = 0 if self.pad == "full" else dw//2-1 if self.pad == "same" else dw//2
        outputs = []
        for i2, y in enumerate(range(start, h-start+1, step=self.step)):
            row = []
            for i1, x in enumerate(range(start, w-start+1, step=self.step)):
                kernel = self.get_kernel(input, (x,y))
                weights = self.weights[i2][i1]
                output = sum([k*w for k, w in zip(kernel, weights)])
                row.append(output)
            outputs.append(row)
        return outputs


    def get_kernel(self, input, pos):
        w, h = self.input_shape
        center_x, center_y = pos
        dx = self.kernel_size[0]//2
        dy = self.kernel_size[1]//2
        k = []
        for x in range(center_x-dx, center_x+dx+1, step=self.dilusion+1):
            for y in range(center_y-dy, center_y+dy+1, step=self.dilusion+1):
                if x < 0 or y < 0 or x >= w or y >= h:
                    if self.pad == "shrink":
                        raise Exception("pad found in shrink layer")
                    k.append(0)
                else:
                    k.append(input[y][x])
        return k




class CovolutionalNNs:
    def __init__(self, input_shape, layers):
        self.input_shape = input_shape
        self.layers = layers

    def setup(self):
        self.layers[0].input_shape = self.input_shape
        self.layers[0].set_up_random_weights()
        for i in range(len(self.layers), start=1):
            self.layers[i].input_shape = self.layers[i-1].get_output_shape()
            self.layers[i].set_up_random_weights()

    def propagate_layer(self, input, layer):
        pass

    def apply_filter(self, filter):
        pass

    def condence(self, image, step):
        pass

    def apply_layer(self, filters):
        return [self.apply_filter(thing) for thing in filters]



