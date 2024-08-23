$(document).ready(function () {
  $('#table').DataTable({
    data: tableData,
    columns: [
      { title: 'id' },
      { title: 'account' },
      { title: 'date' },
      { title: 'year' },
      { title: 'month' },
      { title: 'category' },
      { title: 'description' },
      { title: 'amount' },
      { title: 'sourceFile' },

    ],
    fixedHeader: true,
    info: false,
    responsive: true,
    ordering: true,
    scrollY: '85vh',
    lengthMenu: [
      [50, 75, 100, -1],
      [50, 75, 100, 'All'],
    ],
    buttons: ['columnsToggle'],
  });
});
