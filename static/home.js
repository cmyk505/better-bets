function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
  try {
    var info = gen[key](arg);
    var value = info.value;
  } catch (error) {
    reject(error);
    return;
  }
  if (info.done) {
    resolve(value);
  } else {
    Promise.resolve(value).then(_next, _throw);
  }
}

function _asyncToGenerator(fn) {
  return function () {
    var self = this,
      args = arguments;
    return new Promise(function (resolve, reject) {
      var gen = fn.apply(self, args);
      function _next(value) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
      }
      function _throw(err) {
        asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
      }
      _next(undefined);
    });
  };
}

//set default search filters in local storage
localStorage.setItem("q", "");
localStorage.setItem("completed", "incomplete");
document.querySelector("#reload-balance-btn").addEventListener(
  "click",
  /*#__PURE__*/ (function () {
    var _ref = _asyncToGenerator(function* (e) {
      // handles click of reload balance button on home page
      e.preventDefault();
      const userId = document.querySelector("#reload-balance-btn").dataset.user; //call API with user ID to check if they're eligible to refill balance

      const res = yield fetch(`/balance/${userId}`).then(res => res.json());
      const resultsDiv = document.createElement("div");
      resultsDiv.id = "results-div";

      if (res.eligible) {
        resultsDiv.innerText = `Balance reloaded. New balance is ${res.balance}`;
      } else {
        resultsDiv.innerText = `Not currently eligible to reload balance. You can reload your balance once a day.`; // document.getElementById("reload-balance-btn").innerHTML = '';
      }

      document.querySelector("#reload-balance-btn").disabled = true;
      document.querySelector("#balance-info-container").append(resultsDiv);
    });

    return function (_x) {
      return _ref.apply(this, arguments);
    };
  })()
);
document.querySelector("#completion-filter").addEventListener(
  "click",
  /*#__PURE__*/ (function () {
    var _ref2 = _asyncToGenerator(function* (e) {
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

    return function (_x2) {
      return _ref2.apply(this, arguments);
    };
  })()
);
document.querySelector("input#search-events").addEventListener(
  "keyup",
  /*#__PURE__*/ (function () {
    var _ref3 = _asyncToGenerator(function* (e) {
      // handles new inputs to search filter
      localStorage.setItem("q", e.target.value);
      searchWithFilters().then(search => addEventsToPage(search));
    });

    return function (_x3) {
      return _ref3.apply(this, arguments);
    };
  })()
);

const addEventsToPage = search => {
  // loops through new events returned by database and adds them to DOM
  const eventCards = document.querySelectorAll("#event-list");

  for (const ev of eventCards) {
    ev.parentNode.removeChild(ev);
  }

  for (const s of search) {
    document.querySelector(".event-list-container").insertAdjacentHTML(
      "afterbegin",
      `
      <div id="event-list">
    <div class="card bg-light">
                <div class="row align-items-center">
                    <div class="col">
                        <a href="/event/${s.id}">
                            <img class="col" src=${s.strThumb} alt="Card image cap">
                        </a>
                    </div>
                    <div class="col">

                        <a href="/event/${s.id}">
                            ${s.title}
                        </a>
                        <div>${s.datetime} PST</div>

                    </div>
                </div>
            </div>
        <br>
        </div>
    `
    );
  }
};

const searchWithFilters = async => {
  // calls out to Flask endpoint to get updated results from DB based on user search
  const q = localStorage.getItem("q");
  const completed = localStorage.getItem("completed");
  return fetch(`/search?q=${q}&completed=${completed}`).then(res => res.json());
};
