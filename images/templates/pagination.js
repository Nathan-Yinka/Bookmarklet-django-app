let page = 1;
let emptyPage = false;
let blockRequest = false
const NoFeeds = document.querySelector(".no_feeds")

function isNearBottom() {
    const scrollHeight = document.documentElement.scrollHeight;
    const scrollTop = window.scrollY || window.pageYOffset;
    const clientHeight = document.documentElement.clientHeight;
    const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
    return distanceFromBottom <= 200;
}

function fetchNewData(){
    if(!blockRequest && !emptyPage){
        blockRequest =true;
        page += 1;

        fetch(`?images_only=1&page=${page}`)
        .then(response=>response.text())
        .then(html=>{
            if (html === ""){
                emptyPage = true;
                NoFeeds.style.display = 'block'
            }
            else{
                const imageList = document.getElementById('image-list');
                imageList.insertAdjacentHTML('beforeEnd', html);
                blockRequest = false;
                NoFeeds.style.display = 'none'
            }
        })
    }
}

window.addEventListener('scroll', () => {
    if (isNearBottom()) {
        fetchNewData();
    }
});