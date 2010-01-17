function(doc) {
  var output = new Document();
  var valid_fields = [
    "mod_datetime",
    "title",
    "url",
    "contents"
  ];
  
  for (var i in valid_fields) {
    var field = valid_fields[i];
    output.add(
      doc[field], 
      {
        field: f,
        store: "yes",
        index: "analyzed"
      }
    )
  }
  
  return output;
}
