"use strict";

var connection = new signalR.HubConnectionBuilder().withUrl("/chatHub").build();

//Disable send button until connection is established
document.getElementById("sendButton").disabled = true;

connection.on("ReceiveMessage", function (user, stats) {

    if (config.data.datasets.length > 0) {
        config.data.labels.push("");
        config.data.datasets[0].data.push(stats.cpu );
        config.data.datasets[1].data.push(stats.ram  );
        config.data.datasets[2].data.push(stats.disk  );

        window.myLine.update();
    }
});

connection.start().then(function () {
    document.getElementById("sendButton").disabled = false;
}).catch(function (err) {
    return console.error(err.toString());
});

document.getElementById("sendButton").addEventListener("click", function (event) {
    var user = document.getElementById("userInput").value;
    var message = document.getElementById("messageInput").value;
    connection.invoke("SendMessage", user, message).catch(function (err) {
        return console.error(err.toString());
    });
    event.preventDefault();
});

window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};
window.randomScalingFactor = function() {
    return Math.round(Samples.utils.rand(-100, 100));
};
var config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'cpu',
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: [],
            fill: false,
        },
        {
            label: 'RAM',
            backgroundColor: window.chartColors.green,
            borderColor: window.chartColors.green,
            data: [],
            fill: false,
        },{
        label: 'DISK',
        backgroundColor: window.chartColors.blue,
        borderColor: window.chartColors.blue,
        data: [],
        fill: false,
    }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Chart.js Line Chart'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};


window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};