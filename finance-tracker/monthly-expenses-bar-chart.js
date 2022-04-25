var monthDom = document.getElementById('monthly-expenses-bar-chart');
var monthlyExpensesChart = echarts.init(monthDom);
var monthlyExpensesOption;
var monthlyExpensesSeries = [];

for (var i = 0; i < monthlyExpenses.length; i++) {
  var temp = {
    name: monthlyExpenses[i][0],
    type: 'bar',
    stack: 'total',
    emphasis: {
      focus: 'series',
    },
    data: monthlyExpenses[i][1],
  };
  monthlyExpensesSeries.push(temp);
}

monthlyExpensesOption = {
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
  series: monthlyExpensesSeries,
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

if (monthlyExpensesOption && typeof monthlyExpensesOption === 'object') {
  monthlyExpensesChart.setOption(monthlyExpensesOption);
  monthlyExpensesChart.on('mouseover', function (event) {
    let month_name = event.name;
    let month_code = getMonthFromString(month_name);
    let inputField = document.getElementsByTagName('input')[0];
    inputField.value = month_code;
    inputField.dispatchEvent(new Event('click'));
    inputField.dispatchEvent(new Event('focus'));
    inputField.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
  });
}
