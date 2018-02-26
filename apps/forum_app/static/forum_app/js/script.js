'use strict'

// expands images when clicked
var img = document.querySelectorAll("[data-alt-src]");

for(let i of img){
    i.addEventListener("click", function(e){
        let temp = e.target.dataset.altSrc;
        e.target.dataset.altSrc = e.target.src;
        e.target.src = temp;
    });
}

// add a link to the reply when clicking on a post number
var replies = document.getElementsByClassName("reply")

for(let r of replies){
    r.addEventListener("click", function(e){
        let textarea = document.querySelector("textarea");
        textarea.value += `>>>${e.target.innerHTML} `;
    });
}

// creates a preview thumbnail when uploading an image
// from: https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL
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

// basically jquery's $.get
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

// generate quotes (>greentext) and links
var pre = document.getElementsByTagName("pre");

for(let ele of pre){
    let el = ele.innerHTML;
    let lines = el.split("\n");
    for(let line in lines){
        if(lines[line].search("&gt;&gt;&gt") > -1){
            let words = lines[line].split(" ");
            for(let word in words){
                if(words[word].search("&gt;&gt;&gt") === 0){
                    let w = words[word].split("&gt;&gt;&gt;")[1]
                    let toReplace = `&gt;&gt;&gt;${w}`;
                    let replacement = `<a data-id="${w}" href="/post/${w}">>>>${w}</a>`;
                    words[word] = words[word].replace(toReplace, replacement);
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

// only make AJAX request when a user clicks on a link
var genLinks = document.querySelectorAll("[data-id]");

for(let link of genLinks){
    link.addEventListener("click", function(e){
        e.preventDefault();
        client.get(`/q/${e.target.dataset.id}`, function(response) {
            window.location = JSON.parse(response).url;
        });
    });
}