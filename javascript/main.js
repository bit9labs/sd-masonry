let scripts = [
    "https://unpkg.com/masonry-layout@4/dist/masonry.pkgd.min.js",
    "https://unpkg.com/imagesloaded@5/imagesloaded.pkgd.min.js"
];

// Loop through the scripts array
for (let i = 0; i < scripts.length; i++) {
    const script = document.createElement('script');
    script.src = scripts[i];
    document.head.appendChild(script);
}

// Add the CSS link
let is_initialized = false;
let msnry = null;
let lightbox = null;
let container = null;
let loadingWheel = null;

function debounce(func, delay) {
    let timeoutId;
    
    return function() {
      const context = this;
      const args = arguments;
      
      clearTimeout(timeoutId);
      timeoutId = setTimeout(function() {
        func.apply(context, args);
      }, delay);
    };
}

// Code that depends on the masonry library
function initializeMasonry() {
    // Initialize masonry or perform other actions with the library
    // ...
    
    if (!is_initialized) {
        container = document.querySelector('.masonry-container');
        loadingWheel = document.getElementById('loading-wheel');
        loadingWheel.classList.add('hidden');

        msnry = new Masonry( container, {
            itemSelector:'.masonry-item', 
            columnWidth: '.masonry-item'
        });

        lightbox = new SDLightbox({
            gallery: '.masonry-container',
            children: '.masonry-item'
        });

        is_initialized = true;
    } else {
        // console.log('reload masonry');
        container.classList.add('hidden');
        loadingWheel.classList.remove('hidden');
        let imgLoad = imagesLoaded( container, () => {
            container.classList.remove('hidden');
            loadingWheel.classList.add('hidden');
            // console.log('images loaded', loadingWheel);

            msnry.reloadItems();
            msnry.layout();
        });
        
    }
}

debounceInitHandler = debounce(initializeMasonry, 500);

current_tab = () => get_uiCurrentTab().textContent.trim() === "Masonry Browser"
onUiTabChange(() => {
    // console.log("tab change", get_uiCurrentTab().textContent);
    if (current_tab()) {
        initializeMasonry();
    }
});

// Add a keydown event listener to the document
document.addEventListener('keydown', (e) => {
    if (current_tab()) {
        const shiftKeyHeld = e.shiftKey;
        let lightboxModal = document.querySelector('.modal');

        if (e.shiftKey) {
            switch (e.key) {
                case 'Q':
                    lightboxModal.style.display = 'none';
                    document.querySelector('.sd-masonry.first').click();
                    break;
                case 'E':
                    lightboxModal.style.display = 'none';
                    document.querySelector('.sd-masonry.last').click();
                    break;
            }
        } else {
            switch (e.key) {
                case 'q':
                    lightboxModal.style.display = 'none';
                    document.querySelector('.sd-masonry.previous').click();
                    break;
                case 'e':
                    lightboxModal.style.display = 'none';
                    document.querySelector('.sd-masonry.next').click();
                    break;
            }
        }
    }
});