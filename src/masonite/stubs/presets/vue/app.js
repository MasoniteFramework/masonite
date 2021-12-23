/**
 * First we will load all of this project's JavaScript dependencies which
 * includes Vue and other libraries. It is a great starting point when
 * building robust, powerful web applications using Vue and Masonite.
 */

import { createApp } from "vue/dist/vue.esm-bundler.js"
import App from "./App.vue"
require("./bootstrap")

/**
 * Next, we will create a fresh Vue application instance
 */
const app = createApp(App)

/** You can also create an application without the App.vue
const app = createApp({})
*/


/**
 * The following block of code may be used to automatically register your
 * Vue components. It will recursively scan this directory for the Vue
 * components and automatically register them with their "basename".
 *
 * Eg. ./components/ExampleComponent.vue -> <example-component></example-component>
const files = require.context("./", true, /\.vue$/i)
files
  .keys()
  .map((key) =>
    app.component(key.split("/").pop().split(".")[0], files(key).default)
  )
 */

/**
Or you can register components manually
import ExampleComponent from './components/ExampleComponent.vue'
app.component("example-component", ExampleComponent)
 */

/** Finally we attach the Vue instance to the page.
 *  Then, you may begin adding components to this application
 * or customize the JavaScript scaffolding to fit your unique needs.
 */

app.mount("#app")
