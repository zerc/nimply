var SETTINGS = {},
    gulp = require('gulp'),
    less = require('gulp-less'),
    runSequence = require('run-sequence'),
    del = require('del'),
    concat = require('gulp-concat'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream'),
    reactify = require('reactify');


SETTINGS.SRC_JSX = './src/js/App.jsx';
SETTINGS.SRC_LESS = './src/css/styles.less';
SETTINGS.JS_DEST = './build/js/';
SETTINGS.LESS_DEST = './build/css';
SETTINGS.PATH_ALL = [SETTINGS.SRC_JSX, SETTINGS.SRC_LESS];

gulp.task('vendor', function() {
    // CSS
    gulp.src('./node_modules/Skeleton-Less/less/skeleton.less')
        .pipe(less())
        .pipe(gulp.dest(SETTINGS.LESS_DEST));

    gulp.src('./node_modules/normalize.css/normalize.css')
        .pipe(gulp.dest(SETTINGS.LESS_DEST));

    gulp.src('./src/font-awesome/fonts/*')
        .pipe(gulp.dest('./build/fonts/'));

    gulp.src('./src/font-awesome/less/font-awesome.less')
        .pipe(less())
        .pipe(gulp.dest(SETTINGS.LESS_DEST));
});

gulp.task('less', function () {
    return gulp.src(SETTINGS.SRC_LESS)
        .pipe(less())
        .pipe(gulp.dest(SETTINGS.LESS_DEST))
});

gulp.task('browserify', function() {
    return browserify({
            entries: './src/js/App.jsx',
            transform: [reactify],
        })
        .bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest(SETTINGS.JS_DEST));
});

gulp.task('js', function () {
    return gulp.src(SETTINGS.SRC_JSX)
        .pipe(react())
        .pipe(concat('app.js'))
        .pipe(gulp.dest(SETTINGS.JS_DEST));
});

gulp.task('clean', del.bind(
  null, ['.tmp', 'build/*', '!build/.git'], {dot: true}
));

gulp.task('watch', function(){
  gulp.watch(SETTINGS.PATH_ALL, ['less']);
});

gulp.task('default', ['clean'], function (cb) {
    runSequence(['vendor', 'less', 'browserify'], cb);
});
