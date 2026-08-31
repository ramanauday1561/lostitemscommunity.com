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
- **Rich UI** - Modern, responsive design using Tailwind CSS
- **Performance Optimized** - Fast loading with preloaded critical resources

## 🎨 Technology Stack

- **Frontend Framework:** React (JavaScript)
- **Styling:** Tailwind CSS (with custom design tokens)
- **Fonts:** IBM Plex Sans, IBM Plex Mono, Google Material Symbols
- **Performance:** Optimized with resource hints and preloading strategies

### Design System

**Color Palette:**
- **Primary:** `#005dac` - Main brand color
- **Surface:** `#fcf8ff` - Light background
- **Lost Items:** `#D32F2F` - Danger/Red
- **Found Items:** `#2E7D32` - Success/Green
- **Pending Status:** `#ED6C02` - Warning/Orange

## 📱 Responsive Design

The platform is fully responsive and optimized for:
- Mobile devices (with viewport-fit=cover for notched displays)
- Tablets
- Desktop browsers

## ⚡ Performance Optimizations

- DNS prefetching for external font services
- Resource preloading for critical images (WebP format)
- Font preloading with `font-display: swap` for better performance
- Content Security Policy and meta tags for security

## 🔄 Deployment

This repository is configured for hosting on GitHub Pages. The `index.html` file serves as the entry point for the static website.

### Setting Up GitHub Pages

1. Go to repository settings
2. Enable GitHub Pages
3. Select `main` branch as source
4. Choose `/ (root)` as the publishing directory

## 📦 Project Structure

```
.
├── index.html          # Main HTML entry point
├── README.md           # This file
├── images/             # Static images
│   ├── Background2.webp
│   └── HomePage1.webp
├── favicon.ico         # Website favicon
├── logo192.png         # Apple touch icon
└── manifest.json       # PWA manifest file
```

## 🛠️ Development

If you're working with the original React source code, refer to the [LostItemsCommunity](https://github.com/ramanauday1561/LostItemsCommunity) repository.

### Build Process
The React application is built using `npm run build`, which generates the optimized static files that are then deployed via GitHub Pages.

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