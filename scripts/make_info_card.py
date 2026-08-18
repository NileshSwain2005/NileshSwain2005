import os

def generate_info_card(output_path="info-card.svg"):
    # Card Configuration
    width = 490
    height = 370
    bg_color = "#0d1117"        # GitHub dark mode background
    border_color = "#30363d"    # Terminal border
    text_primary = "#c9d1d9"     # Default text color
    text_secondary = "#8b949e"   # Muted labels
    
    # Theme Accent Colors (Neofetch palette)
    c_blue = "#58a6ff"
    c_green = "#3fb950"
    c_purple = "#bc8cff"
    c_yellow = "#d29922"
    c_cyan = "#39c5bb"

    # Profile Data Rows
    data = [
        ("OS", "GIFT Autonomous, BBSR (CSE '28)", c_blue),
        ("Host", "Bhanjanagar, Ganjam, Odisha", c_purple),
        ("Role", "Full-Stack Developer & AI/ML Enthusiast", c_green),
        ("Stack", "MERN • Tailwind CSS • Python • C++", c_yellow),
        ("Focus", "RAG Systems • Computer Vision • Web3D", c_cyan),
        ("Projects", "Ntariksh • NirmaanConnect • Eco Hack '26", c_blue),
        ("Status", "Building, Learning & Scaling 🚀", c_green),
    ]

    # Check for static mode environment variable (useful for static local previews)
    is_static = os.getenv("STATIC", "0") == "1"

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <style>',
        f'    .bg {{ fill: {bg_color}; rx: 8px; }}',
        f'    .border {{ fill: none; stroke: {border_color}; stroke-width: 1.5; rx: 8px; }}',
        '    .dot-red { fill: #ff5f56; }',
        '    .dot-yellow { fill: #ffbd2e; }',
        '    .dot-green { fill: #27c93f; }',
        f'    .title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: {text_secondary}; }}',
        f'    .term-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11.5px; fill: {text_primary}; }}',
        f'    .label {{ fill: {text_secondary}; font-weight: 600; }}',
        '    @keyframes fadeInSlide {',
        '      from { opacity: 0; transform: translateY(6px); }',
        '      to { opacity: 1; transform: translateY(0); }',
        '    }',
        '    .animated-row {',
        '      opacity: ' + ('1' if is_static else '0') + ';',
        '      animation: ' + ('none' if is_static else 'fadeInSlide 0.4s ease-out forwards') + ';',
        '    }',
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" />',
        f'  <rect width="100%" height="100%" class="border" />',
        '  ',
        '  <!-- Terminal Top Window Controls -->',
        '  <circle cx="16" cy="16" r="4" class="dot-red" />',
        '  <circle cx="28" cy="16" r="4" class="dot-yellow" />',
        '  <circle cx="40" cy="16" r="4" class="dot-green" />',
        '  <text x="56" y="19" class="title">nilesh@github ~ neofetch</text>',
        '  <line x1="0" y1="32" x2="100%" y2="32" stroke="#21262d" stroke-width="1" />',
        '  ',
        '  <!-- Main Terminal Content -->',
        '  <g class="term-text" transform="translate(18, 52)">'
    ]

    # Add Header Username Title
    svg_lines.append('    <g class="animated-row" style="animation-delay: 0.05s;">')
    svg_lines.append(f'      <text x="0" y="0" font-weight="bold" fill="{c_blue}">nilesh</text>')
    svg_lines.append(f'      <text x="42" y="0" fill="{text_secondary}">@</text>')
    svg_lines.append(f'      <text x="54" y="0" font-weight="bold" fill="{c_purple}">gift-bbsr</text>')
    svg_lines.append('    </g>')
    
    svg_lines.append('    <g class="animated-row" style="animation-delay: 0.10s;">')
    svg_lines.append(f'      <text x="0" y="12" fill="{border_color}">------------------------------------------</text>')
    svg_lines.append('    </g>')

    # Generate Data Rows with Staggered Delays
    start_y = 32
    row_height = 24

    for idx, (label, val, color) in enumerate(data):
        y_pos = start_y + (idx * row_height)
        delay = 0.15 + (idx * 0.06)
        
        svg_lines.append(f'    <g class="animated-row" style="animation-delay: {delay:.2f}s;">')
        svg_lines.append(f'      <text x="0" y="{y_pos}" class="label" fill="{color}">{label.ljust(9)}:</text>')
        svg_lines.append(f'      <text x="80" y="{y_pos}">{val}</text>')
        svg_lines.append('    </g>')

    # Add Color Palette Circles at Bottom
    palette_y = start_y + (len(data) * row_height) + 14
    palette_delay = 0.15 + (len(data) * 0.06) + 0.05
    colors = [c_blue, c_green, c_purple, c_yellow, c_cyan, "#f85149", "#ffffff"]
    
    svg_lines.append(f'    <g class="animated-row" style="animation-delay: {palette_delay:.2f}s;">')
    for idx, col in enumerate(colors):
        cx = idx * 20 + 6
        svg_lines.append(f'      <circle cx="{cx}" cy="{palette_y}" r="6" fill="{col}" />')
    svg_lines.append('    </g>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    # Write output SVG
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_info_card()