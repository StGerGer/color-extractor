# import the necessary packages
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2
from palette import Palette, Color

def generate_hex(color, bgr=False):
    string_color = "#"
    if bgr: color = color[::-1]
    for value in color:
        string_color += "{:02X}".format(int(value))
    return string_color

class Extractor:

    scheme_cache = None
    
    def get_colors(self, image_path, num, return_color_counts=False, return_image=False, use_logs=False):
        if num < 2:
          print("The image must have at least 2 colors.")
          return
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
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

        palette = Palette()
        for i, color in enumerate(res_colors):
            palette.add(Color(color, color_counts[i]))

        self.scheme_cache = palette
            
        # Oh no
        if return_image:
            if return_color_counts:
                return palette, color_counts, res_image
            return palette, res_image
        if return_color_counts:
            return palette, color_counts
        return palette

    def get_image_data_from_url(self, url):
        req = urllib.urlopen(url)
        return np.asarray(bytearray(req.read()), dtype=np.uint8) 
    
    def get_cached_colors(self):
        return self.scheme_cache

if __name__ == "__main__":
    print("Running...")
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    ap.add_argument("-c", "--colors", required = True, type = int, help = "Number of colors")
    ap.add_argument("-s", "--sort", required=False, default="lightness", help="How to sort the resulting palette. [lightness, prevalence]")
    args = ap.parse_args()
    extractor = Extractor()
    palette, counts, image = extractor.get_colors(args.image, args.colors, return_color_counts=True, return_image=True, use_logs=True)
    (h, w) = image.shape[:2]
    print("Resulting colors:")

    #   palette = Palette()
    #   for i, color in enumerate(colors):
    #       palette.add(Color(color, counts[i]))
    palette.sort(args.sort)
    print(palette.get_palette_plain())

    cv2.imshow("Image crushed to {} colors".format(args.colors), image)
    cv2.waitKey(5000)