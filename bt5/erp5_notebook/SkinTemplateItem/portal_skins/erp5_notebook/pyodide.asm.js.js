var pyodide = function(pyodide) {
  pyodide = pyodide || {};






  return pyodide;
};
pyodide = pyodide.bind({
  _currentScript: typeof document !== 'undefined' ? document.currentScript : undefined
});
if (typeof exports === 'object' && typeof module === 'object')
    module.exports = pyodide;
  else if (typeof define === 'function' && define['amd'])
    define([], function() { return pyodide; });
  else if (typeof exports === 'object')
    exports["pyodide"] = pyodide;
  