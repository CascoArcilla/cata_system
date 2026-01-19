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
        "cts-enfasis": "#91C4C3",

        "cts-primary": "#FF9D00",
        "cts-secondary": "#E6E6E6",
        "cts-tertiary": "#88EE88",
        "cts-fourthy": "#D18100",
        "cts-fifthy": "#696969",

        "cts-border": "#969696",
        "cts-radius-ring-color": "#79E785",
      },
    },
  },
  plugins: [],
};