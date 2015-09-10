'use strict';

var gulp = require('gulp');
var del = require('del');

// Vars
var src = 'bower_components/';

gulp.task('clean', function (cb) {
    del([
        'filemanager/*',
    ], cb);
});

gulp.task('install_filemanager', function () {
    return gulp.src(src + 'filemanager/dist/*')
        .pipe(gulp.dest('filemanager/'));
});

gulp.task('install_fileuploader', function () {
    return gulp.src(src + 'ng-file-upload/ng-file-upload.min.js')
        .pipe(gulp.dest('fileuploader/'));
});

gulp.task('install_angular', function () {
    return gulp.src(src + 'angular/angular.min.js')
        .pipe(gulp.dest('angular/'));
});

gulp.task('install_angular_translate', function () {
    return gulp.src(src + 'angular-translate/angular-translate.min.js')
        .pipe(gulp.dest('angular/'));
});

gulp.task('install_angular_cookies', function () {
    return gulp.src(src + 'angular-cookies/angular-cookies.min.js')
        .pipe(gulp.dest('angular/'));
});

gulp.task('install_angular_ui_tinymce', function () {
    return gulp.src(src + 'angular-ui-tinymce/src/tinymce.js')
        .pipe(gulp.dest('angular-ui-tinymce/'));
});


gulp.task('install_tinymce', function () {
    return gulp.src(src + 'tinymce-dist/tinymce.jquery.min.js')
        .pipe(gulp.dest('tinymce/'));
});


gulp.task('default', ['clean', 'install_filemanager', 'install_fileuploader', 'install_angular', 'install_angular_translate', 'install_angular_cookies', 'install_angular_ui_tinymce', 'install_tinymce']);

