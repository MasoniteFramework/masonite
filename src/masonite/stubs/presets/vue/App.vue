<template>
  <img alt="Vue logo" src="https://v3.vuejs.org/logo.png" />
  <hello-world msg="Hello Masonite and Vue 3.0" />
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue"

export default {
  name: "App",
  components: {
    HelloWorld,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
