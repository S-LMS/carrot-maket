<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Nav.svelte";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";
  import Nav from "../components/Nav.svelte";

  let title;
  let price;
  let description;
  let place;

  const db = getDatabase();
  const storage = getStorage();

  function writeUserData(imgUrl) {
    push(ref(db, "items/"), {
      title,
      price,
      place,
      description,
      inserAt: new Date().getTime(),
      imgUrl,
    });

    window.location.hash = "/";

    // set(ref(db, "items/" + 'title'), {
    //   title,
    //   price,
    //   place,
    //   description
    // }) 문제점 : 같은 title을 가진 값을 입력하면 기존 값을 수정해버림.
  }

  // 'file' comes from the Blob or File API
  let files;
  $: if (files) console.log(files[0]);

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);

    const res = await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef);
    return url;
  };
  // bind:files를 통해 선택한 파일의 정보를 받아오는걸 알수있습니다
  // $: if (files) console.log(files);

  const handleSubmit = async () => {
    const url = await uploadFile();
    writeUserData(url);
  };
</script>

<form action="" id="write_form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="">이미지</label>
    <input type="file" bind:files name="image" id="image" />
  </div>
  <div>
    <label for="">제목</label>
    <input type="text" name="title" id="title" bind:value={title} />
  </div>
  <div>
    <label for="">가격</label>
    <input type="number" name="price" id="price" bind:value={price} />
  </div>
  <div>
    <label for="">설명</label>
    <input
      type="text"
      name="description"
      id="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="">장소</label>
    <input type="text" name="place" id="place" bind:value={place} />
  </div>
  <div>
    <button type="submit" class="write_button">글쓰기 완료</button>
  </div>
</form>
<Nav location="write" />

<style>
  .write_button {
    bottom: 120px;
    right: 20px;
    width: 90px;
    height: 30px;
    text-align: center;
    font-size: 18px;
    background-color: var(--button-primary);
    color: white;
    padding: 0px 15px 10px 15px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 1s ease-in-out;
    text-decoration: none;
  }
</style>
