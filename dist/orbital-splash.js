const splash = document.querySelector('.orbital-splash');

if (typeof splash?.showModal === 'function') {
  splash.addEventListener('cancel', (event) => event.preventDefault());
  splash.showModal();
  setTimeout(() => {
    if (splash.open) splash.close();
  }, 2100);
}
