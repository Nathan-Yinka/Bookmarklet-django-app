const url = "{% url 'user_follow' %}"
const options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
}

const follow = document.querySelector('a.follow');
follow.addEventListener("click",(e)=>{
    e.preventDefault();
    const formData = new FormData()
    formData.append("id",follow.dataset.id);
    formData.append("action",follow.dataset.action);
    options.body = formData

    fetch(url,options)
    .then(response=>response.json())
    .then(data=>{
        if (data['status'] === "ok"){
            const perviousAction = follow.dataset.action

            const action = perviousAction === "follow"? "unfollow" : "follow"

            follow.dataset.action = action
            follow.innerHTML = action

            const followerCount = document.querySelector('span.count .total');

            const totalFollowers = parseInt(followerCount.innerHTML);

            followerCount.innerHTML = perviousAction === 'follow' ? totalFollowers + 1 : totalFollowers - 1;
        }
        else{
            window.location.reload()
        }
    })
})