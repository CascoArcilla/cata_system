document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("download-csv-btn");
  if (!btn) return;

  btn.addEventListener("click", function () {
    // Try set the table in the page
    let table = document.getElementById("generic-donwload-table");
    if (!table) {
      const section = btn.closest("section");
      if (section) table = section.querySelector("table");
    }
    if (!table) {
      console.warn("No se encontró la tabla para descargar.");
      return;
    }

    // helper to trim and normalize cell text
    const cellText = (cell) => {
      if (!cell) return "";
      return String(cell.textContent || "").trim();
    };

    // Collect headers
    const headers = [];
    const ths = table.querySelectorAll("thead th");
    ths.forEach((th) => headers.push(cellText(th)));

    // Collect rows
    const rows = [];
    const trs = table.querySelectorAll("tbody tr");
    trs.forEach((tr) => {
      const cols = [];
      const tds = tr.querySelectorAll("td");
      tds.forEach((td) => cols.push(cellText(td)));
      rows.push(cols);
    });

    // Convert to CSV string (escape quotes, wrap in quotes if needed)
    const escapeValue = (val) => {
      if (val == null) return "";
      normalVal = val.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      const needsQuotes = /[",\n,]/.test(normalVal);
      let v = String(normalVal).replace(/"/g, '""');
      if (needsQuotes) v = `"${v}"`;
      return v;
    };

    const lines = [];
    if (headers.length) lines.push(headers.map(escapeValue).join(","));
    rows.forEach((r) => lines.push(r.map(escapeValue).join(",")));

    const csvContent = lines.join("\n");

    // File name: data_{nombre_sesion or codigo_sesion}
    const rawName = (btn.dataset.sessionName || "").trim();
    const code = (btn.dataset.sessionCode || "").trim() || "session";
    const namePart = rawName
      ? rawName.replace(/[^a-zA-Z0-9-_áéíóúÁÉÍÓÚ ]/g, "").replace(/\s+/g, "_")
      : code;
    const fileName = `data_${namePart}.csv`;

    // Create blob and force download
    const blob = new Blob([csvContent], { type: "text/csv;charset=UTF-8;" });
    if (navigator.msSaveBlob) {
      navigator.msSaveBlob(blob, fileName);
    } else {
      const link = document.createElement("a");
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", fileName);
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  });
});
