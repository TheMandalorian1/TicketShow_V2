<template>
  <div class="container">
    <form class="form-1" @submit.prevent="createProfile" action="">
      <h1 class="center">SignUp</h1>
      <label for="name">Name</label>
      <input type="text" name="user_name" id="name" v-model="userName" required />
      <!-- <br> -->
      <label for="email">Email</label>
      <input type="email" name="email_id" id="email_id" v-model="emailId" required />
      <!-- <br> -->
      <label for="password">Password</label>
      <input type="password" name="password" id="password" v-model="password" required />
      <!-- <br> -->
      <div>
        <button type="submit" class="btn btn-primary">SignUp</button>
      </div>
      <!-- <br> -->
      <p>Already have an account? <a href="/login" id="login-link">Log in here</a></p>
      <br>
    </form>
  </div>
</template>
  
<script>
export default {
  name: "SignUp",
  data() {
    return {
      userName: "",
      emailId: "",
      password: "",
    };
  },
  methods: {
    createProfile() {
      fetch("http://127.0.0.1:5000/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.userName,
          email: this.emailId,
          password: this.password
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            alert(data.error)
            this.$router.push({ name: "SignUp" })
          }
          else {
            localStorage.setItem("token", data.token)
            localStorage.setItem("uname", data.name)
            localStorage.setItem("uid", data.uid)
            this.$router.push({ name: "UserDashboard" })
            alert(data["message"])
          }
        })
        .catch((error) => {
          alert(error.message)
          this.$router.push({ name: "SignUp" })
        })
    }
  }
};
</script>
  
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.form-1 {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: aliceblue;
  width: 40%;
  width: 450px;
  box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3);
}

.form-1 h1 {
  text-align: center;
  margin-top: 0.7rem;
  margin-bottom: 1.5rem;
}

input[type="email"],
input[type="password"],
input[type="text"] {
  border: none;
  outline: none;
  border-bottom: 1px solid;
  background: none;
  margin: 0.9rem 2rem;
  font-size: 20px;
}

label {
  margin: 0 2rem;
}

span {
  margin: 0 2rem;
  color: blue;
  cursor: pointer;
}

button {
  margin: 2rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem;
  cursor: pointer;
  border: none;
  font-size: 1.1rem;

}

p {
  text-align: center;
  font-weight: bolder;
}
</style>
  