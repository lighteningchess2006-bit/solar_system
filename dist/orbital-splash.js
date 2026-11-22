const splash = document.querySelector('.orbital-splash');
const galleryOnly = splash?.hasAttribute('data-gallery-only');
const galleryView = new URLSearchParams(location.search).get('view') === 'gallery';

if (typeof splash?.showModal === 'function' && (!galleryOnly || galleryView)) {
  splash.addEventListener('cancel', (event) => event.preventDefault());
  splash.showModal();
  setTimeout(() => {
    if (splash.open) splash.close();
  }, 2100);
}
