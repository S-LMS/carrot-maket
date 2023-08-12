<script>
  import { onMount } from "svelte";
  import Footer from "../components/Nav.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";
  import Nav from "../components/Nav.svelte";

  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  //시간
  const calcTime = (timestamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second >= 0) return `${second}초 전`;
  };
  // $ : 반응형 변수(랜더링)
  $: items = [];

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  // onMount : JS파일은 처음 랜더링 될떄 한번만 실행됨 →  다른곳으로 이동 후에도 data가 뜸
  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
      console.log(items);
    });
  });
</script>

<!-- 헤더 -->
<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="img/wifi.svg" alt="wifi" />
      <img src="img/chart-bar.svg" alt="chart-bar" />
      <img src="img/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location--icons">
        <img src="img/arrow.svg" alt="arrow" />
      </div>
    </div>
    <div class="menu-bar__icons" style="position: relative">
      <img src="img/search.svg" alt="search" />
      <img src="img/menu.svg" alt="menu" />
      <img src="img/bell.svg" alt="bell" />
      <!-- <span style="position: absolute; right: 15px; top: 70px">안읽음</span> -->
      <div
        style="
            position: absolute;
            width: 10px;
            height: 10px;
            border-radius: 100%;
            background-color: coral;
            right: 7px;
            top: 0px;
          "
      />
    </div>
  </div>
</header>

<!-- 메인 -->
<main>
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img src={item.imgUrl} alt={item.title} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.inserAt)}
        </div>
        <div class="item-list__info-price">{item.price}</div>
        <div>{item.description}</div>
      </div>
    </div>
  {/each}

  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>
<Nav location="home" />

<div class="media-info-msg">화면 크기를 키워주세요.</div>

<style>
  .info-bar__time {
    color: red;
  }
</style>
