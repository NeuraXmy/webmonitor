javascript:(function() {
  var verify_authenticity_token = "NQ.ZV2orQ.CgWBUK4b_jUtl27_h8B6tJCNK6E";

  var base_url = "http://127.0.0.1:5173";

  var currentURL = window.location.href;
  if (currentURL.indexOf(base_url) >= 0) {
    alert('请拖拽书签到浏览器导航栏.');
    return false;
  }
  
  var iframe = document.createElement('iframe');
  iframe.src = base_url + '/select_monitor';
  iframe.style.position = 'fixed';
  iframe.style.top = '70%';
  iframe.style.right = '0';
  iframe.style.width = '100%';
  iframe.style.height = '30%';
  iframe.style.zIndex = 2147483647;
  iframe.id = 'iframe';


  var container = document.body;
  container.appendChild(iframe);
  window.okRemoveIframe = true;



  function postMessage() {
      var targetWindow = document.getElementById('iframe').contentWindow;
      targetWindow.postMessage({ verify_authenticity_token: verify_authenticity_token,  baseURI: window.location.href, xpath:'' }, base_url + '/select_monitor');
  }


  var getcssSelector = function(path) {
    console.log(path.length);
    return path[path.length-1];
  };
  var cssPath = function(el) {
      var path = [];
      while (
        (el.nodeName.toLowerCase() != 'body') &&
          (el = el.parentNode) &&
          path.unshift(el.nodeName.toLowerCase() +
            (el.id ? '#' + el.id : '') +
              (el.className ? '.' + el.className.replace(/\s+/g, '.') : ''))
      );
      return path;
  };
  window.addEventListener('click', function(evt) {
      if(window.okRemoveIframe === true){
          console.log(evt);
          console.log(evt.target.baseURI);
          console.log(evt.target.innerText);
          var x = evt.clientX;
          var y = evt.clientY;
          var el = document.elementFromPoint(x, y);
          var selector = cssPath(el);
      
          var element = evt.target;
          var xpath = getXPath(element);
          selector = getcssSelector(selector);
          
          console.log(xpath);
          console.log(selector);
          var targetWindow = document.getElementById('iframe').contentWindow;
          targetWindow.postMessage({xpath:xpath, selector:selector,  selectText:evt.target.innerText, baseURI: evt.target.baseURI, verify_authenticity_token: verify_authenticity_token}, base_url + '/select_monitor');
      }
      
  });
  function mouse_over(event) {
      if(window.okRemoveIframe === true){
          var element = event.target;
          element.style.border = '1px solid red';
      }
    
  }
  function mouse_out(event) {
      if(window.okRemoveIframe === true){
          var element = event.target;
          element.style.border = '';
      }
  }
  function getXPath(element) {
    if (element.id !== '') {
      return '//*[@id=' + '%22' + element.id + '%22' + ']';
    }
    if (element === document.body) {
      return '/html/body';
    }
  
    var index = 1;
    const childNodes = element.parentNode ? element.parentNode.childNodes : [];
    var siblings = childNodes;
  
    for (var i = 0; i < siblings.length; i++) {
      var sibling = siblings[i];
      if (sibling === element) {
        return (
          getXPath(element.parentNode) +
          '/' +
          element.tagName.toLowerCase() +
          '[' +
          index +
          ']'
        );
      }
      if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
        index++;
      }
    }
  }
  document.addEventListener('mouseover', mouse_over);
  document.addEventListener('mouseout', mouse_out);
  
  window.addEventListener('message', function(evt) {
      if(evt.data.msg === "start"){
          postMessage();
      }else if(evt.data.msg === "Remove"){
          iframe.parentNode.removeChild(iframe);
          window.okRemoveIframe = false;
          console.log(window.okRemoveIframe);
      }
  });
})();