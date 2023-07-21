let scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/photoswipe/5.3.4/umd/photoswipe.umd.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/photoswipe/5.3.4/umd/photoswipe-lightbox.umd.min.js",
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
const cssLink = document.createElement('link');
cssLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/photoswipe/5.3.4/photoswipe.min.css';
cssLink.rel = 'stylesheet';
document.head.appendChild(cssLink);

let is_initialized = false;
let msnry = null;
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
        console.log('init masonry');
        container = document.querySelector('.masonry-container');
        loadingWheel = document.getElementById('loading-wheel');
        loadingWheel.classList.add('hidden');

        msnry = new Masonry( container, {
            itemSelector:'.masonry-item', 
            columnWidth: '.masonry-item'
        });

        var lightbox = new PhotoSwipeLightbox({
            gallery: '.masonry-container',
            children: 'a',
            pswpModule: PhotoSwipe 
        });
        lightbox.init();
        is_initialized = true;
    } else {
        console.log('reload masonry');
        container.classList.add('hidden');
        loadingWheel.classList.remove('hidden');
        let imgLoad = imagesLoaded( container, () => {
            container.classList.remove('hidden');
            loadingWheel.classList.add('hidden');
            console.log('images loaded', loadingWheel);

            msnry.reloadItems();
            msnry.layout();
        });
        
    }
}

debounceInitHandler = debounce(initializeMasonry, 500);

onUiTabChange(() => {
    console.log("tab change", get_uiCurrentTab().textContent);
    if (get_uiCurrentTab().textContent.trim() === "Masonry Browser") {
        initializeMasonry();
    }
});