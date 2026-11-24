/* ?paper -> light "paper" theme (print shops with poor dark coverage) */
document.documentElement.dataset.theme = /paper/.test(location.search) ? "light" : "dark";
