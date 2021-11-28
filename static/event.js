document.querySelector("#bet-form").addEventListener("submit", async e => {
  // handles form submission for new bets by calling out to Flask route
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
});

document
  .querySelector("#api-response-container")
  .addEventListener(onload, async e => {
    //upon page load, check if user has already made bet on event and render content accordingly
    const div = document.querySelector("#bet-details");

    const content = await fetch("/api/bet/content").then(response =>
      response.json()
    );

    div.append(content);
  });
