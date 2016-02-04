gulp = require 'gulp'
connect = require 'gulp-connect'
jade = require 'gulp-jade'
stylus = require 'gulp-stylus'
coffee = require 'gulp-coffee'
uglify = require 'gulp-uglify'
clean = require 'gulp-clean'
rjs = require 'gulp-requirejs'
data = require 'gulp-data'
rename = require 'gulp-rename'

dist = 'dist/'
db_dir = '../database/db_full.json'

gulp.task 'connect', ->
  connect.server
    port: 1337
    livereload: on
    root: './' + dist

gulp.task 'jade', ->
  gulp.src 'jade/index.jade'
    .pipe data (file) ->
      require db_dir
    .pipe do jade
    .pipe gulp.dest dist
    .pipe do connect.reload
  truth = true
  tasks = require db_dir
  for name in Object.keys tasks.data

    task = Object()
    task['cur'] = tasks.data[name]
    task['data'] = (require db_dir)['data']
    gulp.src 'jade/task.jade'
      .pipe data (file) ->
        task
      .pipe do jade
      .pipe rename task.name + '.html'
      .pipe gulp.dest dist + '/tasks'
      .pipe do connect.reload

gulp.task 'stylus', ->
  gulp.src 'stylus/*.styl'
    .pipe stylus set: ['compress']
    .pipe gulp.dest dist + '/css'
    .pipe do connect.reload

gulp.task 'build', ['coffee'], ->
  rjs
    baseUrl: 'js'
    name: '../bower_components/almond/almond'
    include: ['main']
    insertRequire: ['main']
    out: 'all.js'
    wrap: on
  .pipe do uglify
  .pipe gulp.dest dist + '/js'
  .pipe do connect.reload
  
  gulp.src 'js/', read: no
    .pipe do clean

gulp.task 'coffee', ->
  gulp.src 'coffee/*.coffee'
    .pipe do coffee
    .pipe gulp.dest 'js'

gulp.task 'watch', ->
  gulp.watch 'jade/*.jade', ['jade']
  gulp.watch 'stylus/*.styl', ['stylus']
  gulp.watch 'coffee/*.coffee', ['build']

gulp.task 'default', ['jade', 'stylus', 'build']
