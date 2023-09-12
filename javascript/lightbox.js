class SDLightbox {

  constructor(options) {
    this.gallery = document.querySelector(options.gallery);
    this.childrenSelector = options.children;
    this.imageCards = this.gallery.querySelectorAll(this.childrenSelector);
    this.currentIndex = 0; // Keep track of the currently displayed image index
    
    this.setupEventListeners();

    console.log('SD Lightbox');
  }

  // Function to show the modal for a specific image
  displayModal(index) {
    // Get references to DOM elements
    let lightboxModal = document.querySelector('.modal');
    let modalImage = document.getElementById('modal-image');
    let modalPrompt = document.querySelector('.modal-prompt');
    let modalNegPrompt = document.querySelector('.modal-neg-prompt');
    let modalModel = document.querySelector('.modal-model');
    let modalSeed = document.querySelector('.modal-seed');
    let modalCfgScale = document.querySelector('.modal-cfg-scale');
    let modalSampler = document.querySelector('.modal-sampler');
    let modalSteps = document.querySelector('.modal-steps');
    
    // Make sure the index is within bounds
    if (index >= 0 && index < this.imageCards.length) {
        const card = this.imageCards[index];
        const imageInfo = card.querySelector('.image-info');

        // Display the modal
        lightboxModal.style.display = 'flex';

        // Set modal content based on the clicked image's data attributes
        modalImage.src = card.querySelector('img').src;
        modalPrompt.textContent = imageInfo.getAttribute('data-prompt');
        modalNegPrompt.textContent = imageInfo.getAttribute('data-negative-prompt');
        modalModel.textContent = imageInfo.getAttribute('data-model');
        modalSeed.textContent = imageInfo.getAttribute('data-seed');
        modalCfgScale.textContent = imageInfo.getAttribute('data-cfg-scale');
        modalSampler.textContent = imageInfo.getAttribute('data-sampler');
        modalSteps.textContent = imageInfo.getAttribute('data-steps');

        // Update the currentIndex
        this.currentIndex = index;
    }
  }

  // Function to navigate to the next image
  nextImage() {
    const nextIndex = (this.currentIndex + 1) % this.imageCards.length;
    this.displayModal(nextIndex);
  }

  // Function to navigate to the previous image
  prevImage() {
    const prevIndex = (this.currentIndex - 1 + this.imageCards.length) % this.imageCards.length;
    this.displayModal(prevIndex);
  }

  setupEventListeners() {
    const self = this;
    let lightboxModal = document.querySelector('.modal');
    let closeBtn = document.querySelector('.close-btn');
    
    this.gallery.addEventListener('click', (e) => {
      const masonryItem = e.target.closest(this.childrenSelector);
      console.log(masonryItem);
        if (masonryItem) {
            e.preventDefault();

            this.imageCards = this.gallery.querySelectorAll(this.childrenSelector);
            const index = Array.from(this.imageCards).indexOf(masonryItem);
            this.displayModal(index);
        }
    });

    // Close the modal when the close button is clicked
    closeBtn.addEventListener('click', () => {
      lightboxModal.style.display = 'none';
    });

    lightboxModal.addEventListener('click', (e) => {
      if (e.target === lightboxModal) {
        lightboxModal.style.display = 'none';
      }
    });

    // Add a keydown event listener to the document
    document.addEventListener('keydown', (e) => {
      if (current_tab() && lightboxModal.style.display === 'flex') {
          // If the modal is open, listen for arrow key presses
          switch (e.key) {
              case 'ArrowLeft':
              case 'a':
                  self.prevImage();
                  break;
              case 'ArrowRight':
              case 'd':
                  self.nextImage();
                  break;
              case 'Escape':
                  lightboxModal.style.display = 'none'; // Close the modal on Escape key
                  break;
          }
      }
    });
  }
}