let charts_arr = {};

function makeCharts(coins) {

    coins.forEach(function(coin, i, coins) {
        let NewCtx = document.getElementById(coin).getContext("2d");
        let NewChart = new Chart(NewCtx, {
          type: "line",
          options: {
            responsive: true,
            title: {
              display: false,
              text: ""
            }
          }
        });
        charts_arr[coin] = NewChart;
    });
}

$(document).ready(function() {

    $.ajax({
        url: "/charts/options/",
        type: "GET",
        dataType: "json",
        success: (jsonResponse) => {
            let days = [];
            jsonResponse.coins.forEach(function(coin, i, coins) {
                let first_option = new Option(0, 0);
                let j = 0;
                jsonResponse.options.forEach(option => {
                     if (j == 0) {days.push(option);}
                     $(`#${coin}_days`).append(new Option(option, option));
                     j++;
                });

            });
            makeCharts(jsonResponse.coins);
            loadAllCharts(days, jsonResponse.coins);
        },
        error: () => {alert("error");}
    })
});

$('.settings').click(function(eventObject){
    loadChart(charts_arr[eventObject.currentTarget.name], `/charts/${eventObject.currentTarget.name}/${$(`#${eventObject.currentTarget.name}_days`).val()}`);
});

function loadChart(chart, endpoint) {
    $.ajax({
        url: endpoint,
        type: "GET",
        dataType: "json",
        success: (jsonResponse) => {
//            alert(jsonResponse)
            const title = jsonResponse.title;
            const labels = jsonResponse.data.labels;
            const datasets = jsonResponse.data.datasets;
            chart.data.datasets = [];
            chart.data.labels = [];
            chart.options.title.text = title;
            chart.options.title.display = true;
            chart.data.labels = labels;
            datasets.forEach(dataset => {
            chart.data.datasets.push(dataset);
            });
            chart.update();
        }
    })
}

function loadAllCharts(days, coins) {
    let i = 0;
    for (let key in charts_arr) {
        loadChart(charts_arr[key], `/charts/${key}/${days[i]}`);
        i++;
    }
}
