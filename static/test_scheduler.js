document
  .querySelector("#toggle-scheduled-jobs-form")
  .addEventListener("submit", async e => {
    e.preventDefault();
    console.log("running");
    // make API call to Flask endpoint that starts or shuts down scheduled processes, depending on current button text

    const responseText = {
      start: "please allow a minute while we start up the scheduled tasks...",
      stop: "please allow a minute while we shut down the scheduled tasks...",
      "after-stop": "Automated process has been stopped",
      "after-start":
        "One user with random data is being added to the database every 3 seconds",
    };

    const btn = document.querySelector("#toggle-scheduled-jobs-btn");
    const btnText = btn.innerText;
    const ACTION = btnText;
    const res = fetch(`/${ACTION}`, { method: "post" });

    const responseContainer = document.querySelector("#response-container");

    // disable button for a bit
    btn.disabled = true;
    responseContainer.innerText = responseText[ACTION];
    btn.innerText = ACTION === "start" ? "stop" : "start";

    setTimeout(() => {
      responseContainer.innerText = responseText[`after-${ACTION}`];
      if (btn.innerText === "stop") {
        btn.disabled = false;
      } else {
        location.reload();
      }
    }, 2000);

    // toggle button text
  });

socket.on("new_db_add", msg => {
  let newLi = document.createElement("li");
  newLi.innerText = `${msg.data}`;
  document.getElementById("response-container").append(newLi);
});
