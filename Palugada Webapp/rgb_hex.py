import numpy as np
from PIL import Image

class Rgb_hex:
    def __init__(self, img_path, jumlah_tampil):
        self.img_path = img_path
        self.img_data = Image.open(self.img_path)
        self.img_array = np.array(self.img_data)
        self.num_color = jumlah_tampil


    def get_colors(self, numcolors , resize=1000):
        # Resize image to speed up processing
        img = self.img_data
        img = img.copy()
        print(f"size awal : {img.size}")
        if (img.size[0] > 1000) or (img.size[1] > 10000):
            img.thumbnail((resize, resize))

        print(f"size akhir : {img.size}")
        # Reduce to palette
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

        # Find dominant colors
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        colors = list()
        for i in range(numcolors):
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index * 3:palette_index * 3 + 3]
            colors.append(tuple(dominant_color))

        return colors


    def rgb_to_hex(self, r, g, b):
        r = "{:X}".format(r)
        g = "{:X}".format(g)
        b = "{:X}".format(b)
        data_hex = [r, g, b]
        hex_akhir = []
        for x in data_hex:
            if len(x) < 2:
                x = f"0{x}"
            hex_akhir.append(x)

        return f"{hex_akhir[0]}{hex_akhir[1]}{hex_akhir[2]}"

    def img_to_hex(self):
        list_hex = []

        top_n_color = self.get_colors(numcolors= self.num_color)
        for data in top_n_color:
            list_hex.append(self.rgb_to_hex(data[0], data[1], data[2]))

        return list_hex