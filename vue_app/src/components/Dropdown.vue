<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      class="bg-blue-500 text-white px-4 py-2 rounded focus:outline-none"
    >
      {{ selectedOption }}
    </button>
    <div v-if="isOpen" class="absolute mt-2 w-full bg-white border rounded shadow-lg">
      <div
        v-for="option in options"
        :key="option"
        @click="selectOption(option)"
        class="px-4 py-2 hover:bg-gray-200 cursor-pointer"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const options = ref(['Option 1', 'Option 2', 'Option 3'])
const selectedOption = ref('Select an option')
const isOpen = ref(false)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  selectedOption.value = option
  isOpen.value = false
}
</script>

<style scoped>
/* Add any scoped styles here */
</style>
