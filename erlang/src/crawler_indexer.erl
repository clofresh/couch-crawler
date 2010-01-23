-module(crawler_indexer).
-export([index/3]).

index(Db, Url, Html) ->
  Title    = crawler_html:get_title(Html),
  Contents = crawler_html:find_text_content(Html),

  io:format("Indexing: ~p~n", [Contents]),

  Doc = {[{<<"_id">>,      list_to_binary(Url)},
          {<<"url">>,      list_to_binary(Url)},
          {<<"contents">>, Contents},
          {<<"title">>,    Title}]},

  couchbeam_db:save_doc(Db, Doc).

