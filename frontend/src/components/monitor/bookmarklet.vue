<template>
    <div>
      <a href="javascript:void(0);" @dragstart="handleDragStart" id="bookmarkButton">小书签</a>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      handleDragStart(event) {
        event.dataTransfer.setData('text/plain', '书签按钮');
      }
    }
  };
  </script>
  