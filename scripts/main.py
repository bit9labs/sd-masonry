import gradio as gr
import os
from PIL import Image

from modules import script_callbacks
from modules.shared import opts
from modules.scripts import basedir
from modules.ui_components import ToolButton

image_ext_list = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".svg"]
dir_path = opts.outdir_samples or opts.outdir_txt2img_samples
image_list = []
items_per_page = 25

def set_dir_path(path):
    global dir_path
    dir_path = path

def traverse_all_files(path):
    # our return object
    image_list = []

    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in image_ext_list:
                image_path = os.path.join(root, filename)
                try:
                    image = Image.open(image_path)
                    width, height = image.size
                    image.close()
                    image_list.append((image_path, width, height))
                except (IOError, SyntaxError) as e:
                    # Skip the image if it cannot be opened or has syntax errors
                    print(f"Skipped {image_path}: {str(e)}")

    return image_list

def set_items_per_page(count):
    global items_per_page 
    items_per_page = int(count) if count != "All" else None
    
def get_images(refresh=False):
    global image_list

    # Check to see if never been scaned or forced via refresh button
    if refresh or len(image_list) == 0:
        image_list = traverse_all_files(dir_path)

    return image_list

def total_pages():
    global items_per_page
    image_list = get_images()
    
    if items_per_page == None:
        return len(image_list)
    
    return (len(image_list) + int(items_per_page) - 1) // int(items_per_page)

def get_page(page_index):
    global items_per_page
    html = ''

    if page_index < 1 or page_index > total_pages():
        page_index = min(total_pages(), max(1, page_index))
    else:
        images = image_list = get_images()
        
        if items_per_page != None:
            #coerce
            items_per_page = int(items_per_page)

            #paginate
            start_index = int((page_index - 1) * items_per_page)
            end_index = int(start_index + items_per_page)
            images = image_list[start_index:end_index]

        for image, width, height in images:
            html += '<a href="/file={}" class="masonry-item" itemprop="contentUrl" data-pswp-width="{}" data-pswp-height="{}">'.format(image, width, height)
            html += '<img src="/file={}" class="object-cover w-96" itemprop="thumbnail" alt="" />'.format(image)
            html += '</a>'
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
    get_images(True)
    return get_page(page_index)


# def get_image_paths():
#     global image_paths
#     if len(image_paths) == 0:
#         image_list = traverse_all_files(dir_path)
#         image_paths = [file_info[0] for file_info in image_list]
#     return image_paths

# def get_image_urls():
#     global image_paths
#     if len(image_paths) == 0:
#         image_list = traverse_all_files(dir_path)
#         image_paths = [os.path.join(basedir(), file_info[0]) for file_info in image_list]
#     return image_paths


def on_ui_tabs():
    # image_paths = get_image_paths()

    # for image_path in image_paths:
    #     print(os.path.join(basedir(), image_path))

    # with gr.Blocks(analytics_enabled=False) as image_browser:
    #     with gr.Row() as main_panel:
    #         image_gallery = gr.Gallery(value=image_paths, show_label=False, elem_id=f"txt2img_image_browser_gallery").style(grid=5)

    # image_urls = get_image_urls()
    with gr.Blocks(analytics_enabled=False) as image_browser:
        #get the first page but also load the images
        html = get_page(1)
        
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    first_page_btn = ToolButton('\u23EE')
                    prev_page_btn = ToolButton('\u23EA')
                    page = gr.Number(value=1, visible=False, show_label=False)
                    next_page_btn = ToolButton('\u23E9')
                    last_page_btn = ToolButton('\u23ED')
            with gr.Column(scale=1):
                page_html = gr.HTML("1/" + str(total_pages()))
            with gr.Column(scale=2):
                with gr.Row():
                    source = gr.Dropdown(choices=["t2i","i2i"], value="t2i", show_label=False)
                    items_count = gr.Dropdown(choices=["All", "25", "50", "100", "250"], value="25", show_label=False)
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
            fn=lambda page_index: str(int(page_index)) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html]
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
        )

        source.change(
            fn=lambda source: set_dir_path(opts.outdir_txt2img_samples if source == "t2i" else opts.outdir_img2img_samples),
            inputs=[source]
        ).then(
            fn=refresh_images,
            inputs=[page],
            outputs=[masonry_gallery]
        ).then(
            fn=lambda page_index: str(int(page_index)) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html]
        )

        refresh.click(
            fn=refresh_images,
            inputs=[page],
            outputs=[masonry_gallery]
        ).then(
            fn=lambda page_index: str(int(page_index)) + "/" + str(total_pages()),
            inputs=[page],
            outputs=[page_html]
        )
        masonry_gallery.change(
            fn=None,
            _js="()=>debounceInitHandler()"
        )

    return (image_browser, "Masonry Browser", "masonry_browser"),

script_callbacks.on_ui_tabs(on_ui_tabs)
