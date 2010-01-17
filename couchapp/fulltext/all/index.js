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
  
  output.add(
    doc["title"] + "\n" + doc["contents"], 
    {field: "default", store: "no", index: "analyzed"}
  );
  
  output.add(doc["contents"].substr(0, 140), {field: "snippet", store: "yes", index: "no"});
  
  return output;
}
