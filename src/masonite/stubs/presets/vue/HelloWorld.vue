<template>
  <h1>{{ msg }}</h1>
  <p>Count is: {{ count }}, double is {{ double }}.</p>
  <button @click="increment">click to increment</button>
</template>

<script>
import { ref, computed, onMounted } from "vue"

export default {
  name: "HelloWorld",
  props: {
    msg: {
      type: String,
      default: "",
    },
  },
  setup() {
    const count = ref(0)
    const double = computed(() => count.value * 2)

    function increment() {
      count.value++
    }

    onMounted(() => console.log("HelloWorld mounted!"))

    return {
      count,
      double,
      increment,
    }
  },
}
</script>
