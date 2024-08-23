var pieChartDom = document.getElementById("pie-chart");
var pieChart = echarts.init(pieChartDom);
let searchYear = startYear;

function getSeriesConfig() {
  var series = [];
  for (var i = 0; i < pieChartData.length - 1; i++) {
    series.push({
      type: "line",
      stack: "Total",
      areaStyle: {},
      smooth: true,
      seriesLayoutBy: "row",
      emphasis: { focus: "series" },
    });
  }
  series.push({
    id: "pie",
    type: "pie",
    radius: "40%",
    center: ["50%", "35%"],
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: "rgba(0, 0, 0, 0.5)",
      },
    },
    label: {
      formatter: "{b} {@[" + startYear + "]} ({d}%)",
    },
    tooltip: {
      trigger: "item",
      axisPointer: {
        type: "shadow",
      },
    },
    encode: {
      itemName: "Category",
      value: "" + startYear,
      tooltip: "" + startYear,
    },
  });

  return series;
}

var pieChartOption;
var startYear = "" + startYear;

setTimeout(function () {
  pieChartOption = {
    title: { text: "Annual Expenses per Category", top: "1.5%" },
    dataset: {
      source: pieChartData,
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    grid: { top: "60%" },
    legend: {
      top: "5%",
      left: "left",
      orient: "horizontal",
    },
    series: getSeriesConfig(),
    tooltip: {
      trigger: "axis",
      showContent: true,
    },
    xAxis: { type: "category" },
    yAxis: { gridIndex: 0 },
  };

  pieChart.on("updateAxisPointer", function (event) {
    var xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      var dimension = xAxisInfo.value + 1;
      pieChart.setOption({
        series: {
          id: "pie",
          label: {
            formatter: "{b}: {@[" + dimension + "]} ({d}%)",
          },
          encode: {
            value: dimension,
            tooltip: dimension,
          },
        },
      });
      let inputField = document.getElementsByTagName("input")[0];
      searchYear = Number(xAxisInfo.value) + Number(startYear);
      inputField.value = searchYear;
      inputField.dispatchEvent(new Event("click"));
      inputField.dispatchEvent(new Event("focus"));
      inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
    }
  });
  pieChart.on("mouseover", function (event) {
    let category = event.data[0];
    let inputField = document.getElementsByTagName("input")[0];
    inputField.value = searchYear + " " + category;
    inputField.dispatchEvent(new Event("click"));
    inputField.dispatchEvent(new Event("focus"));
    inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
  });
  pieChart.setOption(pieChartOption);
});

if (pieChartOption && typeof pieChartOption === "object") {
  pieChart.setOption(pieChartOption);
}
