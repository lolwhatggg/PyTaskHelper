gulp = require 'gulp'
connect = require 'gulp-connect'
jade = require 'gulp-jade'
stylus = require 'gulp-stylus'
coffee = require 'gulp-coffee'
uglify = require 'gulp-uglify'
clean = require 'gulp-clean'
rjs = require 'gulp-requirejs'
rename = require 'gulp-rename'

dist = 'dist/'
db_dir = '../database/db.json'
full_db_dir = '../database/db_full.json'
update_time = '../database/date.json'

gulp.task 'connect', ->
  connect.server
    port: 1337
    livereload: on
    root: './' + dist

gulp.task 'jade', ->
  gulp.src ['jade/index.jade', 'jade/table.jade']
    .pipe jade
      locals: require db_dir
    .pipe gulp.dest dist
    .pipe do connect.reload

  tasks = require full_db_dir
  task_names = Object.keys tasks
  for name in task_names

    gulp.src 'jade/task.jade'
      .pipe jade
        locals:
          task: tasks[name]
          tasks: task_names
          date: require update_time
          annual: tasks[name]['annual_averages']
          students: tasks[name]['students']
        pretty: true
      .pipe rename tasks[name]['filename']
      .pipe gulp.dest dist + 'tasks'
      .pipe do connect.reload

gulp.task 'stylus', ->
  gulp.src 'stylus/*.styl'
    .pipe stylus set: ['compress']
    .pipe gulp.dest dist + 'css'
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
  .pipe gulp.dest dist + 'js'
  .pipe do connect.reload
  
  gulp.src 'js/', read: no
    .pipe do clean

gulp.task 'coffee', ->
  gulp.src 'coffee/*.coffee'
    .pipe do coffee
    .pipe gulp.dest 'js'

gulp.task 'ext', ->
  gulp.src 'backup/*.js'
    .pipe gulp.dest dist + 'js'
    .pipe do connect.reload
  gulp.src 'backup/*.css'
    .pipe gulp.dest dist + 'css'
    .pipe do connect.reload
  gulp.src '../icons/*'
    .pipe gulp.dest dist + 'icons'
  gulp.src '../database/*.json'
    .pipe gulp.dest dist + 'db'

gulp.task 'watch', ->
  gulp.watch 'jade/*.jade', ['jade']
  gulp.watch 'stylus/*.styl', ['stylus']
  gulp.watch 'coffee/*.coffee', ['build']
  gulp.watch 'backup/*.css', ['ext']
  gulp.watch 'backup/*.js', ['ext']

gulp.task 'default', ['jade', 'stylus', 'build', 'ext', 'watch', 'connect']
