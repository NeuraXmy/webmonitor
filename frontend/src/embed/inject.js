javascript:(function() {
    var iframe = document.createElement('iframe');
    iframe.src = 'http://127.0.0.1:5174/select_monitor';
    console.log(iframe.src);
    iframe.width = 200;
    iframe.height = "100%";
    iframe.style.position = "fixed";
    iframe.style.top = "0";
    iframe.style.right = "0";
    iframe.id = 'iframe';
    var container = document.body;
    container.appendChild(iframe);
    window.addEventListener('click', function(evt) {
        console.log(evt);
        console.log(evt.target.baseURI);
        var targetWindow = document.getElementById('iframe').contentWindow;
        targetWindow.postMessage('Hello from the host page!', 'http://127.0.0.1:5174/select_monitor');
    });
  })();
  
  javascript:(function() {
    var iframe = document.createElement('iframe');
    iframe.src = 'http://127.0.0.1:5174/select_monitor';
    iframe.width = 200;
    iframe.height = "100%";
    iframe.style.position = "fixed";
    iframe.style.top = "0";
    iframe.style.right = "0";
    iframe.id = 'myIframe';
    var container = document.body;
    container.appendChild(iframe);
    iframe.addEventListener('click', function() {
        var targetWindow = iframe.contentWindow;
        targetWindow.addEventListener('message', function(event) {
            console.log('Received message from iframe:', event.data);
        });
        window.addEventListener('click', function(evt) {
            console.log(evt);
            targetWindow.postMessage('Hello from the host page!', 'http://127.0.0.1:5174');
        });
    });
})();

  javascript:console.log(window.innerWidth);
  javascript:window.innerWidth='50%';
  javascript:(function(){
    var d=top.document,v;
    if((v=d.documentElement)&&typeof v.clientWidth==='number'&&v.clientWidth!==0||(v=d.body)){
      v.scrollWidth='50%';
      console.log(v.scrollWidth);
      window.alert('Window :\t'+v.clientWidth+' x '+v.clientHeight+' px\nPage :\t'+v.scrollWidth+' x '+v.scrollHeight+' px\nScrolled :\t'+v.scrollLeft+' x '+v.scrollTop+' px' );
    }
  })()
  
  javascript:(function() {
    var newWidth = 800;
    var newHeight = 600;
    var container = document.body;
    container.style.width = newWidth + 'px';
    container.style.height = newHeight + 'px';
  })();
  
  
  javascript:(function() {
    var appRoot = "<%= root_url %>";
    var editorURL = "<%= @iframe_url %>";
    var postMessageDomain = "<%= root_url %>";
  
    var currentURL = window.location.href;
    console.log(currentURL);
    if (currentURL.indexOf(appRoot) >= 0) {
      alert("Drag this bookmarklet into your browser toolbar.");
      return false;
    }
  
    if (window._klaxonInject === true) {
      alert("The Klaxon bookmarklet already injected on this page.");
      return;
    } else {
      window._klaxonInject = true;
      console.log('[klaxon booted]');
    }
  
    var getCanonicalURL = function() {
      var og = null;
      var linkRel = null;
      var urlBar = null;
  
      try {
        og = document.querySelector("meta[property='og:url']").getAttribute("content");
      } catch(e) { }
  
      try {
        linkRel = document.querySelector("link[rel='canonical']").getAttribute("href");
      } catch(e) { }
  
      urlBar = window.location.href;
  
      if (og) {
        console.log("using og:url");
        return og;
      }
      if (linkRel) {
        console.log("using link[rel=canonical]")
        return linkRel;
      }
      console.log("no meta tag for canonical, using url as provided")
      return urlBar;
    }
  
    var cssPath = function(el) {
      // https://stackoverflow.com/questions/3620116/get-css-path-from-dom-element
      var path = [];
      while (
        (el.nodeName.toLowerCase() != 'body') &&
          (el = el.parentNode) &&
          path.unshift(el.nodeName.toLowerCase() +
            (el.id ? '#' + el.id : '') +
              (el.className ? '.' + el.className.replace(/\s+/g, ".") : ''))
      );
      return path;
    }
  
    var src = editorURL + "?url=" + encodeURIComponent(getCanonicalURL());
    var iframe = document.createElement('iframe');
    iframe.setAttribute('src', src);
    iframe.setAttribute('id', 'klaxon-bookmarklet-iframe');
    iframe.setAttribute('frameborder', 0);
    iframe.style.top = '0px';
    iframe.style.right = '0px';
    iframe.style.width = '300px';
    iframe.style.height = (window.innerHeight)+'px';
    iframe.style.position = 'fixed';
    iframe.style.zIndex = 2147483647;
    document.body.appendChild(iframe);
    document.body.setAttribute('cursor', 'grab')
  
    var styles = document.createElement('style');
    styles.setAttribute('id', 'klaxon-css-inject');
    document.body.appendChild(styles);
  
    var postMessage = function(data) {
      var json = JSON.stringify(data);
      iframe.contentWindow.postMessage(json, postMessageDomain);
    }
  
    var lastElement = function(arr) {
      return arr[arr.length-1];
    }
  
    var currentPath = [];
    var savedSelector;
    var updatePath = function(path) {
      currentPath = path;
      // var selector = path.join(" ");
      var selector = lastElement(path);
  
      var css = selector + " { background-color: rgba(255, 11, 58, 0.3); }\n";
      css += savedSelector + " { background-color: rgba(58, 255, 11, 0.3); }\n";
      console.log(css);
      styles.innerHTML = css;
  
      var matchText = document.querySelector(selector).innerText;
      postMessage({ event: 'updatePath', value: selector, matchText: matchText })
    }
  
    window.addEventListener('click', function(evt) {
      if (window._klaxonInject === true) {
        evt.preventDefault();
        var x = evt.clientX;
        var y = evt.clientY;
        var el = document.elementFromPoint(x, y);
        var selector = cssPath(el);
        updatePath(selector);
        savedSelector = lastElement(selector);
        postMessage({ event: 'click' });
      }
    });
  
    window.addEventListener('mousemove', function(evt) {
      if (window._klaxonInject === true) {
        var x = evt.clientX;
        var y = evt.clientY;
        var el = document.elementFromPoint(x, y);
        updatePath(cssPath(el));
      }
    });
  
    var receiveMessage = function(event){
      if (event.data == 'close_klaxon_bookmarklet'){
        iframe.parentNode.removeChild(iframe);
        var style = document.getElementById('klaxon-css-inject');
        style.parentNode.removeChild(style);
        console.log("Closed Klaxon Bookmarklet")
        window._klaxonInject = false;
      } else if (event.data.type == 'update_saved_selector') {
        savedSelector = event.data.selector;
        console.log('Updating saved selector', event.data.selector)
      }
    }
    window.addEventListener("message", receiveMessage, false);
  })();