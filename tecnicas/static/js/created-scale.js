function checkSendRating(word) {
  const btnCheck = document.querySelector(`.ct-btn-check-${word}`);
  const btnSend = document.querySelector(`.ct-btn-submit-${word}`);
  const btnCancel = document.querySelector(`.ct-btn-cancel-${word}`);

  btnCheck.classList.add("hidden");
  btnSend.classList.remove("hidden");
  btnCancel.classList.remove("hidden");
}

function cancelSendRating(word) {
  const btnCheck = document.querySelector(`.ct-btn-check-${word}`);
  const btnSend = document.querySelector(`.ct-btn-submit-${word}`);
  const btnCancel = document.querySelector(`.ct-btn-cancel-${word}`);

  btnCheck.classList.remove("hidden");
  btnSend.classList.add("hidden");
  btnCancel.classList.add("hidden");
}

async function sendRating(word) {
  const formRatingWord = document.querySelector(`.form-rating-${word}`);

  const dataForm = new FormData(formRatingWord);
  const url = "/cata/testers/api/ratingword";

  dataForm.set("name-word", word);

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
      console.log(jsonResponse.error);
      return;
    }

    console.log(jsonResponse);
    remplaceForm(formRatingWord, jsonResponse.message);
  } catch (error) {
    console.log("Error:", error);
  }
}

function remplaceForm(oldForm, message) {
  const articleContainer = document.createElement("article");
  const thankYouMessage = document.createElement("p");
  const messageResponse = document.createElement("p");

  thankYouMessage.textContent =
    "Palabra calificada, gracias por la participación";
  messageResponse.textContent = message;

  articleContainer.classList.add(
    "bg-gray-200",
    "p-6",
    "rounded-lg",
    "mb-3",
    "text-center"
  );
  thankYouMessage.classList.add("text-2xl", "font-bold");
  messageResponse.classList.add("text-lg");

  articleContainer.appendChild(thankYouMessage);
  articleContainer.appendChild(messageResponse);
  oldForm.replaceWith(articleContainer);
}
