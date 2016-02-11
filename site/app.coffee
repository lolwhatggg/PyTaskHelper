express = require 'express'
stylus = require 'stylus'
nib = require 'nib'
fs = require 'fs'

get_data = (path) ->
  JSON.parse fs.readFileSync path

data = get_data '../database/tasks_full.json'

app = do express

app.set 'view engine', 'jade'
app.locals.pretty = true

app.use (req, res, next) ->
  console.log req.method, req.url
  do next

app.use stylus.middleware
  src: __dirname + '/views'
  dest: __dirname + '/public'
  compile: (str, path) ->
    console.log path
    stylus str
      .set 'filename', path
      .use do nib
      .set 'compress', true

app.use express.static __dirname + '/public'

app.get '/tasks/:task', (req, res) ->
  task = req.params.task
  console.log task
  if !data.tasks[task]
    res.redirect '/tasks'
    return
  cur_data =
    tasks: data.tasks
    task: data.tasks[task]
    date: data.date
  res.render 'task', cur_data

app.get '/:page?', (req, res) ->
  page = req.params.page
  if !page then page = 'index'
  file = __dirname + '/views/' + page + '.jade'
  fs.stat file, (err, stat) ->
    if err
      res.redirect '/'
      return
    res.render page, tasks: data.tasks

server = app.listen 8282, ->
  console.log 'Listen on port 8282'
