
var socket = new WebSocket(
    'ws://localhost:8000' + 
    '/ws/' +
    'stock/' +
    'stock_room/' +
    'NIFTY-RELIANCE-INFY/'   
);

socket.onmessage = function(e) {
    var stocks = JSON.parse(e.data)
    console.log(stocks);

    var str = '<ul>';
    stocks.forEach(element => {
        str += '<li>' + element.company + '&nbsp;&nbsp;' + element.price + '</li>';
    });

    str += '</ul>';
    document.getElementById('mytext').innerHTML = str;
}

// socket.onopen = function(event) {
//     socket.send("NIFTY");
// };

function sendMessageServer() {
    socket.send("NIFTY");
}