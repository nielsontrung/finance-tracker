var monthlyExpensesDom = document.getElementById("monthly-expenses-bar-chart");
var monthlyExpensesChart = echarts.init(monthlyExpensesDom);
var monthlyExpensesOption;
var monthlyExpensesSeries = [];

for (var i = 0; i < monthlyExpenses.length; i++) {
  var temp = {
    name: monthlyExpenses[i][0],
    type: "bar",
    stack: "total",
    emphasis: {
      focus: "series",
    },
    data: monthlyExpenses[i][1],
  };
  monthlyExpensesSeries.push(temp);
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

monthlyExpensesOption = {
  emphasis: {
    itemStyle: {
      shadowBlur: 5,
      shadowOffsetX: 0,
      shadowColor: "rgba(0, 0, 0, 0.5)",
    },
  },
  title: {
    text: "Annual Expenses per Month",
  },
  tooltip: {
    trigger: "item",
  },
  toolbox: {
    feature: {
      saveAsImage: {},
    },
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
  series: monthlyExpensesSeries,
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

if (monthlyExpensesOption && typeof monthlyExpensesOption === "object") {
  monthlyExpensesChart.setOption(monthlyExpensesOption);
  monthlyExpensesChart.on("mouseover", function (event) {
    let year = event.seriesName;
    let month_name = event.name;
    let month_code = getMonthFromString(month_name);
    let inputField = document.getElementsByTagName("input")[0];
    inputField.value = year + month_code;
    inputField.dispatchEvent(new Event("click"));
    inputField.dispatchEvent(new Event("focus"));
    inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
  });
}
