var monthDom = document.getElementById('monthly-earnings-bar-chart');
var monthlyEarningsChart = echarts.init(monthDom);
var monthlyEarningsOption;
var monthlyEarningsSeries = [];

for (var i = 0; i < monthlyEarnings.length; i++) {
  var temp = {
    name: monthlyEarnings[i][0],
    type: 'bar',
    stack: 'total',
    emphasis: {
      focus: 'series',
    },
    data: monthlyEarnings[i][1],
  };
  monthlyEarningsSeries.push(temp);
}

monthlyEarningsOption = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },
  legend: {
    orient: 'horizontal',
    left: 'center',
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
  },
  yAxis: {
    type: 'category',
    data: [
      'Dec',
      'Nov',
      'Oct',
      'Sep',
      'Aug',
      'Jul',
      'Jun',
      'May',
      'Apr',
      'Mar',
      'Feb',
      'Jan',
    ],
  },
  series: monthlyEarningsSeries,
};

function getMonthFromString(mon) {
  let month = new Date(Date.parse(mon + ' 1, 2012')).getMonth() + 1;
  month = '' + month;
  if (month.length < 2) {
    month = '0' + month;
  }
  month = '/' + month + '/';
  return month;
}

if (monthlyEarningsOption && typeof monthlyEarningsOption === 'object') {
  monthlyEarningsChart.setOption(monthlyEarningsOption);
  monthlyEarningsChart.on('mouseover', function (event) {
    let month_name = event.name;
    let month_code = getMonthFromString(month_name);
    let inputField = document.getElementsByTagName('input')[0];
    inputField.value = month_code + ' deposit';
    inputField.dispatchEvent(new Event('click'));
    inputField.dispatchEvent(new Event('focus'));
    inputField.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
  });
}
