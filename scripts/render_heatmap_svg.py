import json
import os
from datetime import datetime

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Data file '{json_path}' not found. Run scripts/fetch_contributions.py first.")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    # Grid Dimensions & Colors
    box_size = 10
    box_gap = 3
    stride = box_size + box_gap
    start_x = 45
    start_y = 55

    width = 860
    height = 200
    bg_color = "#0d1117"
    border_color = "#30363d"
    text_primary = "#c9d1d9"
    text_muted = "#8b949e"

    # Contribution Level Colors (GitHub Dark Theme)
    level_colors = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353"
    }

    # Process Calendar Grid
    # Group days into weeks (columns)
    weeks = []
    current_week = []

    for idx, day in enumerate(days):
        dt = datetime.strptime(day["date"], "%Y-%m-%d")
        day_of_week = dt.weekday()  # Mon=0, Sun=6 (Convert to Sun=0 for standard grid)
        grid_row = (day_of_week + 1) % 7  # 0=Sun, 1=Mon, ..., 6=Sat

        # If it's Sunday and we already have items, start a new week
        if grid_row == 0 and current_week:
            weeks.append(current_week)
            current_week = []

        current_week.append({
            "date": day["date"],
            "count": day["count"],
            "level": day["level"],
            "row": grid_row
        })

    if current_week:
        weeks.append(current_week)

    # Build SVG content
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <style>',
        f'    .bg {{ fill: {bg_color}; rx: 8px; }}',
        f'    .border {{ fill: none; stroke: {border_color}; stroke-width: 1.5; rx: 8px; }}',
        f'    .text-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 13px; font-weight: bold; fill: {text_primary}; }}',
        f'    .text-stat {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: {text_muted}; }}',
        f'    .text-stat-val {{ font-weight: bold; fill: #58a6ff; }}',
        f'    .label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; fill: {text_muted}; }}',
        '    .day-rect { rx: 2px; ry: 2px; transition: all 0.2s ease; }',
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" />',
        f'  <rect width="100%" height="100%" class="border" />',
        '  ',
        '  <!-- Header Statistics -->',
        f'  <text x="20" y="30" class="text-title">Contribution Activity</text>',
        '  <g class="text-stat">',
        f'    <text x="420" y="30">Total: <tspan class="text-stat-val">{total_contribs}</tspan></text>',
        f'    <text x="560" y="30">Current Streak: <tspan class="text-stat-val">{current_streak} days</tspan></text>',
        f'    <text x="710" y="30">Longest: <tspan class="text-stat-val">{longest_streak} days</tspan></text>',
        '  </g>',
        '  ',
        '  <!-- Day Labels (Mon, Wed, Fri) -->',
        f'  <text x="20" y="{start_y + (1 * stride) + 8}" class="label">Mon</text>',
        f'  <text x="20" y="{start_y + (3 * stride) + 8}" class="label">Wed</text>',
        f'  <text x="20" y="{start_y + (5 * stride) + 8}" class="label">Fri</text>',
        '  '
    ]

    # Month Labels
    last_month = None
    for w_idx, week in enumerate(weeks):
        if not week:
            continue
        first_day_of_week = datetime.strptime(week[0]["date"], "%Y-%m-%d")
        month_name = first_day_of_week.strftime("%b")
        if month_name != last_month and w_idx < len(weeks) - 1:
            month_x = start_x + (w_idx * stride)
            svg.append(f'  <text x="{month_x}" y="{start_y - 10}" class="label">{month_name}</text>')
            last_month = month_name

    # Heatmap Grid Rectangles
    svg.append('  <!-- Heatmap Grid -->')
    for w_idx, week in enumerate(weeks):
        x = start_x + (w_idx * stride)
        for day in week:
            y = start_y + (day["row"] * stride)
            color = level_colors.get(day["level"], level_colors[0])
            title_text = f"{day['count']} contribution{'s' if day['count'] != 1 else ''} on {day['date']}"
            
            svg.append(f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" class="day-rect"><title>{title_text}</title></rect>')

    # Legend at Bottom Right
    legend_x = width - 180
    legend_y = height - 20
    svg.append('  <!-- Legend -->')
    svg.append(f'  <text x="{legend_x - 30}" y="{legend_y + 9}" class="label">Less</text>')
    for lvl, col in level_colors.items():
        lx = legend_x + (lvl * (box_size + 3))
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="{box_size}" height="{box_size}" fill="{col}" class="day-rect" />')
    svg.append(f'  <text x="{legend_x + (5 * (box_size + 3)) + 5}" y="{legend_y + 9}" class="label">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    render_heatmap()