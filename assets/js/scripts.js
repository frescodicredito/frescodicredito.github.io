// Script per il pulsante menu hamburger
document.querySelector('.menu-toggle').addEventListener('click', function () {
  const menu = document.querySelector('.menu');
  menu.classList.toggle('visible');
});

// Script per la navigazione tra le sezioni e caricamento dinamico del contenuto
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('nav a[data-file]');
  const contentArea = document.getElementById('content-area');

  // Carica la Home all'avvio
  fetch('home.html')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.text();
    })
    .then(html => {
      contentArea.innerHTML = html;
    })
    .catch(error => {
      console.error('Errore nel caricamento della sezione Home:', error);
      contentArea.innerHTML = `<p>Sorry, the Home content could not be loaded.</p>`;
    });

  // Gestisce la navigazione dinamica
  links.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const file = link.getAttribute('data-file');

      // Carica il contenuto della sezione selezionata
      fetch(file)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.text();
        })
        .then(html => {
          contentArea.innerHTML = html;
        })
        .catch(error => {
          console.error('Errore nel caricamento del contenuto:', error);
          contentArea.innerHTML = `<p>Sorry, the content could not be loaded.</p>`;
        });
    });
  });
});
