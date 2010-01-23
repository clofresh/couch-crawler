-module(crawler_html).
-export([find_links/2, find_text_content/1, get_title/1]).

find_links(Url, Html) ->
  {Scheme, Netloc, _, _, _} = mochiweb_util:urlsplit(Url),
  
  try
    {Element, Attrs, Children} = mochiweb_html:parse(Html),

    sets:to_list(lists:foldl(
      fun(BinLink, Links) -> 
        Link = binary_to_list(BinLink),

        UrlParts = try
          mochiweb_util:urlsplit(Link)
        catch _Class:_Error ->
          {}
        end,
      
        case UrlParts of
          {_, Netloc, _, _, _} ->
            sets:add_element(Link, Links);

          {[], [], [], [], _Fragment} ->
            Links;
        
          {[], [], Path, Query, _} ->
            sets:add_element(
              mochiweb_util:urlunsplit({Scheme, Netloc, Path, Query, []}), 
              Links
            );
        
          Error ->
            io:format("Skipping link: ~p~n", [Error]),
            Links
          
        end
      end,
      sets:new(),
      find_links({Element, Attrs}, Children, []))
    )
  catch Class:Error ->
    io:format("[~p:~p] Could not parse document at ~p~n", [Class, Error, Url]),
    []
  end.

find_links({<<"a">>, Attrs}, [], Links) ->
  append_link(Attrs, Links);

find_links(_Element, [], Links) ->
  Links;

find_links({<<"a">>, Attrs}, Children, Links) ->
  NextLinks = append_link(Attrs, Links),

  [Head | Tail] = Children,
  case Head of
    {NextElement, NextAttrs, NextChildren} ->
      find_links({NextElement, NextAttrs}, NextChildren ++ Tail, NextLinks);
    NextElement ->
      find_links({NextElement, []}, Tail, NextLinks)
  end;

find_links(_Element, Children, Links) ->
  [Head | Tail] = Children,
  case Head of
    {NextElement, NextAttrs, NextChildren} ->
      find_links({NextElement, NextAttrs}, NextChildren ++ Tail, Links);
    NextElement ->
      find_links({NextElement, []}, Tail, Links)
  end.

append_link(Attrs, Links) ->
  case proplists:get_value(<<"href">>, Attrs) of 
    undefined ->
      Links;
    Link ->
      case proplists:get_value(<<"rel">>, Attrs) of
        <<"nofollow">> -> Links;
        _              -> [Link] ++ Links
      end
  end.

find_text_content(Html) ->
  try
    {Element, Attrs, Children} = mochiweb_html:parse(Html),
    find_text_content({Element, Attrs}, Children, <<"">>)
  catch _:_ ->
    io:format("Could not parse document: ~p~n", [Html]),
    <<"">>
  end.

find_text_content(_Element, [], Content) ->
  Content;

find_text_content(Element, Children, Contents) ->
  [Head | Tail] = Children,
  case Head of
    {NextElement, NextAttrs, NextChildren} ->
      find_text_content({NextElement, NextAttrs}, NextChildren ++ Tail, Contents);
    NewContent ->
      case Element of 
        {<<"p">>, _} ->
          find_text_content({NewContent, []}, Tail, <<Contents/binary, " ", NewContent/binary>>);
        _ ->
          find_text_content({NewContent, []}, Tail, Contents)
      end
  end.

get_title(Html) ->
  <<"Title">>.

