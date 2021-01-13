const mix = require("laravel-mix");
const path = require("path");

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
  .js("resources/js/app.js", "storage/compiled/js")
  .postCss("resources/css/tailwind.css", "storage/compiled/css", [
    require("tailwindcss"),
  ])

// For Tailwind CSS, append
// .options({
//     processCssUrls: false,
//     postCss: [ tailwindcss('tailwind.config.js') ],
//   })
