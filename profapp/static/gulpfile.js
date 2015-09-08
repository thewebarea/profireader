'use strict';

var gulp = require('gulp');
var del = require('del');

// Vars
var src = 'bower_components/filemanager/dist/';
var dst = 'filemanager/';

gulp.task('clean', function (cb) {
  del([
      dst + '/*',
  ], cb);
});

gulp.task('install', function() {
  return gulp.src(src + '*')
    .pipe(gulp.dest(dst));
});


gulp.task('default', ['clean', 'install']);

