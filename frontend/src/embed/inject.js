javascript:(function() {

  var iframe = document.createElement('iframe');
  iframe.src = 'http://127.0.0.1:5173/select_monitor';
  iframe.style.position = "fixed";
  iframe.style.top = "70%";
  iframe.style.right = "0";
  iframe.style.width = '100%';
  iframe.style.height = '30%';
  iframe.style.zIndex = 2147483647;
  iframe.id = 'iframe';

  var container = document.body;
  container.appendChild(iframe);

  window.addEventListener('click', function(evt) {
    console.log(evt);
    var x = evt.clientX;
    var y = evt.clientY;
    var el = document.elementFromPoint(x, y);
    var selector = cssPath(el);
    var xpath = getXPath(el);

    var targetWindow = document.getElementById('iframe').contentWindow;
    targetWindow.postMessage({ xpath: xpath, selector: selector }, 'http://127.0.0.1:5173/select_monitor');
  });

  function cssPath(el) {
    var path = [];
    while ((el.nodeName.toLowerCase() != 'body') && (el = el.parentNode)) {
      if (el.id) {
        path.unshift('#' + el.id);
        break;
      } else {
        var tagName = el.tagName.toLowerCase();
        var siblings = el.parentNode.querySelectorAll(tagName);
        if (siblings.length > 1) {
          for (var i = 0; i < siblings.length; i++) {
            if (siblings[i] === el) {
              path.unshift(tagName + ':nth-child(' + (i + 1) + ')');
              break;
            }
          }
        } else {
          path.unshift(tagName);
        }
      }
    }
    return path.join(' > ');
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
})();
