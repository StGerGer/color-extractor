from extract import Extractor
import argparse
from pathlib import Path
from string import Template
import shutil

class Replacer:

    template_path = ""
    output_path = ""

    pattern = Template("#[color$index]")

    def __init__(self, template, output):
        self.template_path = template
        self.output_path = output

    def replace(self, colors):
        print("Checking that the template file exists...")
        template = Path(self.template_path)
        output = Path(self.output_path)
        if(template.is_file()):
            print("Found template file.")
            if(output.is_file()):
                print("Config file already exists at {}. Creating backup.".format(self.output_path))
                shutil.copyfile(self.output_path, "{}.bak".format(self.output_path))
            with template.open("r") as template_file:
                with output.open("w") as output_file:
                    template_contents = template_file.read()
                    line_count = 0
                    for line in template_contents.split(sep="\n"):
                        color = 0
                        contains_color = False
                        while color < colors.get_size():
                            if self.pattern.substitute(index=(color+1)) in line:
                                contains_color = True
                                print("Found color {} on line {}, replacing with {}.".format(color+1, line_count, colors.get_color(color).get_hex()))
                                output_file.write("{}\n".format(line.replace(self.pattern.substitute(index=color+1), colors.get_color(color).get_hex())))
                            color += 1
                        
                        if not contains_color:
                            output_file.write("{}\n".format(line))
                        line_count += 1
                    
                    print("Done.")

        else:
            print("Template file does not exist.")
            exit(1)


if __name__ == "__main__":
    extractor = Extractor()

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", required=True, help="Path to image file")
    parser.add_argument("-c", "--colors", required=True, help="Number of colors to generate")
    parser.add_argument("-t", "--template", required=True, help="Path to config file template containing color variables")
    parser.add_argument("-o", "--output", required=True, help="Where to save resulting config file")
    args = parser.parse_args()

    replacer = Replacer(args.template, args.output)

    palette = extractor.get_colors(args.image, int(args.colors), use_logs=True)
    palette.sort("lightness")
    replacer.replace(palette)



