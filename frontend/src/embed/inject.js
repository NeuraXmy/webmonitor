javascript:(function() {

  var iframe = document.createElement('iframe');
  iframe.src = 'http://127.0.0.1:5173/select_monitor';
  console.log(iframe.src);
  iframe.style.position = "fixed";
  iframe.style.top = "70%";
  iframe.style.right = "0";

  iframe.style.width = '100%';
  iframe.style.height = '30%';
  iframe.style.zIndex = 2147483647;
  
  iframe.id = 'iframe';
  var container = document.body;
  container.appendChild(iframe);
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
              (el.className ? '.' + el.className.replace(/\s+/g, ".") : ''))
      );
      return path;
  };
  window.addEventListener('click', function(evt) {
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
      targetWindow.postMessage({xpath:xpath, selector:selector,  selectText:evt.target.innerText}, 'http://127.0.0.1:5173/select_monitor');
  });
  function mouse_over(event) {
    var element = event.target;
    element.style.border = "1px solid red";
  }
  function mouse_out(event) {
    var element = event.target;
    element.style.border = "";
  }
  function getXPath(element) {
    if (element.id !== "") {
      return '//*[@id="' + element.id + '"]';
    }
    if (element === document.body) {
      return "/html/body";
    }

    var index = 1;
    const childNodes = element.parentNode ? element.parentNode.childNodes : [];
    var siblings = childNodes;

    for (var i = 0; i < siblings.length; i++) {
      var sibling = siblings[i];
      if (sibling === element) {
        return (
          getXPath(element.parentNode) +
          "/" +
          element.tagName.toLowerCase() +
          "[" +
          index +
          "]"
        );
      }
      if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
        index++;
      }
    }
  }
  document.addEventListener("mouseover", mouse_over);
  document.addEventListener("mouseout", mouse_out);

  var links = document.getElementsByTagName('a');

  for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function(event) {
      event.preventDefault();
      event.stopPropagation();
    });
  }
})();

