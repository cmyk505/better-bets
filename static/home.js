//set default search filters in local storage
localStorage.setItem("q", "");
localStorage.setItem("completed", "incomplete");

document
  .querySelector("#reload-balance-btn")
  .addEventListener("click", async e => {
    // handles click of reload balance button on home page
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
  .querySelector("#completion-filter")
  .addEventListener("click", async e => {
    // handles clicks to complete/incomplete filter for events on home page
    e.preventDefault();
    console.log("running");
    const selectEl = document.querySelector("#completion-filter");
    localStorage.setItem(
      "completed",
      selectEl.options[selectEl.selectedIndex].value
    );

    searchWithFilters().then(search => addEventsToPage(search));
  });

document
  .querySelector("input#search-events")
  .addEventListener("keyup", async e => {
    // handles new inputs to search filter
    localStorage.setItem("q", e.target.value);
    searchWithFilters().then(search => addEventsToPage(search));
  });

const addEventsToPage = search => {
  // loops through new events returned by database and adds them to DOM
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
};

const searchWithFilters = async => {
  // calls out to Flask endpoint to get updated results from DB based on user search
  const q = localStorage.getItem("q");
  const completed = localStorage.getItem("completed");
  return fetch(`/search?q=${q}&completed=${completed}`).then(res => res.json());
};
