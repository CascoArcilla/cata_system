document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("download-pf-all-csv-btn");
  if (!btn) return;

  btn.addEventListener("click", function () {
    const table = document.getElementById("table-pf-all");
    if (!table) {
      console.warn("No se encontró la tabla para descargar.");
      return;
    }

    const cellText = (cell) => {
      if (!cell) return "";
      return String(cell.textContent || "").trim();
    };

    // Build first header row: "Producto" + usernames (repeated by colspan)
    const firstHeaderRow = [];
    const secondHeaderRow = [];
    const headerRows = table.querySelectorAll("thead tr");
    
    const firstRow = headerRows[0];
    const firstRowCells = firstRow.querySelectorAll("th");
    const secondRow = headerRows[1];
    const wordCells = secondRow.querySelectorAll("th");
    
    // First cell: "Producto" (with rowspan=2 in HTML, so it appears in first row, empty in second)
    firstHeaderRow.push(cellText(firstRowCells[0]));
    secondHeaderRow.push(""); // Empty cell under "Producto"
    
    // Process each user column
    let wordIndex = 0;
    for (let i = 1; i < firstRowCells.length; i++) {
      const th = firstRowCells[i];
      const username = cellText(th);
      const colspan = parseInt(th.getAttribute("colspan") || "1");
      
      // Add username to first row, repeated for each word (colspan)
      for (let k = 0; k < colspan; k++) {
        firstHeaderRow.push(username);
        
        // Add corresponding word to second row
        const wordCell = wordCells[wordIndex];
        if (wordCell) {
          secondHeaderRow.push(cellText(wordCell));
        } else {
          secondHeaderRow.push("");
        }
        wordIndex++;
      }
    }

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
      const normalVal = val.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      const needsQuotes = /[",\n]/.test(normalVal);
      let v = String(normalVal).replace(/"/g, '""');
      if (needsQuotes) v = `"${v}"`;
      return v;
    };

    const lines = [];
    // Add both header rows
    lines.push(firstHeaderRow.map(escapeValue).join(","));
    lines.push(secondHeaderRow.map(escapeValue).join(","));
    // Add data rows
    rows.forEach((r) => lines.push(r.map(escapeValue).join(",")));

    const csvContent = lines.join("\n");

    // File name: data_{nombre_sesion or codigo_sesion}_pf_all
    const rawName = (btn.dataset.sessionName || "").trim();
    const code = (btn.dataset.sessionCode || "").trim() || "session";
    const namePart = rawName
      ? rawName.replace(/[^a-zA-Z0-9-_áéíóúÁÉÍÓÚ ]/g, "").replace(/\s+/g, "_")
      : code;
    const fileName = `data_${namePart}_pf_all.csv`;

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
