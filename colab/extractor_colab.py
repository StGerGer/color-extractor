#@title Color Scheme Generator {display-mode: "form"}

from sklearn.cluster import MiniBatchKMeans
import numpy as np
import urllib.request as urllib
import cv2
import operator
from google.colab.patches import cv2_imshow
from IPython.core.display import display, HTML
from palette import Palette, Color

#@markdown #### Options
#@markdown Direct link to the image.
image_url = 'https://images.unsplash.com/photo-1580118797218-2413f9d2e36b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60' #@param{type: "string"}
#@markdown Number of colors to generate.
colors =  16#@param{type: "number"}
#@markdown Size in pixels of each square in the palette shown.
color_chip_size = 80#@param{type: "number"}
#@markdown How to sort the palette. (Prevalence, by default, is ordered from lowest to highest.)
sort_palette_by = "lightness"#@param["prevalence", "lightness"]
#@markdown Should we reverse the palette order?
sort_palette_reverse = False#@param{type: "boolean"}

def generate_hex(color, bgr=False):
    string_color = "#"
    if bgr: color = color[::-1]
    for value in color:
        string_color += "{:02X}".format(int(value))
    return string_color

class Color:
    def __init__(self, hex, prevalence):
      self.hex = hex
      self.rgb = hex.strip('#')
      self.rgb = [int(self.rgb[i:i + 2], 16) for i in range(0, 6, 2)]
      self.prevalence = prevalence
      self.lightness = sum(self.rgb) / 3

    def set_hex(self, new_hex):
      self.hex = new_hex
      self.rgb = hex.strip('#')
      self.rgb = tuple(int(self.rgb[i:i + 2], 16) for i in range(0, 6, 2))
      self.lightness = sum(self.rgb) / 3

    def get_hex(self):
      return self.hex

    def get_lightness(self):
      return self.lightness
    
    def get_prevalence(self):
      return self.prevalence

    def get_color_chip(self):
      source = "<div style='display: flex; align-items: center; justify-content: center; margin: 10px; width: {}px; height: {}px; background-color: {}; color: {}'>{}</div> ".format(color_chip_size, color_chip_size, self.hex, "#000" if self.get_lightness() > 126 else "#FFF", self.hex)
      return source

class Palette:

    def __init__(self, colors):
      self.colors = colors

    def get_colors(self):
      return self.colors

    def add(self, color):
      self.colors.append(color)

    def get_palette_html(self):
      source = "<div style=' display: flex; flex-direction: row; flex-wrap: wrap;'>"
      for color in self.colors:
        source += color.get_color_chip()
      source += "</div>"
      return HTML(source)

    def sort(self, type):
      self.colors = sorted(self.colors, key=operator.attrgetter(type), reverse=sort_palette_reverse)

class Extractor:
    
    def get_colors(self, image_data, num, return_color_counts=False, return_image=False, use_logs=False):
        if num < 2:
          print("The image must have at least 2 colors.")
          return
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        (h, w) = image.shape[:2]
        # Convert color spaces
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clusters = MiniBatchKMeans(n_clusters = num)
        labels = clusters.fit_predict(image)
        res = clusters.cluster_centers_.astype("uint8")[labels]
        # To get the colors back to RGB, we must convert to an image and extract the colors
        res = res.reshape((h, w, 3))
        res = cv2.cvtColor(res, cv2.COLOR_LAB2BGR)
        if return_image:
            res_image = res

        res = res.reshape((h * w, 3))

        res_colors = []
        color_counts = []

        for color in res:
            string_color = generate_hex(color, bgr = True)
            if string_color not in res_colors:
                res_colors.append(string_color)
                color_counts.append(0)
            else:
                color_counts[res_colors.index(string_color)] += 1
            
        # Oh no
        if return_image:
            if return_color_counts:
                return res_colors, color_counts, res_image
            return res_colors, res_image
        if return_color_counts:
            return res_colors, color_counts
        return res_colors

    def get_image_data_from_url(self, url):
        req = urllib.urlopen(url)
        return np.asarray(bytearray(req.read()), dtype=np.uint8) 


if __name__ == "__main__":
    print("Running...")
    extractor = Extractor()
    colors, counts, image = extractor.get_colors(extractor.get_image_data_from_url(image_url), colors, return_color_counts=True, return_image=True, use_logs=True)
    (h, w) = image.shape[:2]
    if colors is not None:
      print("Resulting colors:")
      palette = Palette([])
      for i, color in enumerate(colors):
          palette.add(Color(color, counts[i]))
      palette.sort(sort_palette_by)
      display(palette.get_palette_html())

      cv2_imshow(image)
    