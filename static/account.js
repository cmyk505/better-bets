// prettier-ignore
const getAccountStats = (async () => {
  // makes get request to our server, which will then query database to get information about user's betting history. Once we have that we can do fun things like making charts
  const userData = await fetch("/account/get-account-history").then(res =>
    res.json()
  );

  const {win, loss} = userData;

  const labels = ["Win", "Loss"];
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Results - all-time",
        backgroundColor: ["rgb(100, 200, 20)", "rgb(255, 99, 132)"],
        borderColor: "rgb(100,100,100)",
        data: [win, loss],
      },
    ],
  };
  const config = {
    type: "doughnut",
    data,
    options: { maintainAspectRatio: false, animateRotate: true},
  };
  
  const myChart = new Chart(document.getElementById("myChart"), config);  
})();
