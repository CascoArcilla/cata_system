const formSubmit = document.querySelector(".ct-cretae-session-form");

document.addEventListener("DOMContentLoaded", () => {
  cretaeSession();
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
    renderElementsResponse({
      sessionId: data["codigo_sesion"],
      nameSession: data["nombre_sesion"],
    });
  } catch (error) {
    renderElementsResponse({ error: error });
  }
}

function renderElementsResponse({
  sessionId = "No id",
  error = false,
  nameSession = "",
}) {
  const container = document.querySelector(".ct-message-create");
  const loadElement = document.querySelector(".ct-load-create");

  const message = document.createElement("p");
  message.classList.add("text-2xl", "text-center", "font-bold");

  const nameSessionP = document.createElement("p");
  nameSessionP.classList.add(
    "text-lg",
    "text-center",
    "font-bold"
  );

  const idSession = document.createElement("p");
  idSession.classList.add("text-lg", "text-center", "font-bold");
  const pHelp = document.createElement("p");

  // ******************************** //
  // Mostrar el error que ha ocurrido //
  // ******************************** //
  if (error) {
    message.textContent = "No se ha podido completar la creacion de la sesion";
    idSession.textContent = `Error: ${error}`;
  } else {
    message.textContent = "La sesión se ha creado";
    idSession.innerHTML = `El código de la sesión es:<br><strong class="border-b border-white">${sessionId}</strong>`;
    nameSessionP.textContent = `Nombre de sesión: ${nameSession}`;

    pHelp.classList.add("text-lg", "text-center");
    pHelp.textContent =
      "Puedes pasar este código a los catadores para que ingresen a la sesión";
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
    "tracking-wider",
    "cts-btn-general",
    "btn-push",
    "w-fit",
  ];

  const aIndex = document.createElement("a");
  aIndex.href = "/cata/presenter/";
  aIndex.textContent = "Volver al inicio";

  aIndex.classList.add(
    ...stylesBtns,
    "cts-btn-fifthy"
  );

  const aDetails = document.createElement("a");
  aDetails.href = `/cata/presenter/detalles-sesion/${sessionId}`;
  aDetails.textContent = "Ver detalles la sesión";

  aDetails.classList.add(
    ...stylesBtns,
    "cts-btn-fourthy"
  );

  divBtns.appendChild(aIndex);
  if (!error) {
    divBtns.appendChild(aDetails);
  }

  loadElement.classList.add("hidden");
  container.classList.remove("hidden");

  container.innerHTML = "";

  container.appendChild(message);
  if (nameSession != "") {
    container.appendChild(nameSessionP);
  }
  container.appendChild(idSession);
  container.appendChild(pHelp);
  container.appendChild(divBtns);
}
