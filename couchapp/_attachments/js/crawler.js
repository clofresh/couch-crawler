$(document).ready(function() {
  var q = $.query.get('q');
  
  if (q) {
    $('#input_q').attr('value', q);
  
    $.getJSON('/crawler/_fti/crawler/all' + $.query.toString(), 
      function(search_results) {
        $("#search_results_metadata").html(crawler.search_results_metadata(search_results)); 
        $("#search_results").html(crawler.search_results(search_results)); 
        $("#search_pager").html(crawler.search_pager(search_results, $.query)); 
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
  
  search_pager: function(data, search_query) {
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
          var skip = i * search_query.get('limit');
          return $.mustache(
            '<a href="index.html{{query}}" class="pager_link">{{page_num}}</a>', 
            {
              "page_num": page_num, 
              "query": search_query.set('skip', skip).toString()
            }
          );

        }
    }).join(" | ")
  }
}



