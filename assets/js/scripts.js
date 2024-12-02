document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const targetID = this.getAttribute('href');
    const targetElement = document.querySelector(targetID);
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('.section');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const sectionId = link.getAttribute('data-section');

            // Rimuovi la classe active da tutte le sezioni
            sections.forEach(section => section.classList.remove('active'));

            // Aggiungi la classe active alla sezione selezionata
            document.getElementById(sectionId).classList.add('active');
        });
    });
});

// Script per il pulsante menu hamburger
document.querySelector('.menu-toggle').addEventListener('click', function () {
  const menu = document.querySelector('.menu');
  menu.classList.toggle('visible');
});

// Script per la navigazione tra le sezioni
document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('nav a[data-section]');
  const sections = document.querySelectorAll('.section');

  links.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const sectionId = link.getAttribute('data-section');

      // Rimuovi la classe active da tutte le sezioni
      sections.forEach(section => section.classList.remove('active'));

      // Aggiungi la classe active alla sezione selezionata
      document.getElementById(sectionId).classList.add('active');
    });
  });
});

