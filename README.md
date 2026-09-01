# Lost Items Community

> Find and report lost items in your community

**Website:** [https://lostitemscommunity.com](https://lostitemscommunity.com)

## 📋 Overview

Lost Items Community is a platform that helps community members report, track, and recover lost items. Whether you've lost something valuable or found an item that needs to be returned to its owner, this community-driven platform makes it easy to connect and help each other.

## 🚀 Features

- **Report Lost Items** - Document and share details about items you've lost
- **Post Found Items** - Help reunite found items with their owners
- **Community Engagement** - Connect with community members to assist in recovery
- **Item Tracking** - Keep track of lost and found items status
- **Rich UI** - Modern, responsive design
- **Performance Optimized** - All assets self-hosted, no third-party requests

## 🎨 Technology Stack

- **Frontend:** React 18 (UMD build) driven by `public/js/support.js`, a
  generated `dc-runtime` that renders the markup in `index.html`
- **Styling:** Inline styles in the generated markup — no CSS framework
- **Fonts:** Public Sans, IBM Plex Mono, Material Symbols Rounded — all
  self-hosted as woff2 under `public/fonts/`
- **No build tooling at runtime:** plain static files, no bundler, no CDN

### Design System

**Color Palette:**
- **Primary:** `#0B6BCB` - Main brand color
- **Ink:** `#16181F` - Headings and dark surfaces
- **Found / Success:** `#0F7B3D` - Green
- **Surface:** `#F6F7F8` - Light background
- **Muted text:** `#6B7280`

## 📱 Responsive Design

The layout adapts at runtime (the React runtime switches between desktop and
mobile trees) and is checked at 375px and 1440px:
- Mobile devices, including a slide-down nav menu
- Tablets
- Desktop browsers

Installable to a phone home screen via `manifest.webmanifest` and an
`apple-touch-icon`.

## ⚡ Performance Notes

- Every asset is served from this origin — no Google Fonts, no unpkg, no CDN
- `font-display: swap` on all faces
- Images shipped as WebP where possible

## 📦 Project Structure

```
.
├── Lost Items Community.html   # Source: self-extracting design bundle
├── build.py                    # Unpacks the bundle -> index.html + public/
├── index.html                  # GENERATED - do not edit by hand
├── manifest.webmanifest        # PWA manifest
├── favicon.ico
├── CNAME
└── public/
    ├── fonts/                  # woff2 (Public Sans, IBM Plex Mono, Material Symbols)
    ├── icons/                  # home-screen icons (180/192/512 + maskable)
    ├── images/                 # webp / png / svg artwork
    └── js/                     # react.js, react-dom.js, support.js
```

## 🛠️ Development

`index.html` and everything under `public/images`, `public/fonts` and
`public/js` are **generated**. Edit the design upstream, re-export
`Lost Items Community.html`, then regenerate:

```bash
python3 build.py
```

The script unpacks the bundle's asset manifest to disk, rewrites the template's
uuid references to real paths, and prunes any file under `public/` that the new
build no longer references. Hand edits to `index.html` are lost on the next run.

Preview locally:

```bash
python3 -m http.server 4321
```

## 🔄 Deployment

Hosted on GitHub Pages from the `main` branch, `/ (root)` publishing directory.
`CNAME` points the site at lostitemscommunity.com. No build step runs on
GitHub's side — the committed files are served as-is.

## 📝 License

This project is part of the Lost Items Community initiative.

## 🤝 Contributing

We welcome community contributions! To contribute:

1. Fork this repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📞 Support

For issues, feature requests, or questions, please visit the [LostItemsCommunity](https://github.com/ramanauday1561/LostItemsCommunity) repository.

---

**Made with ❤️ by the Lost Items Community**