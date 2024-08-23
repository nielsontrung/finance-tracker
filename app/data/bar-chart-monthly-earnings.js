var monthlyEarningsDom = document.getElementById("monthly-earnings-bar-chart");
var monthlyEarningsChart = echarts.init(monthlyEarningsDom);
var monthlyEarningsOption;
var monthlyEarningsSeries = [];

for (var i = 0; i < monthlyEarnings.length; i++) {
  var temp = {
    name: monthlyEarnings[i][0],
    data: monthlyEarnings[i][1],
    type: "bar",
    stack: "total",
    emphasis: {
      focus: "series",
    },
  };
  monthlyEarningsSeries.push(temp);
}

xAxisLabel = [
  "Dec",
  "Nov",
  "Oct",
  "Sep",
  "Aug",
  "Jul",
  "Jun",
  "May",
  "Apr",
  "Mar",
  "Feb",
  "Jan",
].reverse();

monthlyEarningsOption = {
  emphasis: {
    itemStyle: {
      shadowBlur: 5,
      shadowOffsetX: 0,
      shadowColor: "rgba(0, 0, 0, 0.5)",
    },
  },
  title: {
    text: "Annual Earnings per Month",
    padding: [0, 0, 0, 0],
  },
  toolbox: {
    feature: {
      saveAsImage: {},
    },
  },
  tooltip: {
    trigger: "item",
  },
  legend: {
    orient: "horizontal",
    left: "center",
    top: "7%",
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    top: "17%",
    containLabel: true,
  },
  yAxis: {
    type: "value",
  },
  xAxis: {
    type: "category",
    data: xAxisLabel,
  },
  series: monthlyEarningsSeries,
};

function getMonthFromString(mon) {
  let month = new Date(Date.parse(mon + " 1, 2012")).getMonth() + 1;
  month = "" + month;
  if (month.length < 2) {
    month = "0" + month;
  }
  month = "/" + month + "/";
  return month;
}

if (monthlyEarningsOption && typeof monthlyEarningsOption === "object") {
  monthlyEarningsChart.setOption(monthlyEarningsOption);
  monthlyEarningsChart.on("mouseover", function (event) {
    let year = event.seriesName;
    let month_name = event.name;
    let month_code = getMonthFromString(month_name);
    let inputField = document.getElementsByTagName("input")[0];
    inputField.value = year + month_code + " deposit";
    inputField.dispatchEvent(new Event("click"));
    inputField.dispatchEvent(new Event("focus"));
    inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
  });
}
