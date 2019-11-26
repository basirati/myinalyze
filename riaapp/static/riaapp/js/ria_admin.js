function addIssueFunction(new_req_text, priority, type, effort, update_table) {
  $.ajax({
    url: '/riaapp/addIssue/',
    data: {
      'req': new_req_text,
      'priority': priority,
      'type': type,
      'effort': effort
    },
    dataType: 'json',
    success: function (data) {
      if (data.successful) {
        if (update_table == true) {
          /*
          $('#reqs_table > tbody').empty();
          var flag = false;
          for (i in data.sortedReqs)
          {
            r = JSON.parse(data.sortedReqs[i]);
            if (r.text == new_req_text) { flag = true; }
            $('#reqs_table > tbody').append('<tr><th>'+r.text+'</th><td>'+ r.indeg +'</td><td>'+ r.outdeg +'</td></tr>');
          }
          if (flag == false) {
            $('#reqs_table > tbody:last-child').append('<tr><th>'+ JSON.parse(data.new_req).id +'</th><th>' + JSON.parse(data.new_req).text+'</th><td>' + JSON.parse(data.new_req).indeg + '</td><td>'+ JSON.parse(data.new_req).outdeg +'</td></tr>');
          }
          */
          id = JSON.parse(data.new_issue).id
          text = JSON.parse(data.new_issue).text
          indeg = JSON.parse(data.new_issue).indeg
          outdeg = JSON.parse(data.new_issue).outdeg
          $('#reqs_table > tbody:last-child').append('<tr><th hidden="true">'+ id +'</th><th>' + text +'</th><td>' + indeg + '</td><td>'+ outdeg +'</td></tr>');
        }
        return true;
      }
      else {
        alert("An error occured!");
        return false;
      }
    }
  });
}  
