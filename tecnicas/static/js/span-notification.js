function spanNotifaction(messageError, isError = true, time = 4500) {
  const span = document.createElement("span");
  span.textContent = messageError;

  const div = document.createElement("div");
  div.classList.add("alert", isError ? "alert-error" : "alert-success");
  div.appendChild(span);

  document.querySelector(".toast").append(div);

  setTimeout(() => {
    document.querySelector(".toast").removeChild(div);
  }, time);
}
