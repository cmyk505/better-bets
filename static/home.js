document
  .querySelector("#reload-balance-btn")
  .addEventListener("click", async e => {
    e.preventDefault();
    const userId = document.querySelector("#reload-balance-btn").dataset.user;

    //call API with user ID to check if they're eligible to refill balance
    const res = await fetch(`/balance/${userId}`).then(res => res.json());
    const resultsDiv = document.createElement("div");
    resultsDiv.id = "results-div";
    if (res.eligible) {
      resultsDiv.innerText = `Balance reloaded. New balance is ${res.balance}`;
    } else {
      resultsDiv.innerText = `Not currently eligible to reload balance. You can reload your balance once a week`;
    }
    document.querySelector("#reload-balance-btn").disabled = true;
    document.querySelector("#balance-info-container").append(resultsDiv);
  });
