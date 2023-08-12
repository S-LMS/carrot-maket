<script>
  import Nav from "../components/Nav.svelte";
  import { user$ } from "../store";

  const logout = () => {
    //user정보와 local storage(token)를 비워주면됨
    localStorage.removeItem("token");
    user$.set(null);
  };
</script>

<div>{$user$.displayName}님의 당근</div>
<button on:click={logout}>Logout</button>

<Nav location="my" />

<style>
  button {
    cursor: pointer;
    border: 1px solid gray;
    width: 100px;
    height: 40px;
  }
</style>
