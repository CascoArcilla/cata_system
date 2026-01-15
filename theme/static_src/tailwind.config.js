// tailwind.config.js
module.exports = {
  content: [
    "../templates/base.html",
    "../../tecnicas/templates/tecnicas/*.{html,py,js}",
    "../../tecnicas/templates/tecnicas/**/*.{html,py,js}",
  ],
  theme: {
    extend: {
      colors: {
        "surface-general": "#FFFFFF",
        "surface-alter": "#FFE0AD",
        "surface-sweet": "#FFC29B",
        "surface-ligt": "#FFECC0",
        "surface-card": "#FFF3E0",
        "surface-alter-card": "#91C4C3",
        "btn-primary": "#FF9D00",
        "btn-secondary": "#E6E6E6",
        "btn-tertiary": "#88EE88",
        "ct-success": "#2E7D32",
        "ct-error": "#D18100",
        "cts-border": "#969696",

        "cts-radius-ring-color": "#79E785",
      },
    },
  },
  plugins: [],
};
// rgb(121, 231, 133)