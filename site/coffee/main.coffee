$ "#menu-toggle"
  .click (e) ->
    do e.preventDefault
    $ "#wrapper"
      .toggleClass "toggled"