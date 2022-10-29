// filters
let filtersArr = [];
const currencyFilters = document.querySelectorAll(".currency-filter input[type='checkbox']");
currencyFilters.forEach((currencyItem) => {
  currencyItem.addEventListener("change", function () {
    if (this.checked) {
      filtersArr.push(this.dataset.currency);
    } else {
      filtersArr = filtersArr.filter((item) => item != this.dataset.currency);
    }
    console.log("filter", filtersArr);
    getData();
  });
});

// table container
function showColumn(value, countRowSpan = 1) {
  let localContent = "";
  localContent += `<td rowspan="${countRowSpan}">`;
  localContent += value;
  localContent += "</td>";

  return localContent;
}

const tableContainer = $("#table-container table tbody");
function showTable(dataShow) {
  let content = "";
  dataShow.forEach((item) => {
    const countRowSpan = item.exchanges.length;
    let currencyShow = true;
    item.exchanges.forEach((exchange) => {
      content += "<tr>";
      // name
      content += showColumn(exchange.name);
      if (currencyShow) {
        // currency
        content += showColumn(item.currency, countRowSpan);
      }

      // price
      content += showColumn(exchange.price);
      // volume
      content += showColumn(exchange.volume);
      // Liq
      content += showColumn(exchange.liq);
      if (currencyShow) {
        // spread
        content += showColumn(item.spread, countRowSpan);
        currencyShow = false;
      }

      content += "</tr>";
    });
  });
  tableContainer.html("");
  tableContainer.append(content);
}

// data
let data = [];
let updateDate = "";

// Вариант 1
function getData() {
  $.getJSON("json/data.json", function (data) {
    updateDate = data.updateDate;
    data = data.currencies;

    if (filtersArr.length > 0) {
      data = data.map((item) => {
        return {
          currency: item.currency,
          spread: item.spread,
          exchanges: item.exchanges.filter((exchange) => filtersArr.includes(exchange.name)),
        };
      });
    }

    showTable(data);
  });
}
/*
// Вариант 2
const url = 'http://example/data';
$.ajax({ 
    type: 'GET', 
    url: url, 
    data: { filtersArr: JSON.stringify(filtersArr)}, 
    dataType: 'json',
    success: function (getData) { 
        data = getData;
        showTable(data);
    }
});*/

getData();

//update button
const updateButton = document.querySelector("#update-button");
updateButton.addEventListener("click", getData);

// auto update
let autoUpdate = false;
let updateInterval = "";
const intervalTime = 10000; // 10 cекунд
const autoUpdateCheckbox = document.querySelector("#auto-update");

autoUpdateCheckbox.addEventListener("change", function () {
  if (this.checked) {
    autoUpdate = true;
    updateInterval = setInterval(() => getData(), intervalTime);
  } else {
    autoUpdate = false;
    clearInterval(updateInterval);
  }
  console.log(autoUpdate);
});
