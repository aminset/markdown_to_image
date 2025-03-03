# Markdown to Image Converter

A powerful Python utility that converts Markdown files to high-quality images with RTL/LTR language support and syntax highlighting.

## Features

- Convert any Markdown file to PNG image
- Support for RTL (Right-to-Left) and LTR (Left-to-Right) text directions
- Automatic language direction detection
- Light and dark themes
- Multiple font options including support for Arabic/Persian (Vazirmatn)
- Code syntax highlighting with Pygments
- Proper rendering of tables, links, lists, and blockquotes
- Customizable image width
- Line wrapping for long code blocks

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aminset/markdown-to-image.git
   cd markdown-to-image
   ```

2. Install the required packages:
   ```bash
   pip install markdown playwright pygments
   ```

3. Install the Playwright browser:
   ```bash
   python -m playwright install chromium
   ```

## Usage

Basic usage:

```bash
python md_to_image.py input.md -o output.png
```

With options:

```bash
python md_to_image.py input.md -o output.png -w 800 -t dark -d rtl -f vazirmatn
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `input_file` | Path to input Markdown file |
| `-o, --output` | Path to output image file (default: same as input with .png extension) |
| `-w, --width` | Width of the output image in pixels (default: 800) |
| `-t, --theme` | Theme for rendering: "light" or "dark" (default: light) |
| `-d, --direction` | Text direction: "auto", "rtl", or "ltr" (default: auto) |
| `-f, --font` | Font family to use (see Font Options below) |

## Font Options

- `default`: Arial, sans-serif
- `vazirmatn`: Vazirmatn - excellent for Persian/Arabic
- `roboto`: Roboto
- `opensans`: Open Sans
- `dejavu`: DejaVu Sans
- `dejavusansmono`: DejaVu Sans Mono - good for code
- `sourcecodepro`: Source Code Pro - great for code
- `playfairdisplay`: Playfair Display - elegant serif font
- `firacode`: Fira Code - programming font with ligatures
- `jetbrainsmononerd`: JetBrains Mono - developer-focused font

## Examples

Converting a Markdown file with auto-detection of text direction:
```bash
python md_to_image.py README.md
```

Creating a dark-themed image with custom width:
```bash
python md_to_image.py documentation.md -t dark -w 1000
```

Converting a Persian/Arabic document:
```bash
python md_to_image.py persian_doc.md -d rtl -f jetbrainsmononerd
```

Converting technical documentation with code:
```bash
python md_to_image.py code_doc.md -f sourcecodepro -w 900
```

## How It Works

The tool converts Markdown to HTML, applies styling based on the selected theme and font, and then uses Playwright to render the HTML to a PNG image. It handles RTL/LTR text directions and automatically detects the primary language direction if not specified.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.