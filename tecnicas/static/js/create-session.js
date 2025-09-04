const formSubmit = document.querySelector(".ct-cretae-session-form");

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    cretaeSession();
  }, 2000);
});

async function cretaeSession() {
  const dataForm = new FormData(formSubmit);
  const url = `creando-sesion`;

  try {
    const respone = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": dataForm.get("csrfmiddlewaretoken"),
      },
      body: dataForm,
    });

    const jsonResponse = await respone.json();

    if (jsonResponse.error) {
      renderElementsResponse({ error: jsonResponse.error });
      return;
    }

    const data = jsonResponse["data"];
    renderElementsResponse({ sessionId: data["session_id"] });
  } catch (error) {
    renderElementsResponse({ error: jsonResponse.error });
  }
}

function renderElementsResponse({ sessionId = "No id", error = false }) {
  const container = document.querySelector(".ct-message-create");
  const loadElement = document.querySelector(".ct-load-create");

  const p = document.createElement("p");
  p.classList.add("text-2xl", "text-white", "text-center", "font-bold");
  const idSession = document.createElement("p");
  idSession.classList.add("text-lg", "text-white", "text-center", "font-bold");
  const pHelp = document.createElement("p");

  // ******************************** //
  // Mostrar el error que ha ocurrido //
  // ******************************** //
  if (error) {
    p.textContent = "No se ha podido completar la creacion de la sesion";
    idSession.textContent = `Error: ${error}`;
  } else {
    p.textContent = "La session se ha creado";

    idSession.innerHTML = `El ID de la seesion es:<br><strong class="border-b border-white">${sessionId}</strong>`;

    pHelp.classList.add("text-lg", "text-white", "text-center");
    pHelp.textContent =
      "Puedes pasar este ID a los catadores para que ingresen a la sesion";
  }

  const divBtns = document.createElement("div");
  divBtns.classList.add(
    "flex",
    "flex-wrap",
    "justify-center",
    "items-center",
    "gap-5"
  );

  const stylesBtns = [
    "uppercase",
    "text-lg",
    "tracking-wider",
    "font-medium",
    "p-2",
    "px-4",
    "border-b-2",
    "active:border-b-0",
    "active:border-t-2",
    "transition-all",
    "rounded-xl",
    "w-fit",
  ];

  const aIndex = document.createElement("a");
  aIndex.href = "{% url 'cata_system:index' %}";
  aIndex.textContent = "Volver al inicio";

  aIndex.classList.add(
    ...stylesBtns,
    "active:border-blue-500",
    "border-blue-800",
    "bg-blue-500",
    "text-white"
  );

  const aMonitor = document.createElement("a");
  aMonitor.href = "{% url 'cata_system:index' %}";
  aMonitor.textContent = "Monitorear la sesion";

  aMonitor.classList.add(
    ...stylesBtns,
    "active:border-yellow-500",
    "border-yellow-800",
    "bg-yellow-500",
    "text-black"
  );

  divBtns.appendChild(aIndex);
  if (!error) {
    divBtns.appendChild(aMonitor);
  }

  loadElement.classList.add("hidden");
  container.classList.remove("hidden");

  container.innerHTML = "";

  container.appendChild(p);
  container.appendChild(idSession);
  container.appendChild(pHelp);
  container.appendChild(divBtns);
}
