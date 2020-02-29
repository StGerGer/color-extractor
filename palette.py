import operator

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

    def __init__(self, colors=[]):
      self.colors = colors

    def get_colors(self):
      return self.colors

    def get_color(self, index):
      return self.colors[index]

    def get_size(self):
      return len(self.colors)

    def add(self, color):
      self.colors.append(color)

    def get_palette_html(self):
      source = "<div style=' display: flex; flex-direction: row; flex-wrap: wrap;'>"
      for color in self.colors:
        source += color.get_color_chip()
      source += "</div>"
      return HTML(source)

    def get_palette_plain(self):
        res = ""
        for color in self.colors:
            res += "{}\n".format(color.get_hex())

        return res

    def sort(self, type, reverse=False):
      self.colors = sorted(self.colors, key=operator.attrgetter(type), reverse=reverse)