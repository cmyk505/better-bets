function _createForOfIteratorHelper(o, allowArrayLike) {
  var it =
    (typeof Symbol !== "undefined" && o[Symbol.iterator]) || o["@@iterator"];
  if (!it) {
    if (
      Array.isArray(o) ||
      (it = _unsupportedIterableToArray(o)) ||
      (allowArrayLike && o && typeof o.length === "number")
    ) {
      if (it) o = it;
      var i = 0;
      var F = function F() {};
      return {
        s: F,
        n: function n() {
          if (i >= o.length) return { done: true };
          return { done: false, value: o[i++] };
        },
        e: function e(_e) {
          throw _e;
        },
        f: F,
      };
    }
    throw new TypeError(
      "Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."
    );
  }
  var normalCompletion = true,
    didErr = false,
    err;
  return {
    s: function s() {
      it = it.call(o);
    },
    n: function n() {
      var step = it.next();
      normalCompletion = step.done;
      return step;
    },
    e: function e(_e2) {
      didErr = true;
      err = _e2;
    },
    f: function f() {
      try {
        if (!normalCompletion && it.return != null) it.return();
      } finally {
        if (didErr) throw err;
      }
    },
  };
}

function _unsupportedIterableToArray(o, minLen) {
  if (!o) return;
  if (typeof o === "string") return _arrayLikeToArray(o, minLen);
  var n = Object.prototype.toString.call(o).slice(8, -1);
  if (n === "Object" && o.constructor) n = o.constructor.name;
  if (n === "Map" || n === "Set") return Array.from(o);
  if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))
    return _arrayLikeToArray(o, minLen);
}

function _arrayLikeToArray(arr, len) {
  if (len == null || len > arr.length) len = arr.length;
  for (var i = 0, arr2 = new Array(len); i < len; i++) {
    arr2[i] = arr[i];
  }
  return arr2;
}

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
    var _ref = _asyncToGenerator(
      /*#__PURE__*/ regeneratorRuntime.mark(function _callee(e) {
        var userId, res, resultsDiv;
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch ((_context.prev = _context.next)) {
              case 0:
                // handles click of reload balance button on home page
                e.preventDefault();
                userId = document.querySelector("#reload-balance-btn").dataset
                  .user; //call API with user ID to check if they're eligible to refill balance

                _context.next = 4;
                return fetch("/balance/".concat(userId)).then(function (res) {
                  return res.json();
                });

              case 4:
                res = _context.sent;
                resultsDiv = document.createElement("div");
                resultsDiv.id = "results-div";

                if (res.eligible) {
                  resultsDiv.innerText =
                    "Balance reloaded. New balance is ".concat(res.balance);
                } else {
                  resultsDiv.innerText =
                    "Not currently eligible to reload balance. You can reload your balance once a day."; // document.getElementById("reload-balance-btn").innerHTML = '';
                }

                document.querySelector("#reload-balance-btn").disabled = true;
                document
                  .querySelector("#balance-info-container")
                  .append(resultsDiv);

              case 10:
              case "end":
                return _context.stop();
            }
          }
        }, _callee);
      })
    );

    return function (_x) {
      return _ref.apply(this, arguments);
    };
  })()
);
document.querySelector("#completion-filter").addEventListener(
  "click",
  /*#__PURE__*/ (function () {
    var _ref2 = _asyncToGenerator(
      /*#__PURE__*/ regeneratorRuntime.mark(function _callee2(e) {
        var selectEl;
        return regeneratorRuntime.wrap(function _callee2$(_context2) {
          while (1) {
            switch ((_context2.prev = _context2.next)) {
              case 0:
                // handles clicks to complete/incomplete filter for events on home page
                e.preventDefault();
                console.log("running");
                selectEl = document.querySelector("#completion-filter");
                localStorage.setItem(
                  "completed",
                  selectEl.options[selectEl.selectedIndex].value
                );
                searchWithFilters().then(function (search) {
                  return addEventsToPage(search);
                });

              case 5:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee2);
      })
    );

    return function (_x2) {
      return _ref2.apply(this, arguments);
    };
  })()
);
document.querySelector("input#search-events").addEventListener(
  "keyup",
  /*#__PURE__*/ (function () {
    var _ref3 = _asyncToGenerator(
      /*#__PURE__*/ regeneratorRuntime.mark(function _callee3(e) {
        return regeneratorRuntime.wrap(function _callee3$(_context3) {
          while (1) {
            switch ((_context3.prev = _context3.next)) {
              case 0:
                // handles new inputs to search filter
                localStorage.setItem("q", e.target.value);
                searchWithFilters().then(function (search) {
                  return addEventsToPage(search);
                });

              case 2:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3);
      })
    );

    return function (_x3) {
      return _ref3.apply(this, arguments);
    };
  })()
);

var addEventsToPage = function addEventsToPage(search) {
  // loops through new events returned by database and adds them to DOM
  var eventCards = document.querySelectorAll("#event-list");

  var _iterator = _createForOfIteratorHelper(eventCards),
    _step;

  try {
    for (_iterator.s(); !(_step = _iterator.n()).done; ) {
      var ev = _step.value;
      ev.parentNode.removeChild(ev);
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }

  var _iterator2 = _createForOfIteratorHelper(search),
    _step2;

  try {
    for (_iterator2.s(); !(_step2 = _iterator2.n()).done; ) {
      var s = _step2.value;
      document
        .querySelector(".event-list-container")
        .insertAdjacentHTML(
          "afterbegin",
          '\n      <div id="event-list">\n    <div class="card bg-light">\n                <div class="row align-items-center">\n                    <div class="col">\n                        <a href="/event/'
            .concat(
              s.id,
              '">\n                            <img class="col" src='
            )
            .concat(
              s.strThumb,
              ' alt="Card image cap">\n                        </a>\n                    </div>\n                    <div class="col">\n\n                        <a href="/event/'
            )
            .concat(s.id, '">\n                            ')
            .concat(
              s.title,
              "\n                        </a>\n                        <div>"
            )
            .concat(
              s.datetime,
              " PST</div>\n\n                    </div>\n                </div>\n            </div>\n        <br>\n        </div>\n    "
            )
        );
    }
  } catch (err) {
    _iterator2.e(err);
  } finally {
    _iterator2.f();
  }
};

var searchWithFilters = function searchWithFilters(async) {
  // calls out to Flask endpoint to get updated results from DB based on user search
  var q = localStorage.getItem("q");
  var completed = localStorage.getItem("completed");
  return fetch("/search?q=".concat(q, "&completed=").concat(completed)).then(
    function (res) {
      return res.json();
    }
  );
};
