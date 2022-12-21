// Alert Disappear
setTimeout(() => {
  document.querySelector(".message").remove();
  console.log(["out"]);
}, 3000);

// Like Post Asynchroniously
document.body.addEventListener("click", likePost);
function likePost(e) {
  if (e.target.classList.contains("likePost")) {
    e.preventDefault();
    const like = e.target;

    const id = like.id;
    like.nextElementSibling.classList.toggle("bground-important");
    const likedElement = like.nextElementSibling.classList;
    let likedNumber = like.nextElementSibling;
    like.classList.toggle("text-info");

    let num = Number(likedNumber.innerText);

    if (likedElement.contains("bground-important")) {
      likedNumber.innerText = num + 1;
    } else {
      likedNumber.innerText = num - 1;
    }

    const csrftoken = document.cookie.slice(10);
    fetch(`${location.origin}/like_post/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      mode: "same-origin",
      body: JSON.stringify({ id: id }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.liked) {
          like.classList.remove("text-info");
          like.nextElementSibling.classList.remove("bground-important");
        } else {
          like.classList.add("text-info");
          like.nextElementSibling.classList.add("bground-important");
        }
        like.nextElementSibling.innerText = data.total_likes;
      });
  }
}

// Infinite Scrolling with Ajax
let cardContianer = document.querySelector(".cardContainer");
let laodData = document.querySelector(".loading");
const formInput = document.querySelector(".search-box");

const option = {
  root: null,
  threshold: 0.5,
};
const observer = new IntersectionObserver(GetData, option);

let page = 2;
function GetData(entries) {
  const entry = entries[0];

  if (entry.isIntersecting) {
    fetch(
      `${document.location.origin}?${
        formInput.value !== "" ? `search=${formInput.value}&` : ""
      }page=${page}`,
      {
        headers: {
          method: "GET",
          "X-Requested-With": "XMLHttpRequest",
        },
      }
    )
      .then((response) => response.json())
      .then((posts) => {
        posts[0].forEach((post) => {
          let html = `
          <div class="card mb-4">
        <!-- post header -->
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <a href="/user_profile/${post.profile_id}">
                <img src="${post.profile_image}" alt="" class="
                      img-fluid
                      rounded-circle
                      d-inline-block
                      b-box
                      img-size
                    " />
              </a>
              <h6 class="ml-2 d-inline-block">${post.username}</h6>
            </div>
            <div class="date">${post.date}</div>
          </div>
        </div>
        <!-- post body -->
        ${
          post.post_image_name == "kindpng_4517876.png"
            ? ""
            : `<img src="${post.post_image}" alt="" class="img-fluid" />`
        }
        <div class="card-body">
          <h4 class="card-title">${post.title === null ? "" : post.title}</h4>
          <p class="card-text">
           ${
             post.body.length > 150
               ? post.body.slice(0, 150) +
                 `...<a href="post_details/${post.post_id}" class="read-more cl-fb">Read more</a>`
               : post.body
           }
          </p>
        </div>
        
        <!-- post footer -->
        <div class="card-footer">
          <div class="d-flex align-items-center">
            <div class="mr-3">
                <i id="${post.post_id}" class="fa fa-thumbs-up ${
            post.user_liked && "text-info"
          }  likePost"></i>
              <span class="badge bground-dark text-light ${
                post.user_liked && "bground-important"
              } ">${post.total_liked}</span>
            </div>
            <div class="ml-2">
              <a href="post_details/${post.post_id}">
                <i class="fa fa-comment-alt text-dark"></i>
              </a>
              <span class="badge badge-dark ">${post.comment}</span>
            </div>
          </div>
        </div>
      </div>
          `;
          cardContianer.insertAdjacentHTML("beforebegin", html);
        });
          console.log(posts[1].page_has_next)
        if (posts[1].page_has_next == false) {
          laodData.style.display = "none";
        }
      });
    page++;
  }
}
observer.observe(laodData);


