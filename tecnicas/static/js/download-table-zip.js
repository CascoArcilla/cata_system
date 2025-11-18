document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("download-csv-btn");
  if (!btn) return;

  btn.addEventListener("click", async function () {
    if (typeof JSZip === "undefined" || typeof saveAs === "undefined") {
      alert(
        "Librerías JSZip o FileSaver no están cargadas. Asegúrate de incluir los CDN de JSZip y FileSaver."
      );
      return;
    }

    const sections = document.querySelectorAll("section[data-tester]");
    if (!sections || sections.length === 0) {
      alert("No hay tablas para descargar.");
      return;
    }

    const zip = new JSZip();

    let zipName = "";

    sections.forEach((sec) => {
      const tester = sec.getAttribute("data-tester") || "tester";
      const sessionName = sec.getAttribute("data-session-name") || "";
      const sessionCode = sec.getAttribute("data-session-code") || "";

      const fileName = `${tester}_${
        sessionName ? sessionName.trim() : sessionCode.trim()
      }`;

      zipName = `datos_sesion_${
        sessionName ? sessionName.trim() : sessionCode.trim()
      }`;

      const table = sec.querySelector("table");
      if (!table) return;

      // Build CSV
      const rows = [];
      const headerCells = Array.from(table.querySelectorAll("thead tr th"));
      const headers = headerCells.map((h) => h.textContent.trim());
      rows.push(headers.map(escapeCsv).join(","));

      const trs = table.querySelectorAll("tbody tr");
      trs.forEach((tr) => {
        const tds = Array.from(tr.querySelectorAll("td"));
        const values = tds.map((td) => escapeCsv(td.textContent.trim()));
        rows.push(values.join(","));
      });

      const csvContent = rows.join("\r\n");
      zip.file(`${fileName}.csv`, csvContent);
    });

    try {
      const blob = await zip.generateAsync({ type: "blob" });
      const zipNameWithExtension = zipName + ".zip";
      saveAs(blob, zipNameWithExtension);
    } catch (err) {
      console.error(err);
      alert("Error al generar el ZIP: " + err.message);
    }
  });

  const escapeCsv = (val) => {
    if (val == null) return "";
    let normalVal = val.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const needsQuotes = /[",\n,]/.test(normalVal);
    let v = String(normalVal).replace(/"/g, '""');
    if (needsQuotes) v = `"${v}"`;
    return v;
  };
});
