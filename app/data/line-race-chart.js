var lineRaceDom = document.getElementById("line-race-chart");
var lineRaceChart = echarts.init(lineRaceDom);
var lineChartOption;

run(lineRaceData);

function run(lineRaceData) {
  const TRANSACTION_TYPES = ["earnings", "expenses"];
  const datasetWithFilters = [];
  const seriesList = [];
  echarts.util.each(TRANSACTION_TYPES, function (transaction) {
    var color = transaction === "earnings" ? "#91cc75" : "#ee6666";

    var datasetId = "dataset_" + transaction;
    datasetWithFilters.push({
      id: datasetId,
      fromDatasetId: "dataset_raw",
      transform: {
        type: "filter",
        config: {
          and: [
            { dimension: "amount", gte: 0 },
            { dimension: "type", "=": transaction },
          ],
        },
      },
    });
    seriesList.push({
      color: color,
      type: "line",
      smooth: true,
      datasetId: datasetId,
      showSymbol: false,
      name: transaction,
      endLabel: {},
      labelLayout: {
        moveOverlap: "shiftY",
      },
      emphasis: {
        focus: "series",
      },
      encode: {
        x: "date",
        y: "amount",
        label: ["type", "amount"],
        itemName: "date",
        tooltip: ["amount"],
      },
    });
  });
  lineChartOption = {
    animationDuration: 5000,
    dataset: [
      {
        id: "dataset_raw",
        source: lineRaceData,
      },
      ...datasetWithFilters,
    ],
    title: {
      text: "Lifetime Earnings and Expenses",
    },
    toolbox: {
      feature: {
        saveAsImage: {},
      },
    },
    tooltip: {
      order: "valueDesc",
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      nameLocation: "middle",
      name: "Time",
    },
    yAxis: {
      nameLocation: "middle",
      name: "Income",
    },
    grid: {
      right: 140,
    },
    series: seriesList,
  };
  lineRaceChart.on("updateAxisPointer", function (event) {
    var xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      var dimension = xAxisInfo.value + 1;
      lineRaceChart.setOption({
        series: {
          id: "lineRace",
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
      inputField.value = getMonth(xAxisInfo.value);
      inputField.dispatchEvent(new Event("click"));
      inputField.dispatchEvent(new Event("focus"));
      inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
    }
  });
  lineRaceChart.setOption(lineChartOption);
}

if (lineChartOption && typeof lineChartOption === "object") {
  lineRaceChart.setOption(lineChartOption);
}

function getMonth(value) {
  const zeroPad = (num, places) => String(num).padStart(places, "0");
  value = Number(value);
  var month = (value % 12) + 1;
  var year = Number(startYear) + Math.floor(value / 12);
  return year + "/" + zeroPad(month, 2);
}
