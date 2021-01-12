const mix = require("laravel-mix");
const path = require("path");

// For Tailwind CSS
// const tailwindcss = require("tailwindcss")
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
  .vue({ version: 3 })
  .sass("resources/sass/app.scss", "storage/compiled/css");

// For Tailwind CSS, append
// .options({
//     processCssUrls: false,
//     postCss: [ tailwindcss('tailwind.config.js') ],
//   })

// New Alias plugin
mix.alias({
  "@": path.resolve("resources/js"),
});
