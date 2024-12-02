document.addEventListener("DOMContentLoaded", function () {
  // Aggiungi listener al link "Blog"
  const blogLink = document.querySelector('a[href="/blog/"]');
  if (blogLink) {
    blogLink.addEventListener("click", function (e) {
      e.preventDefault(); // Previene il comportamento predefinito del link

      // Carica il contenuto del blog
      fetch("/blog.html") // Percorso al file blog.html
        .then((response) => {
          if (!response.ok) throw new Error("Errore nel caricamento del blog.");
          return response.text();
        })
        .then((html) => {
          // Trova il contenitore principale e sostituisci il contenuto
          const mainContent = document.querySelector("main");
          if (mainContent) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const blogContent = doc.querySelector(".content");
            mainContent.innerHTML = blogContent.innerHTML;
          }
        })
        .catch((error) => {
          console.error("Errore:", error);
        });
    });
  }
});
