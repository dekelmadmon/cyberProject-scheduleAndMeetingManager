const numCellsToUpdate = 7
let table = $('#schedule')
let headerRow = $('<tr id="schedule-header"></tr>')
let contentRow = $('<tr></tr>')

for (let i = 0; i < numCellsToUpdate; i++) {
  headerRow.append($('<th id="header-' + i + '"></th>'))
  contentRow.append($('<td id="cell-' + i + '"></td>'))
}

table.append(headerRow)
table.append(contentRow)
