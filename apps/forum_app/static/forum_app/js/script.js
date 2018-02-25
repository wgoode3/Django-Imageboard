var img = document.getElementsByTagName("img");
var imageInput = document.querySelector('input[name="image"]')
for(let i of img){
    i.addEventListener("click", function(e){
        let temp = e.target.dataset.altSrc;
        e.target.dataset.altSrc = e.target.src;
        e.target.src = temp;
    });
}
function previewFile() {
    var preview = document.getElementById('preview');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    reader.addEventListener("load", function () {
        // console logging this gives an image as base64... neat
        // console.log(reader.result);

        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}