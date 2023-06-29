let annotations = [`долларов`, `евро`, `рублей`]
let u_balance = 0;
let u_coin_count = 0;

$(document).ready(function() {
    $.ajax({
        url: "/price/",
        type: "GET",
        dataType: "json",
        success: (jsonResponse) => {
            updateTokensCount();
            let price_list = [];
            let prices = jsonResponse.prices;
            for (coin in jsonResponse.prices) {
                price_list.push(coin);
            }
            price_list.forEach(function(p, i, list) {
                let j = 0;
                let curr_coin = jsonResponse.coins[i]
                for (currency in prices[curr_coin]) {
                    let div = document.createElement('div');
                    div.innerHTML = prices[curr_coin][currency] + ` ` + annotations[j];
                    $(`#${curr_coin}_price`).append(div);
                    j++;
                }
                $(`#${curr_coin}_buy`).click(function(){
                    openModal(curr_coin, prices[curr_coin][`usd`], 'buy');
                });
                $(`#${curr_coin}_sell`).click(function(){
                    openModal(curr_coin, prices[curr_coin][`usd`], 'sell');
                });
            });
        },
        error: () => {alert("error");}
    })
});


function updateTokensCount(){
    $.ajax({
        url: "/balance/",
        type: "GET",
        async: false,
        dataType: "json",
        success: (jsonResponse) => {
            let j = 0;
            for (coin in jsonResponse.coin_count) {
                $(`#${coin}_count`).empty();
                let div = document.createElement('div');
                div.innerHTML = jsonResponse.coin_count[coin];
                $(`#${coin}_count`).append(div);
                j++;
            }
        },
        error: () => {alert("error");}
    })
}


function openModal(coin, price, type){
    let dialog = document.getElementById(`${coin}_${type}_dialog`);
    let count_input = document.getElementById(`${coin}_${type}_count`);
    document.getElementById(`${coin}_${type}_close`).onclick = function () {
        dialog.close()
    }
    document.getElementById(`${coin}_${type}_accept`).onclick = function () {
        get_balance_data(coin);
        let count_value = $(`#${coin}_${type}_count`).val();
        let check = checkOperationAvailable(coin, price, count_value, type);
        if (check == 'available' && checkInputValid(count_value)){
            if (type == 'buy')
                $(`#balance`).html(`Баланс: ${Math.floor(u_balance - count_value * price)}` + '$');
            else
                $(`#balance`).html(`Баланс: ${Math.floor(u_balance + count_value * price)}` + '$');
            $.ajax({
                url: "/market/",
                type: 'POST',
                dataType: "json",
                async: false,
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                data: {'coin': coin, 'count': count_value, 'price': price, 'type': type},
                success: function(){

                }
            })
            updateTokensCount();
        } else if (check == 'coin_lack') {
            alert("операция невозможна, недостаточно токенов");
        } else if (check == 'balance_lack') {
            alert("операция невозможна, недостаточно средств");
        }
        dialog.close()
    }
    dialog.show();
}


function get_balance_data(coin){
    $.ajax({
        url: "/balance/",
        type: "GET",
        async: false,
        dataType: "json",
        success: (jsonResponse) => {
            success = true;
            u_balance = jsonResponse.balance;
            if (jsonResponse["coin_count"][coin])
                u_coin_count = jsonResponse["coin_count"][coin];
        },
        error: () => {res = [0, 0];}
    })
}


function checkOperationAvailable(coin, price, count, type){
    if (type == 'buy') {
        let all_price = count * price;
        if (u_balance < all_price)
            return "balance_lack";
    } else {
//        alert([coin, u_coin_count, count])
        if (u_coin_count < count)
            return "coin_lack";
    }
    return "available";
}


$('#search').keyup(function () {
    let input = document.getElementById("search");
    let search = input.value.toUpperCase();
    let table = document.getElementById("main_table");
    let rows = table.getElementsByTagName("tr");

    for (i = 0; i < rows.length; i++) {
        td = rows[i].getElementsByTagName("td")[0];
        if (td) {
             txtValue = td.textContent || td.innerText;
             if (txtValue.toUpperCase().indexOf(search) > -1) {
                 rows[i].style.display = "";
             } else {
                 rows[i].style.display = "none";
             }
        }
    }

});



function checkInputValid(value){
    return /^\d+$/.test(value);
}


function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
