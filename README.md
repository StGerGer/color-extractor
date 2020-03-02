# Color Extractor

This program takes an image and returns a color scheme based on the image. Right now it is very faithful to the original image, but it is planned to add features that allow for easy creation of color schemes viable for IDEs, operating systems, and other UIs.

[Play with an online copy in Google Colab.](https://colab.research.google.com/drive/1d_6hCzxcBsMMVgJF-FzmSulwiX-RQRRU)
## Usage

### Generating a color scheme

To generate a basic color scheme:

```
python extract.py -i [image path] -c [color number]
```

You can also use the `-s` option to specify a sorting method for the resulting palette -- either lightness or prevalence in the image.

Run `python extract.py -h` for help.

### Generating config files

First, create a template file. To do this, copy your existing config file and replace the colors with the variables that the extractor recognizes. The extractor follows the form `#[color{number}]`, where `{number}` is replaced by a number in the range that you set. For example, here is what a template file might look like for some imaginary system.

```
foreground = #[color8]
background = #[color1]
accent = #[color3]
```

Note that the colors will be sorted by lightness from darkest to lightest. `#[color1]` will be replaced by the darkest color, and `#[color{n}]` will be replaced by the lightest.

I recommend saving this file using the form `*.template.[css, ini, etc.]`. For the above example, let's say it's `config.template.ini`.

Next, run `config_replacer.py`. You can run `python config_replacer.py -h` for help, or see below for the same message.

```
usage: config_replacer.py [-h] -i IMAGE -c COLORS -t TEMPLATE -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Path to image file
  -c COLORS, --colors COLORS
                        Number of colors to generate
  -t TEMPLATE, --template TEMPLATE
                        Path to config file template containing color variables
  -o OUTPUT, --output OUTPUT
                        Where to save resulting config file
```

Using the example above, our command might be `python config_replacer.py -i ~/Pictures/example.jpg -c 8 -t config.template.ini -o ~/.config/example/config.ini`.