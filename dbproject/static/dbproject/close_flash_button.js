document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#close")
    .addEventListener("click", () => close_fields());

  function close_fields() {
    document.querySelector("#alert").hidden = true;
  }
});
