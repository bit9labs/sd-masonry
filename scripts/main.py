import gradio as gr
import os
import sqlite3
from PIL import Image

from modules import script_callbacks
from modules.shared import opts
from modules.scripts import basedir
from modules.ui_components import ToolButton

image_ext_list = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".svg"]
dir_extension = basedir()
dir_path = opts.outdir_samples or opts.outdir_txt2img_samples
items_per_page = 25
total_images = 0

# Make a connection with our sqlite database, should be created in install.py
def get_conn():
    return sqlite3.connect(os.path.join(dir_extension, "sqlite.db"))

def set_dir_path(path):
    global dir_path
    dir_path = path

def traverse_all_files(path):
    global total_images

    # get our connection
    conn = get_conn()
    c = conn.cursor()

    # Clear the table before inserting new data
    c.execute("DELETE FROM images")

    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in image_ext_list:
                image_path = os.path.join(root, filename)
                try:
                    image = Image.open(image_path)
                    width, height = image.size
                    image.close()
                    
                    # Save the image details to the database
                    c.execute("INSERT INTO images (path, width, height) VALUES (?, ?, ?)",
                              (image_path, width, height))
                    
                except (IOError, SyntaxError) as e:
                    # Skip the image if it cannot be opened or has syntax errors
                    print(f"Skipped {image_path}: {str(e)}")

    # refresh the total images
    c.execute("SELECT COUNT(*) FROM images")
    total_images = c.fetchone()[0]

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def set_items_per_page(count):
    global items_per_page 
    items_per_page = int(count) if count != "All" else None

def total_pages():
    global items_per_page
    global total_images

    if items_per_page == None:
        return 1
    
    return (total_images + int(items_per_page) - 1) // int(items_per_page)

def get_page(page_index):
    global items_per_page
    html = ''
    conn = get_conn()
    c = conn.cursor()

    if page_index < 1 or page_index > total_pages():
        page_index = min(total_pages(), max(1, page_index))
    else:
        if items_per_page != None:
            c.execute("SELECT path, width, height FROM images LIMIT ? OFFSET ?",
                      (items_per_page, (page_index - 1) * items_per_page))
        else:
            c.execute("SELECT path, width, height FROM images")

        images = c.fetchall()

        for image, width, height in images:
            html += '<a href="/file={}" class="masonry-item" itemprop="contentUrl" data-pswp-width="{}" data-pswp-height="{}">'.format(image, width, height)
            html += '<img src="/file={}" class="object-cover w-96" itemprop="thumbnail" alt="" />'.format(image)
            html += '</a>'

    # Close the connection
    conn.close()

    return html, page_index

def first_page():
    return 1
def prev_page(page_index):
    return max(page_index - 1, 1)
def next_page(page_index):
    return min(page_index + 1, total_pages())
def last_page():
    return total_pages()

def refresh_images(page_index):
    traverse_all_files(dir_path)
    return get_page(page_index)

def on_ui_tabs():
    
    with gr.Blocks(analytics_enabled=False) as image_browser:
        #get the first page but also load the images
        html = refresh_images(1)
        
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    first_page_btn = ToolButton('\u23EE')
                    prev_page_btn = ToolButton('\u23EA')
                    page = gr.Number(value=1, precision=0, visible=False, show_label=False)
                    next_page_btn = ToolButton('\u23E9')
                    last_page_btn = ToolButton('\u23ED')
            with gr.Column(scale=1):
                page_html = gr.HTML("1/" + str(total_pages()))
            with gr.Column(scale=2):
                with gr.Row():
                    source = gr.Dropdown(choices=["t2i","i2i"], value="t2i", show_label=False)
                    items_count = gr.Dropdown(choices=["All", "25", "50", "100", "250", "500", "1000"], value="25", show_label=False)
                    refresh = gr.Button('Refresh', size='sm')
        with gr.Row() as main_panel:
            with gr.Column():
                gr.HTML('<div class="spinner"></div>', elem_id="loading-wheel")
                masonry_gallery = gr.HTML(html, elem_classes="masonry-container")

        page_change = page.change(
            fn=get_page,
            inputs=[page],
            outputs=[masonry_gallery, page]
        ).then(
            fn=lambda page_index: str(page_index) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html],
            _js="(p) => {debounceInitHandler(); return p;}"
        )

        first_page_btn.click(
            fn=first_page,
            outputs=[page]
        )
        prev_page_btn.click(
            fn=prev_page,
            inputs=[page],
            outputs=[page]
        )
        next_page_btn.click(
            fn=next_page,
            inputs=[page],
            outputs=[page]
        )       
        last_page_btn.click(
            fn=last_page,
            inputs=[],
            outputs=[page]
        )

        items_count.change(
            fn=set_items_per_page,
            inputs=[items_count]
        ).then(
            lambda: 1,
            outputs=[page]
        ).then(
            fn=get_page,
            inputs=[page],
            outputs=[masonry_gallery, page],
            cancels=[page_change]
        ).then(
            fn=None,
            _js="() => debounceInitHandler()"
        )

        source.change(
            fn=lambda source: set_dir_path(opts.outdir_txt2img_samples if source == "t2i" else opts.outdir_img2img_samples),
            inputs=[source]
        ).then(
            fn=refresh_images,
            inputs=[page],
            outputs=[masonry_gallery]
        ).then(
            fn=lambda page_index: str(page_index) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html]            
        ).then(
            fn=None,
            _js="() => debounceInitHandler()"
        )

        refresh.click(
            fn=refresh_images,
            inputs=[page],
            outputs=[masonry_gallery]
        ).then(
            fn=lambda page_index: str(page_index) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html]
        ).then(
            fn=None,
            _js="() => debounceInitHandler()"
        )
        
        # masonry_gallery.change(
        #     fn=None,
        #     _js="() => console.log('change')"
        # )

# debounceInitHandler()
    return (image_browser, "Masonry Browser", "masonry_browser"),

script_callbacks.on_ui_tabs(on_ui_tabs)
