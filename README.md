## sd-masonry

A custom image browser extension for [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

#### Gallery View
![Gallery View](./screenshots/gallery.png?raw=true "Gallery  View")

#### Photo View
![Lightbox](./screenshots/lightbox.png?raw=true "Lightbox  View")

## Installation

The extension can be installed directly from within the **Extensions** tab within the Webui.

Manual install from within the webui directory:

	git clone https://github.com/bit9labs/sd-masonry extensions/sd-masonry

and restart your stable-diffusion-webui, then you can see the new tab "Masonry Browser".

## Hotkeys

| Key Combination     | Action            |
|---------------------|-------------------|
| Shift + Q           | First Page        |
| Q                   | Previous Page     |
| E                   | Next Page         |
| Shift + E           | Last Page         |
| A*                  | Previous Image    |
| D*                  | Next Image        |

*When lightbox is Open* *



## Recent updates

- Support for SQLite
- Remove dependency on PhotoswipeJS
- Meta information in individual view
- Hotkeys support

## Roadmap

- Ability to push selecteed image to t2i and i2i

## Credit

I was inspired by [stable-diffusion-webui-images-browser](https://github.com/AlUlkesh/stable-diffusion-webui-images-browser/)

- [Masonry](https://github.com/desandro/masonry)
