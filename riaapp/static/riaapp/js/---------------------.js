var openFile = function(event) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function(){
    var text = reader.result;
    document.getElementById("recontent").innerHTML = reader.path;
  };
  reader.readAsText(input.files[0]);
};