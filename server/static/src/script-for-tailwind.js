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
const windowHeight = document.documentElement.clientHeight;
$("#table-container").height(windowHeight * 0.7);

function showColumn(value, countRowSpan = 1, borderLeft = 1, borderTop = 1, borderRight = 1, borderBottom = 1) {
  let localContent = "";
  //rowspan="${countRowSpan}"

  if (countRowSpan == 1) {
    localContent += `<div class="bg-gray-50 row-span-${countRowSpan} border-r px-2">`;
  } else {
    localContent += `<div class="bg-gray-50 row-span-${countRowSpan} flex justify-center items-center border-r px-2">`;
  }
  localContent += `<div style="font-size: 20px" class="flex justify-center items-center py-2">${value}</div>`;
  if (countRowSpan == 1) {
    localContent += `<div class="w-full border-b"></div>`;
  }
  localContent += "</div>";

  return localContent;
}

const tableContainer = $("#table-container .tbody");
function showTable(dataShow) {
  let content = "";
  dataShow.forEach((item) => {
    const countRowSpan = item.exchanges.length;
    let currencyShow = true;
    content += "<div class='grid grid-cols-6 overflow-hidden mb-4 border-4 rounded-[20px]'>";
    item.exchanges.forEach((exchange) => {
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
      content += showColumn(exchange.liquidity);
      if (currencyShow) {
        // spread
        content += showColumn(item.spread, countRowSpan, (borderRight = 0));
        currencyShow = false;
      }
    });
    content += "</div>";
  });
  tableContainer.html("");
  tableContainer.append(content);
}

// data
let data = [];
let updateDate = "";

// Вариант 1
function getData(action = "default", date = 'g413gg', filter = 'g413gg') {
  $(".tbody").html(`<div class="loading"><img src="../static/src/loading.gif"></div>`);
  if (updateDate == "") {
    updateDate = date;
  }
  if (filtersArr.length > 0) {
    filter = filtersArr.join(",");
  } //185.182.185.203
  $.getJSON(`http://185.182.185.203/get?action=${action}&date=${updateDate}&filter=[${filter}]`, function (data) {
    if (updateDate == data.updateDate && action == "update") {
      $("#toast").show();
      setTimeout(() => $("#toast").hide(), 9000);
    }
    updateDate = data.updateDate;
    data = data.currencies;

    /*if (filtersArr.length > 0) {
      data = data.map((item) => {
        return {
          currency: item.currency,
          spread: item.spread,
          exchanges: item.exchanges.filter((exchange) => filtersArr.includes(exchange.name)),
        };
      });
    }*/

    showTable(data);
  });
}

function getUpdateData() {
  getData("update");
  //getData(date, filter);
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
updateButton.addEventListener("click", getUpdateData);

// auto update
let autoUpdate = false;
let updateInterval = "";
const intervalTime = 60000; // 60 cекунд
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
