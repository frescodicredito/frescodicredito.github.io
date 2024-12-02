document.addEventListener("DOMContentLoaded", function () {
  // Aggiungi listener ai link del menu
  const links = document.querySelectorAll('.menu li a[href^="/"], .menu li a[href="#contact"]');

  links.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault(); // Previene il comportamento predefinito

      const target = this.getAttribute("href"); // Ottieni il percorso della pagina
      if (target === "#contact") {
        // Gestione speciale per il contatto
        const contactSection = document.querySelector("#contact");
        contactSection.classList.toggle("visible");
        return;
      }

      const fetchTarget = target === "/" ? "/home.html" : target; // Se è Home, carica home.html

      // Carica dinamicamente il contenuto
      fetch(fetchTarget)
        .then((response) => {
          if (!response.ok) throw new Error(`Errore nel caricamento: ${fetchTarget}`);
          return response.text();
        })
        .then((html) => {
          // Trova il contenitore principale e sostituisci il contenuto
          const mainContent = document.querySelector("main");
          if (mainContent) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const dynamicContent = doc.querySelector(".content") || doc.body;
            mainContent.innerHTML = dynamicContent.innerHTML;
          }
        })
        .catch((error) => {
          console.error("Errore:", error);
        });
    });
  });

  // Script per il pulsante menu hamburger
  document.querySelector('.menu-toggle').addEventListener('click', function () {
    const menu = document.querySelector('.menu');
    menu.classList.toggle('visible');
  });
});
