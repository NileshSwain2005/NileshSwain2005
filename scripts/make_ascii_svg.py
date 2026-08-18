from PIL import Image

# Brightness ramp: Bright (sparse/spaces) -> Dark (dense symbols)
RAMP = " .`:-=+*cs#%@"
WIDTH = 100  # Character columns (matches ~370px terminal rendering)
FILL_COLOR = "#8b949e"  # GitHub dark-mode secondary text color
BG_COLOR = "#0d1117"    # GitHub dark-mode background color

def make_ascii_svg(image_path="source-prepped.png", output_svg="nilesh-ascii.svg"):
    img = Image.open(image_path).convert("L")
    
    # Maintain aspect ratio for monospace font (~0.55 aspect ratio per char)
    aspect_ratio = img.height / img.width
    height = int(WIDTH * aspect_ratio * 0.55)
    img = img.resize((WIDTH, height), Image.Resampling.LANCZOS)
    
    pixels = img.load()
    rows = []
    
    for y in range(height):
        row_chars = []
        for x in range(WIDTH):
            val = pixels[x, y]
            # Map 0-255 brightness to RAMP index
            idx = int((val / 255) * (len(RAMP) - 1))
            char = RAMP[idx]
            # Escape HTML characters for SVG compatibility
            if char == "&": char = "&amp;"
            elif char == "<": char = "&lt;"
            elif char == ">": char = "&gt;"
            elif char == '"': char = "&quot;"
            elif char == " ": char = "&#160;"
            row_chars.append(char)
        rows.append("".join(row_chars))

    # SVG layout & typing parameters
    char_width = 3.7
    line_height = 7.0
    svg_width = 370
    svg_height = int(height * line_height) + 20
    
    row_delay = 0.04  # Seconds between each line
    row_duration = 0.35  # Time to wipe across a single line

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        '  <style>',
        f'    .bg {{ fill: {BG_COLOR}; }}',
        f'    .ascii {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 5.8px; fill: {FILL_COLOR}; white-space: pre; }}',
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" rx="6" />',
        '  <g class="ascii">'
    ]

    for idx, line in enumerate(rows):
        y_pos = 15 + (idx * line_height)
        start_time = idx * row_delay
        clip_id = f"clip-{idx}"
        
        # Add animated horizontal wipe per row
        svg_lines.append(f'    <clipPath id="{clip_id}">')
        svg_lines.append(f'      <rect x="0" y="{y_pos - line_height}" width="0" height="{line_height + 2}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{start_time:.2f}s" dur="{row_duration}s" fill="freeze" />')
        svg_lines.append(f'      </rect>')
        svg_lines.append(f'    </clipPath>')
        
        svg_lines.append(f'    <text x="10" y="{y_pos}" clip-path="url(#{clip_id})">{line}</text>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated {output_svg}")

if __name__ == "__main__":
    make_ascii_svg()