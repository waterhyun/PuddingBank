<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>


<template>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink> |
        <RouterLink to="/articles">게시판</RouterLink> |
        <RouterLink to="/banks">은행 찾기</RouterLink>
      </nav>
    </div> <RouterView/>
</template>

<!-- <script setup>

</script> -->

<style scoped>

</style>