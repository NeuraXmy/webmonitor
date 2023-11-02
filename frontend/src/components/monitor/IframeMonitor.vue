<template>
    <div class="klaxon">
      <iframe ref="iframe" :src="iframeUrl"></iframe>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Klaxon',
    props: {
      editorUrl: String,
      postMessageDomain: String
    },
    data() {
      return {
        isInjected: false,
        lastPath: '',
        lastMatch: ''
      };
    },
    computed: {
      iframeUrl() {
        return `${this.editorUrl}?url=${encodeURIComponent(this.canonicalURL)}`;
      },
      canonicalURL() {
        const canonicalLink = document.querySelector('link[rel="canonical"]');
        const canonicalMeta = document.querySelector('meta[property="og:url"]');
        if (canonicalLink) {
          return canonicalLink.href;
        } else if (canonicalMeta) {
          return canonicalMeta.content;
        } else {
          return location.href;
        }
      }
    },
    methods: {
      inject() {
        if (location.pathname.startsWith(appRoot)) {
          alert('Klaxon is already injected in this app!');
          return;
        }
  
        if (window._klaxonInject) {
          alert('Klaxon is already injected on this page!');
          return;
        }
  
        window._klaxonInject = true;
        console.log('Klaxon is successfully injected!');
      },
      close() {
        this.$refs.iframe.remove();
        console.log('Klaxon is closed!');
      },
      getCSSPath(el) {
        if (!(el instanceof Element)) return;
        const path = [];
        while (el.nodeType === Node.ELEMENT_NODE) {
          let selector = el.nodeName.toLowerCase();
          if (el.id) {
            selector += '#' + el.id;
            path.unshift(selector);
            break;
          } else {
            let sibling = el;
            let nth = 1;
            while ((sibling = sibling.previousElementSibling) != null) {
              if (sibling.nodeName.toLowerCase() === selector) {
                nth++;
              }
            }
            if (nth != 1) {
              selector += ':nth-of-type(' + nth + ')';
            }
          }
          path.unshift(selector);
          el = el.parentNode;
        }
        return path.join(' > ');
      },
      updatePath(el, match) {
        const path = this.getCSSPath(el);
        if (path === this.lastPath && match === this.lastMatch) return;
        this.lastPath = path;
        this.lastMatch = match;
        this.postMessage({ type: 'update-path', data: { path, match } });
      },
      postMessage(data) {
        const iframe = this.$refs.iframe;
        if (!iframe) return;
        iframe.contentWindow.postMessage(data, this.postMessageDomain);
      },
      handleClick(event) {
        if (event.target.matches('.klaxon-close')) {
          this.close();
          return;
        }
        if (!event.target.matches('.klaxon *')) {
          this.updatePath(null, null);
          return;
        }
        const el = lastElement(event.path);
        const match = window.getSelection().toString();
        if (!match) return;
        this.updatePath(el, match);
      },
      handleMouseMove(event) {
        const el = lastElement(event.path);
        if (!el || !el.matches) return;
        if (!el.matches('.klaxon *')) {
          this.updatePath(null, null);
          return;
        }
        const match = window.getSelection().toString();
        if (!match) return;
        this.updatePath(el, match);
      }
    },
    mounted() {
      this.inject();
      window.addEventListener('click', this.handleClick);
      window.addEventListener('mousemove', this.handleMouseMove);
    },
    beforeUnmount() {
      window.removeEventListener('click', this.handleClick);
      window.removeEventListener('mousemove', this.handleMouseMove);
    }
  };
  </script>
  
  <style>
  .klaxon {
    position: fixed;
    top: 0;
    right: 0;
    width: 300px;
    height: 100vh;
    z-index: 9999;
  }
  .klaxon iframe {
    border: none;
    width: 100%;
    height: 100%;
  }
  .klaxon-close {
    position: absolute;
    top: 0;
    right: 0;
    padding: 4px 6px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
  }
  </style>
  