var chartDom = document.getElementById("area-chart");
var areaChart = echarts.init(chartDom);
var areaChartOption;

let base = +new Date(1968, 9, 3);
let oneDay = 24 * 3600 * 1000;
let areaChartDate = [];
let areaChartData = [Math.random() * 300];
for (let i = 1; i < 20000; i++) {
  var now = new Date((base += oneDay));
  areaChartDate.push(
    [now.getFullYear(), now.getMonth() + 1, now.getDate()].join("/")
  );
  areaChartData.push(
    Math.round((Math.random() - 0.5) * 20 + areaChartData[i - 1])
  );
}
areaChartOption = {
  tooltip: {
    trigger: "axis",
    position: function (pt) {
      return [pt[0], "10%"];
    },
  },
  title: {
    left: "center",
    text: "Large Area Chart",
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: "none",
      },
      restore: {},
      saveAsImage: {},
    },
  },
  xAxis: {
    type: "category",
    boundaryGap: false,
    data: areaChartDate,
  },
  yAxis: {
    type: "value",
    boundaryGap: [0, "100%"],
  },
  dataZoom: [
    {
      type: "inside",
      start: 0,
      end: 10,
    },
    {
      start: 0,
      end: 10,
    },
  ],
  series: [
    {
      name: "Fake Data",
      type: "line",
      symbol: "none",
      sampling: "lttb",
      itemStyle: {
        color: "rgb(255, 70, 131)",
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: "rgb(255, 158, 68)",
          },
          {
            offset: 1,
            color: "rgb(255, 70, 131)",
          },
        ]),
      },
      data: areaChartData,
    },
  ],
};

areaChartOption && areaChart.setOption(areaChartOption);
areaChart.on("mouseover", function (event) {
  console.log(event);
  let inputField = document.getElementsByTagName("input")[0];
  inputField.value = getMonth(xAxisInfo.value);
  inputField.dispatchEvent(new Event("click"));
  inputField.dispatchEvent(new Event("focus"));
  inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
});
