# 🗺️ Isle Map Updater

A powerful and user-friendly coordinate tracker for **The Isle** that automatically monitors your clipboard for coordinates and updates the [vulnona.com](https://vulnona.com/game/map/) map in real-time.

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 🚀 Features

- 📋 **Automatic Clipboard Monitoring** - Detects coordinates copied to clipboard
- 🌐 **Real-time Map Updates** - Automatically updates vulnova map with your position
- 🖥️ **User-friendly GUI** - Simple and intuitive interface
- 🔧 **Easy Setup** - Automated installation with batch scripts
- 🎯 **Coordinate Validation** - Ensures only valid Isle coordinates are processed
- 🔄 **Test Mode** - Built-in testing functionality
- ⚡ **Lightweight** - Minimal resource usage

## 📋 Requirements

- **Python 3.7+** (automatically checked during installation)
- **Google Chrome Browser**
- **Windows Operating System**
- **Internet Connection** (for map updates)

## 🛠️ Installation

### ⚠️ Windows SmartScreen Warning

When running `.bat` files, Windows SmartScreen may show a warning:
```
Windows protected your PC
Microsoft Defender SmartScreen prevented an unrecognized app from starting
```

**This is normal and safe!** To proceed:
1. Click **"More info"** 
2. Click **"Run anyway"**

The batch files only install Python packages and are completely safe.

### Option 1: Quick Setup (Recommended)

1. **Download** or clone this repository
2. **Run** `install.bat` (only once)
   ```batch
   install.bat
   ```
3. **Start** the application with `start.bat`
   ```batch
   start.bat
   ```

### Option 2: Manual Installation

1. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python isle_map_updater.py
   ```

## 📦 What Gets Installed

The `install.bat` script automatically:

- ✅ Checks for Python installation
- ✅ Installs pip if missing
- ✅ Installs required Python packages:
  - `selenium` - Web automation
  - `pyperclip` - Clipboard monitoring
  - `requests` - HTTP requests
  - `psutil` - System utilities
  - `webdriver-manager` - ChromeDriver management
- ✅ Downloads ChromeDriver v138 for compatibility

## 🎮 How to Use

1. **Start the Application:**
   - Double-click `start.bat` or run `python isle_map_updater.py`

2. **Setup Browser:**
   - Click "Setup Browser" to open vulnona map in Chrome
   - The map will open automatically and be ready for updates

3. **Track Coordinates:**
   - Copy coordinates in The Isle (format: `88,879.526, -288,696.11, 21,112.882`)
   - The application automatically detects and processes them
   - Your position updates on the vulnova map instantly

4. **Monitor Status:**
   - Watch the GUI for real-time status updates
   - Green indicators show successful coordinate updates
   - Error messages help troubleshoot any issues

## 📊 Supported Coordinate Formats

The application recognizes **The Isle's native coordinate format**:

```
88,879.526, -288,696.11, 21,112.882
```

✅ **No conversion needed** - Raw Isle coordinates are passed directly to vulnova.com  
✅ **Maximum accuracy** - Full precision maintained  
✅ **Simplified processing** - Direct copy-paste from The Isle

## 🗂️ Project Structure

```
the-isle/
├── 📄 README.md              # This file
├── 🐍 isle_map_updater.py    # Main application
├── 📋 requirements.txt       # Python dependencies
├── ⚙️ install.bat           # Automated installation
├── 🚀 start.bat             # Application launcher
```

## 🔧 Configuration

### Environment Variables

No special environment variables required. The application works out of the box.

### Browser Settings

- The application uses Chrome with specific settings for optimal performance
- No manual browser configuration needed
- ChromeDriver is managed automatically

## 🐛 Troubleshooting

### Common Issues

**Windows SmartScreen blocking .bat files:**
```
Windows protected your PC
Microsoft Defender SmartScreen prevented an unrecognized app from starting
```
**Solution:** Click "More info" → "Run anyway". The files are safe and only install Python packages.

**Python not found:**
```
❌ Python not found! Installing Python...
```
**Solution:** Download Python from [python.org](https://www.python.org/downloads/) and make sure to check "Add Python to PATH"

**ChromeDriver issues:**
```
❌ ChromeDriver installation failed!
```
**Solution:** Check your internet connection and firewall settings

**Map not updating:**
- Ensure Chrome browser is running
- Check that vulnona.com is accessible
- Verify coordinates are in the correct format

**Permission errors:**
- Run as Administrator if needed
- Check antivirus software isn't blocking the application

### Debug Mode

Run with verbose output:
```bash
python isle_map_updater.py --debug
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add comments for complex logic
- Include error handling
- Test with different coordinate formats

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **The Isle Community** - For inspiration and testing
- **vulnona.com** - For providing the excellent map service
- **Selenium Team** - For the web automation framework

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Create an issue on GitHub
3. Provide detailed error messages and logs

## 🔄 Version History

### v1.0.0
- Initial release
- Basic coordinate tracking
- Automated ChromeDriver setup
- GUI interface

---

**Made with ❤️ for The Isle community**

> ⭐ If this tool helps you, please consider giving it a star on GitHub!