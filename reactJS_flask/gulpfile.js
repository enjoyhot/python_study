'use strict';

//This file tells gulp what tasks to run and in what order to run them in.

// requirements
var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean');


// tasks
//-----------------------------------------------------------------------------
// Gulp utilizes pipes to stream data for processing. After grabbing the source
// file (main.js), the file is then “piped” to the browserify() function for
// transformation/bundling. This transformed and bundled code is then “piped”
// to the destination directory along with the size() function.
gulp.task('transform', function () {
    //specify the source directory
    return gulp.src('./project/app/static/js/reactjsx/main.js')
        //create the Browserify bundler functionality along with the transformer via Reactify
        .pipe(browserify({transform: ['reactify']}))
        //specify the destination directory
        .pipe(gulp.dest('./project/app/static/js/reactjs'))
        //calculate the size of the created file
        .pipe(size());
});

// When this task is ran, we grab the source directory – the result of the transform
// task – and then run the clean() function to remove the directory and its contents.
// It’s a good idea to run this before each new build to ensure you start fresh and clean.
gulp.task('clean', function () {
  return gulp.src(['./project/app/static/js/reactjs'], {read: false})
    .pipe(clean());
});

//it automatically runs 'clean' before the transformation
gulp.task('default', ['clean'], function() {
    gulp.start('transform');
    //WATCHER: automatically re-run the transform task anytime changes are made to the project/static/scripts/jsx/main.js file
    gulp.watch('./project/app/static/js/reactjsx/main.js', ['transform']);
    console.log("Running JSX transformation JSX-->JS...");
});
