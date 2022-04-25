var categoryDom = document.getElementById('category-bar-chart');
var categoryChart = echarts.init(categoryDom);
var categoryOption;
var categorySeries = [];
var yearlyCategoryData = category_stats[2];
for (var i = 0; i < yearlyCategoryData.length; i++) {
  var temp = {
    name: yearlyCategoryData[i][0],
    type: 'bar',
    stack: 'total',
    emphasis: {
      focus: 'series',
    },
    data: yearlyCategoryData[i][1],
  };
  categorySeries.push(temp);
}

categoryOption = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      // Use axis to trigger tooltip
      type: 'shadow', // 'shadow' as default; can also be 'line' or 'shadow'
    },
  },
  legend: {
    orient: 'horizontal',
    left: 'center',
  },
  grid: {
    left: '3%',
    right: '4%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
  },
  yAxis: {
    type: 'category',
    data: [
      'withdrawal',
      'utilities',
      'travel',
      'restaurants',
      'personal care',
      'mobile',
      'loans',
      'investments',
      'home',
      'healthcare',
      'groceries',
      'general',
      'gas',
      'fee',
      'fine',
      'e transfers',
      'entertainment',
      'electronics',
      'education',
      'clothing',
      'automotive',
    ],
  },
  series: categorySeries,
};

if (categoryOption && typeof categoryOption === 'object') {
  categoryChart.setOption(categoryOption);
  categoryChart.on('mouseover', function (event) {
    let category = event.name;
    let inputField = document.getElementsByTagName('input')[0];
    inputField.value = category;
    inputField.dispatchEvent(new Event('click'));
    inputField.dispatchEvent(new Event('focus'));
    inputField.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
  });
}
