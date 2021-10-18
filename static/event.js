document.querySelector("#bet-form").addEventListener("submit", async e => {
  e.preventDefault();
  const selectEl = document.querySelector("#bet-selection");
  const selection = selectEl.options[selectEl.selectedIndex].value;

  const res = await fetch("/api/bet", {
    method: "post",
    body: JSON.stringify({ selection }),
  }).then(response => response.json());

  document.querySelector("#api-response-container").append(res.text);
  document.querySelector("#bet-btn").disabled = true;
});
