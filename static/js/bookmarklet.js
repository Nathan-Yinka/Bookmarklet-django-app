const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 100;
const minHeight = 100;
// load css
const head = document.getElementsByTagName("head")[0];
const link = document.createElement("link");
link.rel =  'stylesheet';
link.href = `${styleUrl}?r=${Math.floor(Math.random()*9999999999999999)}`;
head.appendChild(link)

// load HTMl
const body = document.getElementsByTagName("body")[0];
boxHTML = `
<div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
 </div>
`;
body.innerHTML += boxHTML


function bookmarkletLaunch(){
    const bookmarklet = document.getElementById("bookmarklet");
    const imageFound = document.querySelector(".images");
    const close = document.getElementById("close")

    // clear the images in the image div
    imageFound.innerHTML = "";
    bookmarklet.style.display = "block";

    // close the bookmarklet page
    close.addEventListener("click",()=>{
        bookmarklet.style.display = "none";
    })

    const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image =>{
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight){
            const imageCreated = document.createElement("img")
            imageCreated.src = image.src;
            imageFound.append(imageCreated)
        }
    })

    // selecting the image from the bookmarklet image found
    const bookmarkImages=imageFound.querySelectorAll("img")
    bookmarkImages.forEach((image)=>{
        image.addEventListener("click",(e)=>{
            window.open(`${siteUrl}/images/create/?url=${encodeURIComponent(e.target.src)}&title=${document.title}`,"_blank")
        })
    })


    

}

bookmarkletLaunch()

