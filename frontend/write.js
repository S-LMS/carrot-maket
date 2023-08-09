const form = document.getElementById("write_form");

const handleSubmitForm = async (event) => {
  event.preventDefault();

  //body에 timestamp를 같이 보냄
  const body = new FormData(form);
  body.append("inserAt", new Date().getTime());

  //POST 값을 받아와 submit
  try {
    const res = await fetch("/items", {
      method: "POST",
      //   body: new FormData(form),
      body,
    });

    const data = await res.json();
    if (data == "200") window.location.pathname = "/";
  } catch (e) {
    console.error("이미지 업로드에 실패했습니다.");
  }

  console.log();
};

form.addEventListener("submit", handleSubmitForm);
