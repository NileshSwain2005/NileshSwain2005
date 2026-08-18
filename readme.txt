<your-username>/
├── .github/
│   └── workflows/
│       └── update-profile-art.yml   # GitHub Actions workflow for daily automated updates
├── data/
│   └── contributions.json          # Extracted contribution data and streak statistics
├── scripts/
│   ├── requirements.txt            # Python dependencies (requests, beautifulsoup4, pillow, etc.)
│   ├── prep_photo.py               # Pre-processes photo (background removal, OpenCV CLAHE contrast)
│   ├── make_ascii_svg.py           # Converts prepped photo to self-typing ASCII SVG
│   ├── make_info_card.py           # Generates the neofetch-style SVG card
│   ├── fetch_contributions.py      # Scrapes GitHub contribution calendar HTML fragment
│   └── render_heatmap_svg.py       # Generates the animated contribution heatmap SVG
├── avi-ascii.svg                   # Output: Generated ASCII portrait SVG
├── info-card.svg                   # Output: Generated Neofetch info card SVG
├── contrib-heatmap.svg             # Output: Generated contribution heatmap SVG
└── README.md                       # Main profile README placing the SVGs in a HTML table layout