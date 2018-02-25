var img = document.getElementsByTagName("img");

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

// from https://stackoverflow.com/questions/247483/http-get-request-in-javascript
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}

const client = new HttpClient();

// generate green text and links
var pre = document.getElementsByTagName("pre");

for(let ele of pre){
    let el = ele.innerHTML;
    let lines = el.split("\n");
    for(let line in lines){
        if(lines[line].search("&gt;&gt;&gt") > -1){
            var words = lines[line].split(" ");
            for(let word in words){
                if(words[word].search("&gt;&gt;&gt") === 0){
                    let w = words[word].split("&gt;&gt;&gt;")[1]
                    client.get(`/q/${w}`, function(response) {
                        let res = JSON.parse(response)
                        ele.innerHTML = el.replace(`&gt;&gt;&gt;${w}`, `<a href="${res.url}">>>>${w}</a>`);
                    });
                }
            }
            lines[line] = words.join(" ");
        }else if(lines[line].search("&gt") === 0){
            lines[line] = `<span style="color: #789922;">${lines[line]}</span>`;
        }
    }
    el = lines.join("\n")
    ele.innerHTML = el;
}