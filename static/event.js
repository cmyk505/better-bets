document.querySelector("#bet-form").addEventListener("submit", async e => {
  e.preventDefault();
  const selectEl = document.querySelector("#bet-selection");
  const selection = selectEl.options[selectEl.selectedIndex].value;

  const eventId = document.querySelector("#bet-btn").dataset.event_id;
  const betAmt = document.querySelector("#bet-amt").value;

  const res = await fetch("/api/bet", {
    method: "post",
    body: JSON.stringify({ selection, eventId, betAmt }),
  }).then(response => response.json());

  document.querySelector("#api-response-container").append(res.text);
  document.querySelector("#bet-btn").disabled = true;
  location.reload();
});
