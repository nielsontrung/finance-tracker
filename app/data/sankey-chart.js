var sankeyDom = document.getElementById("sankey-chart");
var sankeyChart = echarts.init(sankeyDom);
var option;

sankeyChart.showLoading();
$.get("./data/revenue.json", function (data) {
  sankeyChart.hideLoading();
  sankeyChart.setOption(
    (option = {
      title: {
        text: "Lifetime Revenue",
      },
      toolbox: {
        feature: {
          saveAsImage: {},
        },
      },
      tooltip: {
        trigger: "item",
        triggerOn: "mousemove",
      },
      series: [
        {
          type: "sankey",
          data: data.nodes,
          links: data.links,
          emphasis: {
            focus: "adjacency",
          },
          lineStyle: {
            color: "gradient",
            curveness: 0.5,
          },
        },
      ],
    })
  );
});
sankeyChart.on("mouseover", function (event) {
  let category = event.name;
  console.log(category);
  if (category == "Net Revenue" || category.includes(">")) {
    category = "";
  }
  let inputField = document.getElementsByTagName("input")[0];
  inputField.value = category;
  inputField.dispatchEvent(new Event("click"));
  inputField.dispatchEvent(new Event("focus"));
  inputField.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter" }));
});

option && sankeyChart.setOption(option);
