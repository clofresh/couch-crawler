function(doc) {
  var output = new Document();
  var valid_fields = [
    "mod_datetime",
    "title",
    "url",
    "contents"
  ];
  
  for (var f in valid_fields) {
    output.add(
      doc[f], 
      {
        field: f,
        store: "yes",
        index: "analyzed"
      }
    )
  }
  
  return output;
}
