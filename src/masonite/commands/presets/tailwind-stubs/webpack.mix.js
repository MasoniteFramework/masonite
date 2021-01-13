const mix = require("laravel-mix");
const path = require("path");
const tailwindcss = require("tailwindcss")

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Masonite application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix
  .js("storage/static/js/app.js", "storage/compiled/js")
  .sass("storage/static/sass/style.scss", "storage/compiled/")
  .options({
    processCssUrls: false,
    postCss: [tailwindcss("tailwind.config.js")],
  })
