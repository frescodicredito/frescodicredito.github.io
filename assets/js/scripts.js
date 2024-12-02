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

