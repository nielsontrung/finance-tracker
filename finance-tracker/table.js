$(document).ready(function () {
  $('#table').DataTable({
    data: tableData,
    columns: [
      { title: 'id' },
      { title: 'account' },
      { title: 'date' },
      { title: 'year' },
      { title: 'month' },
      { title: 'description' },
      { title: 'category' },
      { title: 'amount' },
    ],
    fixedHeader: true,
    info: false,
    ordering: true,
    scrollY: '85vh',
    lengthMenu: [
      [50, 75, 100, -1],
      [50, 75, 100, 'All'],
    ],
    buttons: ['columnsToggle'],
  });
});
