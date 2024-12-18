// Script per il pulsante menu hamburger
document.querySelector('.menu-toggle').addEventListener('click', function () {
  const menu = document.querySelector('.menu');
  menu.classList.toggle('visible');
});

// Script per la navigazione tra le sezioni e caricamento dinamico del contenuto
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('nav a[data-file]');
  const contentArea = document.getElementById('content-area');

  // Funzione per caricare i contenuti dinamici
  async function loadContent(file) {
    try {
      const response = await fetch(file);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const html = await response.text();
      contentArea.innerHTML = html;
    } catch (error) {
      console.error(`Errore nel caricamento di ${file}:`, error);
      contentArea.innerHTML = `<p>Sorry, the content could not be loaded.</p>`;
    }
  }

  // Gestisce la navigazione dinamica
  links.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault(); // Previene il comportamento predefinito (apertura di una nuova pagina)
      const file = link.getAttribute('data-file');
      console.log(`Caricamento dinamico della sezione: ${file}`);
      loadContent(file); // Carica la sezione selezionata
    });
  });

  // Carica automaticamente la Home all'avvio
  loadContent('home.html');
});
