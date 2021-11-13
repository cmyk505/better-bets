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

document
  .querySelector("input#search-events")
  .addEventListener("keyup", async e => {
    console.log("running");
    const search = await fetch(`/search?q=${e.target.value}`).then(res =>
      res.json()
    );
    const eventCards = document.querySelectorAll(".event-card");
    for (const ev of eventCards) {
      ev.parentNode.removeChild(ev);
    }

    for (const s of search) {
      let newCard = document.createElement("div");
      newCard.classList.add("event-card");
      let a = document.createElement("a");
      a.href = `/event/${s.id}`;
      let p = document.createElement("p");
      a.append(p);
      p.innerText = s.title;

      let newUl = document.createElement("ul");
      let teamsLi = document.createElement("li");
      let dateLi = document.createElement("li");
      teamsLi.innerText = `${s.home_team} vs ${s.away_team}`;
      dateLi.innerText = `${s.date}`;
      newUl.append(teamsLi);
      newUl.append(dateLi);

      newCard.append(a);
      newCard.append(newUl);

      document.querySelector("#event-list").append(newCard);
    }
  });
