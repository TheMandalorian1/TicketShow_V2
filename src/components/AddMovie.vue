<template>
<adminav></adminav>

  <div class="container">
    <form class="form-1" @submit.prevent="addMovie">
      <h1>Add Movie</h1>

      <label for="movie_name">Movie Name:</label>
      <input type="text" id="movie_name" v-model="movieName" placeholder="Movie name" required>
      <br>
      <label for="description">Description:</label>
      <input type="text" id="description" v-model="description" placeholder="Movie description" required>

      <br>
      <label for="ratings">Rating:</label>
      <input type="number" id="ratings" v-model="rating" placeholder="Rating out of 10" max="10" min="0" step="0.1" required>
      <br>
      <label for="image">Picture:</label>
      <input type="file" id="image" ref="imageInput" @change="handleFileUpload" accept="image/jpg, image/jpeg, image/png" required>
      <!-- <br> -->
      <input class="center" type="submit" value="ADD">
    </form>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  name: "AddMovie",
  components: {
        adminav: AdminNavbar,
    },
  data() {
    return {
      movieName: "",
      description: "",
      rating: "",
      image: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.image = event.target.files[0];
      console.log(this.image);
    },
    addMovie() {
      const formData = new FormData();
      formData.append("movie_name", this.movieName);
      formData.append("description", this.description);
      formData.append("movie_rating", this.rating);
      formData.append("poster", this.image);

      fetch("http://127.0.0.1:5000/api/admin/movie", {
        method: "POST",
        headers: {
          Authorization: localStorage.getItem("accessToken")
        },
        body: formData
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          } else {
            if (res.status === 401) {
              throw new Error("Token is not passed or invalid!");
            }
            if (res.status === 403) {
              throw new Error("Admin access required");
            }
            throw new Error("Failed to add movie: " + res.status);
          }
        })
        .then((data) => {
          if (data.error) {
            alert(data.error);
          } else {
            alert(data.message);
            this.$router.push({ name: "AdminDashboard" });
          }
        })
        .catch((error) => {
          alert(error.message);
        });
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
  background-color: aliceblue;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 550px;
  box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3);
}

.form-1 h1 {
  text-align: center;
  margin: 0.7rem 0 1.5rem;
}

input[type="email"],
input[type="datetime-local"],
input[type="number"],
input[type="file"],
input[type="password"],
input[type="text"],
select {
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

input[type="submit"],
button {
  margin: 2rem;
  margin-bottom: 1.5rem;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 1rem;
  border: none;
  font-size: 1.1rem;
  font-weight: bolder;
  background: linear-gradient(to right, #25aae1, #4481eb, #04befe, #3f86ed);
}

p {
  text-align: center;
  font-weight: bolder;
}
</style>
  