import os
import argparse
import markdown
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
import pygments
from pygments.formatters import HtmlFormatter

def markdown_to_image(md_path, output_path=None, width=800, theme="light", direction="auto", font="default"):
    # Set default output path if not provided
    if output_path is None:
        output_path = os.path.splitext(md_path)[0] + ".png"
    
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Determine which pygments style to use based on theme
    pygments_style = 'monokai' if theme == 'dark' else 'default'
    
    # Convert markdown to HTML with syntax highlighting
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br'
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'linenums': False,
                'guess_lang': True,
                'use_pygments': True,
                'pygments_style': pygments_style
            }
        }
    )
    
    # Get pygments CSS for code highlighting
    pygments_css = HtmlFormatter(style=pygments_style).get_style_defs('.highlight')
    
    # Define font family based on selection
    font_import = ""
    if font == "vazirmatn":
        font_family = "'Vazirmatn', Arial, sans-serif"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "roboto":
        font_family = "'Roboto', Arial, sans-serif"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "opensans":
        font_family = "'Open Sans', Arial, sans-serif"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "dejavu":
        font_family = "'DejaVu Sans', Arial, sans-serif"
        font_import = '<link href="https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf" rel="stylesheet">'
    elif font == "dejavusansmono":
        font_family = "'DejaVu Sans Mono', monospace"
        font_import = '<link href="https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSansMono.ttf" rel="stylesheet">'
    elif font == "sourcecodepro":
        font_family = "'Source Code Pro', monospace"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "playfairdisplay":
        font_family = "'Playfair Display', serif"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "firacode":
        font_family = "'Fira Code', monospace"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">'
    elif font == "jetbrainsmononerd":
        font_family = "'JetBrains Mono', monospace"
        font_import = '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">'
    else:  # default
        font_family = "Arial, sans-serif"
    
    # Define CSS based on theme
    if theme == "dark":
        bg_color = "#1e1e1e"
        text_color = "#e0e0e0"
        code_bg = "#2d2d2d"
        border_color = "#505050"
        link_color = "#66d9ef"  # Light cyan - better visibility in dark mode
        link_visited = "#bb86fc"  # Light purple for visited links
    else:  # light theme
        bg_color = "#ffffff"
        text_color = "#333333"
        code_bg = "#f5f5f5"
        border_color = "#e0e0e0"
        link_color = "#0366d6"  # GitHub-style blue links
        link_visited = "#6f42c1"  # GitHub-style purple for visited
    
    # Determine direction
    dir_attr = ""
    if direction == "rtl":
        dir_attr = 'dir="rtl"'
    elif direction == "ltr":
        dir_attr = 'dir="ltr"'
    # For "auto", we don't set the direction explicitly
    
    # Create full HTML with CSS for styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {font_import}
        <style>
            body {{
                background-color: {bg_color};
                color: {text_color};
                font-family: {font_family};
                line-height: 1.6;
                padding: 20px;
                max-width: {width}px;
                margin: 0 auto;
                box-sizing: border-box;
                overflow-wrap: break-word;
            }}
            a {{
                color: {link_color};
                text-decoration: none;
                border-bottom: 1px solid {link_color}40; /* 40 adds transparency */
                transition: border-bottom 0.2s;
            }}
            a:visited {{
                color: {link_visited};
            }}
            a:hover {{
                border-bottom: 1px solid {link_color};
            }}
            pre {{
                direction: ltr;
                background-color: {code_bg};
                border-radius: 4px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                white-space: pre-wrap !important;
                word-wrap: break-word;
                overflow-wrap: break-word;
                max-width: 100%;
                overflow-x: auto;
            }}
            code {{
                display: inline;
                padding: 2px 5px;
                background-color: {code_bg};
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                word-break: break-all;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
            pre > code {{
                display: block;
                white-space: pre-wrap !important;
                background-color: transparent;
                padding: 0;
                border-radius: 0;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid {border_color};
                padding: 8px;
                text-align: start;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            blockquote {{
                border-left: 4px solid {border_color};
                margin-left: 0;
                padding-left: 15px;
                color: #777;
            }}
            [dir="rtl"] blockquote {{
                border-left: none;
                border-right: 4px solid {border_color};
                margin-right: 0;
                padding-right: 15px;
                padding-left: 0;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 24px;
                margin-bottom: 16px;
            }}
            ul, ol {{
                padding-left: 20px;
            }}
            [dir="rtl"] ul, [dir="rtl"] ol {{
                padding-left: 0;
                padding-right: 20px;
            }}
            
            /* Syntax highlighting CSS */
            {pygments_css}
            
            .highlight {{
                background-color: {code_bg} !important;
                border-radius: 4px;
                padding: 10px;
                margin: 15px 0;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body {dir_attr}>
        <div class="markdown-content">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', suffix='.html', delete=False) as f:
        f.write(full_html)
        temp_html_path = f.name
    
    # Use Playwright to take screenshot
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{temp_html_path}")
        
        # Wait for content to be rendered
        page.wait_for_selector('.markdown-content')
        
        # Get the exact content height for better screenshot
        content_height = page.evaluate('''() => {
            const body = document.querySelector('body');
            return body.getBoundingClientRect().height;
        }''')
        
        # Set viewport size
        page.set_viewport_size({"width": width, "height": int(content_height)})
        
        # Take screenshot
        page.screenshot(path=output_path)
        browser.close()
    
    # Remove temporary HTML file
    os.unlink(temp_html_path)
    
    return output_path

def detect_text_direction(text):
    """
    Attempt to detect if text is primarily RTL or LTR.
    Returns "rtl" or "ltr".
    """
    rtl_chars = 0
    ltr_chars = 0
    
    # Unicode ranges for RTL scripts
    rtl_ranges = [
        (0x0590, 0x05FF),  # Hebrew
        (0x0600, 0x06FF),  # Arabic
        (0x0700, 0x077F),  # Syriac
        (0x0750, 0x077F),  # Arabic Supplement
        (0x08A0, 0x08FF),  # Arabic Extended-A
        (0x0870, 0x089F),  # Arabic Extended-B
        (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
        (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
    ]
    
    for char in text:
        code = ord(char)
        is_rtl = False
        
        # Check if character is in RTL ranges
        for start, end in rtl_ranges:
            if start <= code <= end:
                rtl_chars += 1
                is_rtl = True
                break
                
        # Count as LTR if it's not RTL and it's a letter
        if not is_rtl and char.isalpha():
            ltr_chars += 1
    
    return "rtl" if rtl_chars > ltr_chars else "ltr"

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown file to image with RTL/LTR support")
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("-o", "--output", help="Path to output image file")
    parser.add_argument("-w", "--width", type=int, default=800, help="Width of the output image in pixels")
    parser.add_argument("-t", "--theme", choices=["light", "dark"], default="light", help="Theme for rendering")
    parser.add_argument("-d", "--direction", choices=["auto", "rtl", "ltr"], default="auto", 
                       help="Text direction (default: auto-detect)")
    parser.add_argument("-f", "--font", default="default", 
                      help="Font family to use (default, vazirmatn, roboto, opensans, dejavu, dejavusansmono, sourcecodepro, playfairdisplay, firacode, jetbrainsmononerd)")
    
    args = parser.parse_args()
    
    # Auto-detect direction if set to auto
    direction = args.direction
    if direction == "auto":
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        direction = detect_text_direction(content)
        print(f"Auto-detected text direction: {direction}")
    
    output_path = markdown_to_image(
        args.input_file, 
        args.output, 
        args.width, 
        args.theme,
        direction,
        args.font
    )
    
    print(f"Image created successfully: {output_path}")

if __name__ == "__main__":
    main()