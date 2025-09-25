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
  console.log(formRatingWord);

  const dataForm = new FormData(this);
  const url = "/cata/testers/api/ratingword";

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
  } catch (error) {
    console.log("Error:", error);
  }
}
