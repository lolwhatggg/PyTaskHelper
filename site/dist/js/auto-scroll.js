{% if is_mobile % }
  // Hides mobile browser's address bar when page is done loading.
  window.addEventListener('load', function(e) {
    setTimeout(function() { window.scrollTo(0, 1); }, 1);
  }, false);
{% endif % }