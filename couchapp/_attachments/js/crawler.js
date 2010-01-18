$(document).ready(function() {
  var q = $.query.get('q');
  $('#input_q').attr('value', q);
  
  if (q) {
    var url = '/crawler/_fti/crawler/all' + $.query.toString();
    $.getJSON(url, 
      function(data) {
        var updates = [
          "search_results_metadata",
          "search_results",
          "search_pager"
        ];
      
        _(updates).map(function(section) { 
          $("#" + section).html(crawler[section](data)) 
        });
    });
  }
});


var crawler = {
  search_results_metadata: function(data) {
    return $.mustache(
      "Results {{from}} - {{to}} of {{total_rows}} ({{duration}} seconds)",
      {
        from:       data.skip + 1,
        to:         Math.min(data.skip + data.limit, data.total_rows),
        total_rows: data.total_rows,
        duration:   ((data.search_duration 
                        + data.fetch_duration) / 1000).toFixed(3)
      }
    )
  },
  
  search_results: function(data) {
    return $.mustache(
      [
        '{{#rows}}',
          '<article class="search_result">',
            '<header><h1><a href="{{url}}">{{title}}</a></h1></header>',
            '<p>{{snippet}}</p>',
            '<footer>{{url}}</footer>',
          '</article>',
        '{{/rows}}'
      ].join("\n"),
      {rows: _(data.rows).map( function(row) { return row.fields } )}
    )
  },
  
  search_pager: function(data) {
    var num_pages = Math.ceil(data.total_rows / data.limit);
    
    if (num_pages == 1) { 
      return ''; 
    }
    
    var current_page = parseInt(data.skip / data.limit) + 1;
    
    return _(_.range(num_pages)).map(function(i) {
        var page_num = i + 1;

        if (page_num == current_page) {
          return page_num;

        } else {
          var skip = i * $.query.get('limit');
          return $.mustache(
            '<a href="index.html{{query}}" class="pager_link">{{page_num}}</a>', 
            {
              "page_num": page_num, 
              "query": $.query.set('skip', skip).toString()
            }
          );

        }
    }).join(" | ")
  }
}



