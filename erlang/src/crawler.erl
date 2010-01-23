-module(crawler).

-export([start/0, crawl/2, seen_already_loop/1, processor_loop/0, indexer_loop/1, crawl_test/0]).

seen_already_loop(Urls) ->
  receive
    {add, Url} ->
      Urls2 = sets:add_element(Url, Urls);
    {is_element, Url, SenderPid} ->
      SenderPid ! {is_element, sets:is_element(Url, Urls)},
      Urls2 = Urls
  end,
  seen_already_loop(Urls2).

processor_loop() ->
  receive
    {Url, MaxDepth} ->
      Html = fetch(Url),
      indexer ! {index, Url, Html},

      if 
        MaxDepth > 0 ->
          Urls = crawler_html:find_links(Url, Html),
          spawn(?MODULE, crawl, [Urls, MaxDepth - 1]);
        true ->
          ok
      end
  end,
  processor_loop().

indexer_loop(Connection) ->
  receive
    {index, Url, Html} ->
      Db = couchbeam_db:open(Connection, "crawler_erl"),
      crawler_indexer:index(Db, Url, Html)
  end,
  indexer_loop(Connection).
  
start() ->
  couchbeam:start(),
  Connection = couchbeam_server:start_connection_link(),

  ok = inets:start(),
  true = register(seen_already, spawn(?MODULE, seen_already_loop, [sets:new()])),
  true = register(processor, spawn(?MODULE, processor_loop, [])),
  true = register(indexer, spawn(?MODULE, indexer_loop, [Connection])).

crawl([], MaxDepth) ->
  ok;

crawl([Url], MaxDepth) ->
  process(Url, MaxDepth);

crawl([Url | Rest], MaxDepth) ->
  process(Url, MaxDepth),
  crawl(Rest, MaxDepth).


process(Url, MaxDepth) ->
  seen_already ! {is_element, Url, self()},
  
  receive
    {is_element, false} ->
      io:format("Crawling ~p~n", [Url]),
      processor ! {Url, MaxDepth},
      ok;
    {is_element, true} ->
      ok;
    Error ->
      io:format("process error: ~p~n", [Error])
  end.

fetch(Url) ->
  case http:request(Url) of 
    {ok, {{_, 200, _}, Headers, Body}} ->
      case proplists:get_value("content-type", Headers) of
        undefined   -> "";
        ContentType -> 
          case string:substr(ContentType, 1, 9) of
            "text/html" -> Body;
            _           -> ""
          end
      end;
    {ok, {{_, _Non200, _}, _, _}} ->
      "";
    {_NotOk, _} ->
      ""
  end.

crawl_test() ->
  start(),
  crawl(["http://www.nytimes.com/"], 2).
  
  
