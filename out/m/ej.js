$(document).ready(function() {
  $("div.sm-exercise-number").click(function(){
    var e = $(this).closest("div.exercise");
    e.toggleClass("pshow")
  })
})
