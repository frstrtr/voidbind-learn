/* Remembers the chosen language and, on the root page only, sends the
   visitor to it. No cookies and no third-party code. Everything still
   works if storage is blocked or scripts are off. */
(function () {
  var KEY = 'vb-lang', LANGS = ['en', 'fr', 'ru', 'de', 'zh'];
  function get() { try { return window.localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { window.localStorage.setItem(KEY, v); } catch (e) { /* storage blocked */ } }
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[data-lang]') : null;
    if (a) set(a.getAttribute('data-lang'));
  });
  var root = document.documentElement;
  if (root.getAttribute('data-chooser') === '1') {
    var pick = get();
    if (LANGS.indexOf(pick) < 0) {
      pick = 'en';
      var prefs = navigator.languages || [navigator.language || 'en'];
      for (var i = 0; i < prefs.length; i++) {
        var p = String(prefs[i]).toLowerCase().slice(0, 2);
        if (LANGS.indexOf(p) >= 0) { pick = p; break; }
      }
    }
    window.location.replace('/' + pick + '/');
  }
})();
