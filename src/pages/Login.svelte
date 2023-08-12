<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  const auth = getAuth();
  const provider = new GoogleAuthProvider();

  const loginWithGoogle = async () => {
    //로그인
    try {
      //로그인 결과
      const result = await signInWithPopup(auth, provider);

      //로그인 완료 시 인증정보 - 토큰을 받아와 로그인 유지 시켜줌
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      const user = result.user;
      user$.set(user);
      localStorage.setItem("token", token);

      console.log("로그인", user);
    } catch (error) {
      console.log("에러", error);
    }
  };
</script>

<div>
  <!-- {#if $user$}
    <div>{$user$?.displayName} 로그인 중</div>
  {/if} -->
  <div>로그인하기</div>
  <button class="login-btn" on:click={loginWithGoogle}>
    <img
      class="google-img"
      src="https://w7.pngwing.com/pngs/869/485/png-transparent-google-logo-computer-icons-google-text-logo-google-logo-thumbnail.png"
      alt=""
    />
    <div>Google로 로그인하기</div>
  </button>
</div>

<style>
  .login-btn {
    width: 200px;
    height: 50px;
    border: 1px solid gray;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border-radius: 3px;
  }
  .google-img {
    width: 20px;
  }
</style>
