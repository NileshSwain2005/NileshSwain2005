import os

def generate_info_card(output_path="info-card.svg"):
    width = 490
    height = 370
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_primary = "#c9d1d9"
    text_secondary = "#8b949e"
    
    c_blue = "#58a6ff"
    c_green = "#3fb950"
    c_purple = "#bc8cff"
    c_yellow = "#d29922"
    c_cyan = "#39c5bb"

    data = [
        ("OS", "GIFT Autonomous, BBSR (CSE '28)", c_blue),
        ("Host", "Bhanjanagar, Ganjam, Odisha", c_purple),
        ("Role", "Full-Stack Developer &amp; AI/ML Enthusiast", c_green),
        ("Stack", "MERN • Tailwind CSS • Python • C++", c_yellow),
        ("Focus", "RAG Systems • Computer Vision • Web3D", c_cyan),
        ("Projects", "Ntariksh • NirmaanConnect • Eco Hack '26", c_blue),
        ("Status", "Building, Learning &amp; Scaling 🚀", c_green),
    ]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .bg {{ fill: {bg_color}; }}
    .border {{ fill: none; stroke: {border_color}; stroke-width: 1.5; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .title {{ font-family: monospace; font-size: 11px; fill: {text_secondary}; }}
    .term-text {{ font-family: monospace; font-size: 11.5px; fill: {text_primary}; }}
    .label {{ font-weight: 600; }}
  </style>
  <rect width="{width}" height="{height}" rx="8" class="bg" />
  <rect width="{width}" height="{height}" rx="8" class="border" />
  
  <circle cx="16" cy="16" r="4" class="dot-red" />
  <circle cx="28" cy="16" r="4" class="dot-yellow" />
  <circle cx="40" cy="16" r="4" class="dot-green" />
  <text x="56" y="20" class="title">nilesh@github ~ neofetch</text>
  <line x1="0" y1="32" x2="{width}" y2="32" stroke="#21262d" stroke-width="1" />
  
  <g class="term-text" transform="translate(18, 52)">
    <text x="0" y="0" font-weight="bold" fill="{c_blue}">nilesh</text>
    <text x="42" y="0" fill="{text_secondary}">@</text>
    <text x="54" y="0" font-weight="bold" fill="{c_purple}">gift-bbsr</text>
    <text x="0" y="12" fill="{border_color}">------------------------------------------</text>
'''

    start_y = 32
    row_height = 24

    for idx, (label, val, color) in enumerate(data):
        y_pos = start_y + (idx * row_height)
        svg += f'    <text x="0" y="{y_pos}" class="label" fill="{color}">{label}:</text>\n'
        svg += f'    <text x="75" y="{y_pos}" fill="{text_primary}">{val}</text>\n'

    palette_y = start_y + (len(data) * row_height) + 14
    colors = [c_blue, c_green, c_purple, c_yellow, c_cyan, "#f85149", "#ffffff"]
    
    for idx, col in enumerate(colors):
        cx = idx * 20 + 6
        svg += f'    <circle cx="{cx}" cy="{palette_y}" r="6" fill="{col}" />\n'

    svg += '  </g>\n</svg>'

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Generated {output_path} successfully.")

if __name__ == "__main__":
    generate_info_card()