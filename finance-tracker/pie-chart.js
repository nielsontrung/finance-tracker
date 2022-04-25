var pieDom = document.getElementById('pie-chart');
var pieChart = echarts.init(pieDom);
var datasetSource = [];

var datasetSourceHeader = [];
datasetSourceHeader.push('category');
for (var i = startYear; i <= endYear; i++) {
  datasetSourceHeader.push('' + i);
}

var categoricalExpenses;

datasetSource.push(datasetSourceHeader);

// transactions with earnings
const earnings = ['deposit', 'government', 'other'];

for (var i = 0; i < categoricalExpenses.length; i++) {
  if (!earnings.includes(categoricalExpenses[i][0])) {
    datasetSource.push(categoricalExpenses[i]);
  }
}

function getSeriesConfig() {
  var series = [];
  for (var i = 0; i < categories.length; i++) {
    series.push({
      type: 'line',
      smooth: true,
      seriesLayoutBy: 'row',
      emphasis: { focus: 'series' },
    });
  }
  series.push({
    type: 'pie',
    id: 'pie',
    radius: '35%',
    center: ['55%', '30%'],
    emphasis: {
      focus: 'self',
    },
    label: {
      formatter: '{b}: {@' + startYear + '} ({d}%)',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: () => {
        console.log(this);
        return '{b0}: {c0}<br />{b1}: {c1}';
      },
    },
    encode: {
      itemName: 'category',
      value: '' + startYear,
      tooltip: '' + startYear,
    },
  });

  return series;
}

var categoryOption;
var startYear = '' + startYear;
setTimeout(function () {
  categoryOption = {
    dataset: {
      source: datasetSource,
    },
    grid: { top: '65%' },
    legend: {
      left: 'left',
      orient: 'vertical',
    },
    series: getSeriesConfig(),
    tooltip: {
      trigger: 'axis',
      showContent: false,
    },
    xAxis: { type: 'category' },
    yAxis: { gridIndex: 0 },
  };

  pieChart.on('updateAxisPointer', function (event) {
    var xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      var dimension = xAxisInfo.value + 1;
      pieChart.setOption({
        series: {
          id: 'pie',
          label: {
            formatter: '{b}: {@[' + dimension + ']} ({d}%)',
          },
          encode: {
            value: dimension,
            tooltip: dimension,
          },
        },
      });
      let inputField = document.getElementsByTagName('input')[0];
      inputField.value = Number(xAxisInfo.value) + Number(startYear);
      console.log(event);
      inputField.dispatchEvent(new Event('click'));
      inputField.dispatchEvent(new Event('focus'));
      inputField.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
    }
  });
  pieChart.setOption(categoryOption);
});

if (categoryOption && typeof categoryOption === 'object') {
  pieChart.setOption(categoryOption);
}
