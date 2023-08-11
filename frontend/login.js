const form = document.querySelector("#login-form");
const infoDiv = document.querySelector("#info");

// let accessToken = null;

const handleSubmit = async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const sha256_passwd = sha256(formData.get("password"));
  formData.set("password", sha256_passwd);

  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });
  const data = await res.json();

  if (res.status === 200) {
    const accessToken = data.access_token;
    window.localStorage.setItem("token", accessToken);
    alert("로그인되었습니다");
    window.location.pathname = "/";
  } else if (res.status === 401) infoDiv.innerText = "로그인 실패...";

  //     infoDiv.innerText = "로그인되었습니다.";

  // window.location.pathname = "/";
  // const btn = document.createElement("button");
  // btn.innerText = "상품 가져오기";
  // btn.addEventListener("click", async () => {
  //   //access token을 같이 보내주려면 header에 넣어서 보내야됨
  //   const res = await fetch("/items", {
  //     headers: {
  //       Authorization: `Bearer ${accessToken}`, //Bearer : access token 호출 시 붙여줘야됨
  //     },
  //   });
  //   const data = await res.json();
  //   console.log(data);
  // });
  // infoDiv.appendChild(btn);
};

form.addEventListener("submit", handleSubmit);
