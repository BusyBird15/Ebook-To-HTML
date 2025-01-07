# Ebook-To-HTML
Converts a Project Gutenburg ebook into a fully-offline HTML page, usable even in Android HTML viewer.

## What it does
This Python code reads a URL of an ebook, downloads the data, fixes formatting (for mobile devices), loads images as base-64 data, and exports it to a file.

## Dependencies
Python libs `Beautiful Soup`, `requests`, `urllib`, `Pillow`, `BytesIO`, `base64`. Most of these come with python. However you will probably need to install the following:
```
> pip install Pillow
> pip install beautifulsoup4
> pip install requests
```

Check back periodically for updates.
