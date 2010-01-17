function(doc) {
  var output = new Document();
  var valid_fields = {
    mod_datetime: {
        field: "mod_datetime",
        store: "yes",
        index: "analyzed"
    },

    title: {
      field: "title",
      store: "yes",
      index: "analyzed"
    },

    url: {
        field: "url",
        store: "yes",
        index: "analyzed"
    },
    
    contents:       {
        field: "contents",
        store: "no",
        index: "analyzed"
    }
  };
  
  for (var field in valid_fields) {
    output.add(doc[field], valid_fields[field]);
  }
  
  return output;
}
