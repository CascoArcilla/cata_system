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
        "surface-general": "#B95E82",
        "surface-alter": "#F39F9F",
        "surface-sweet": "#FFC29B",
        "surface-ligt": "#FFECC0",
        "surface-card": "#FFF3E0",
        "surface-alter-card": "#91C4C3",
        "btn-primary": "#4CAF50",
        "btn-secondary": "#E45A92",
        "btn-tertiary": "#FFACAC",
        "ct-success": "#2E7D32",
        "ct-error": "#E62727",
      },
    },
  },
  plugins: [],
};
