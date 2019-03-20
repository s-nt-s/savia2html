function findParent(e, tag, _class) {
  tag = tag.toUpperCase();
  var cl=null;
  while (e) {
    if (e.className && e.tagName.toUpperCase()==tag) {
      cl = e.className.split(/\s+/);
      if (cl.includes(_class)) return e;
    }
    e = e.parentNode;
  }
  return null;
}

function toggleClass(e, _class) {
  var cl = e.className.split(/\s+/);
  if (cl.includes(_class)) {
    var i = cl.indexOf(_class);
    cl.splice(i, 1);
  }
  else {
    cl.push(_class)
  }
  e.className = cl.join(" ");
}

document.addEventListener("DOMContentLoaded", function(event) {
  var elms = document.getElementsByClassName("sm-exercise-number");
  var i, e;
  for (i=0; i<elms.length; i++){
    e = elms[i];
    e.addEventListener('click', function(event) {
      var p = findParent(this, 'div', 'exercise');
      toggleClass(p, "pshow");
    });
  }
});
