var item_list = [];

$( "#add-item" ).click(function() {

    var item = $('#item-input').val();
    var regex = "^https://www.skroutz.gr";
    var valid_url = item.match(regex);

    if (!valid_url){
        alert("μη αποδεκτό URL");
        return;
    }
    $("#items-list").removeClass('hide');
    $("#calculate").removeClass('hide');

    item_list.push(item);

    var body = $("#output-table").find('tbody');

    var row = $('<tr></tr>');
    var cell = $('<td></td>').text(item_list.length);
    row.append(cell);
    var cell = $('<td></td>').text(item);
    row.append(cell);

    body.append(row);
    $('#item-input').val('')
});

$( "#calculate" ).click(function() {

    $("#results-row").removeClass('hide');
    $("#results").empty();

    var data = {
        items_url_list: item_list
    }

// for testing
//    $.ajax({
//      method: "get",
//      url: "find_best",
//      contentType: "application/json; charset=utf-8",
//    })
    $.ajax({
      method: "POST",
      url: "store",
      dataType: 'json',
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data)
    })
      .done(function( msg ) {
        msg.forEach(function(entry){
            var table = $('<table></table>').addClass('table table-striped');

            var header = $('<thead></thead>');
            var header_entry = $('<th></th>').text(entry.shop_name);
            header.append(header_entry);
            table.append(header);

            var body = $('<tbody></tbody>');
            table.append(body);

            var row = $('<tr></tr>');
            var cell = $('<td></td>').addClass('bar').text("τιμή");
            row.append(cell);
            var cell = $('<td></td>').addClass('bar').text(entry.items_price);
            row.append(cell);
            body.append(row);

            var row = $('<tr></tr>').addClass('bar');
            var cell = $('<td></td>').addClass('bar').text("μεταφορικά");
            row.append(cell);
            var cell = $('<td></td>').addClass('bar').text(entry.metaforika);
            row.append(cell);
            body.append(row);

            var row = $('<tr></tr>').addClass('bar');
            var cell = $('<td></td>').addClass('bar').text("αντικαταβολή");
            row.append(cell);
            var cell = $('<td></td>').addClass('bar').text(entry.antikatavoli);
            row.append(cell);
            body.append(row);

            var row = $('<tr></tr>').addClass('bar');
            var cell = $('<td></td>').addClass('bar').text("αριθμός προϊόντων");
            row.append(cell);
            var cell = $('<td></td>').addClass('bar').text(entry.items_length);
            row.append(cell);
            body.append(row);

            var row = $('<tr></tr>').addClass('bar');
            var cell = $('<td></td>').addClass('bar').text("προϊόντα");
            row.append(cell);

            var cell = $('<td></td>').addClass('with-new-lines').text(entry.items_names.join('\n'));
            row.append(cell);
            body.append(row);

            $('#results').append(table);
      });
    });
});
