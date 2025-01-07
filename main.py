# You may need to install PIL Pillow library:
# > pip install Pillow

# the BeautifulSoup library:
# > pip install beautifulsoup4

# and the requests library:
# > pip install requests

# The software should guide you through the rest!



import base64, requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin

print("""
(1) Visit www.gutenberg.org and search for a book to read
(2) On the book info page, select 'Read online (web)'
(3) Copy the URL in the address bar and paste it here:
""")

bookurl = input("Book URL: ")
book = ""

def add_viewport_meta(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create the viewport meta tag
    viewport_meta = soup.new_tag('meta')
    viewport_meta.attrs['name'] = 'viewport'
    viewport_meta.attrs['content'] = 'width=device-width, initial-scale=1.0'
    
    # Insert the meta tag into the <head> section
    if soup.head:
        soup.head.append(viewport_meta)
    else:
        head_tag = soup.new_tag('head')
        head_tag.append(viewport_meta)
        soup.insert(0, head_tag)
    
    return str(soup)

def remove_body_styles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    style_tags = soup.find_all('style')
    for style in style_tags:
        style_content = style.string
        if style_content:
            modified_style_content = '\n'.join(
                line for line in style_content.split('\n') if not line.strip().startswith('body')
            )
            style.string.replace_with(modified_style_content)
    return str(soup)


def get_base64_image(url):
    absolute_url = urljoin(bookurl, url)
    response = requests.get(absolute_url)
    if response.status_code == 200:
        img_bytes = BytesIO(response.content).getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64
    return None

def replace_img_src_with_base64(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        img_url = img['src']
        img_base64 = get_base64_image(img_url)
        if img_base64:
            img['src'] = f'data:image/jpeg;base64,{img_base64}'
    
    return str(soup)

print("Fetching book...")
response = requests.get(bookurl)
if response.status_code == 200:
    book = response.text
    print("Book retreived successfully.\nConverting images...")
    try:
        updated_book = add_viewport_meta(remove_body_styles(replace_img_src_with_base64(book)))
        print("Images converted successfully.\nFixing formatting...")
        try:
            tsoup = BeautifulSoup(updated_book, 'html.parser')
            meta_tag = tsoup.find('meta', attrs={'property': 'og:title'})
            if meta_tag:
                booktitle = meta_tag['content']
            else:
                booktitle = "ebook"
            
            print(f"Formatting fixed successfully. Writing to {booktitle}.html...")
            
            with open(f"{booktitle}.html", "w+") as f:
                f.write(updated_book)
                    
            print(f"Book exported successfully. You may now transfer it to your device.")
            quit(0)
        except Exception as e:
            print(f'Failed to fix styling. Error: {e}.')
            quit(1)
    except Exception as e:
        print(f'Failed to replace the images. Error: {e}.')
        quit(1)
else:
    print(f'Failed to retrieve the book. Status code: {response.status_code}. Please check you entered the correct URL.')
    quit(1)
