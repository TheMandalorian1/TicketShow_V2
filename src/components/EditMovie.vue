<template>
  <adminav></adminav>

  <div class="container">
    <form class="form-1" @submit.prevent="editMovie" action="">
      <h1>Edit Movie</h1>
      <label for="movie_name">Movie Name:</label>
      <input type="text" id="movie_name" v-model="movieName" required>
      <br>
      <label for="description">Description:</label>
      <input type="text" id="description" v-model="description" required>
      <br>
      <label for="image">Picture:</label>
      <input type="file" id="image" ref="imageInput" @change="handleFileUpload" accept="image/jpg, image/jpeg, image/png">
      <!-- <br> -->
      <input type="submit" value="Edit">
    </form>
  </div>
</template>
  
<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  name: "EditMovie",
  components: {
    adminav: AdminNavbar,
  },
  data() {
    return {
      movieName: "",
      description: "",
      image: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.image = event.target.files[0];
    },
    editMovie() {
      const formData = new FormData();
      formData.append('movie_name', this.movieName);
      formData.append('description', this.description);
      formData.append('poster', this.image);

      fetch(`http://127.0.0.1:5000/api/admin/movie/${this.$route.params.mid}`, {
        method: "PUT",
        headers: {
          'Authorization': localStorage.getItem('accessToken')
        },
        body: formData,
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
            } else {
              throw new Error("Failed to edit movie: " + res.status);
            }
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
          this.$router.push({ name: "AdminDashboard" });
        });
    }
  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/admin/movie/${this.$route.params.mid}`, {
      method: "GET",
      headers: {
        'Authorization': localStorage.getItem('accessToken')
      },
    })
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          if (res.status === 401) {
            throw new Error("Token is not passed or invalid!");
          }
          if (res.status === 403) {
            throw new Error("Admin access required!");
          } else {
            throw new Error("Failed to fetch movie details: " + res.status);
          }
        }
      })
      .then((data) => {
        this.movieName = data.movie_name;
        this.description = data.description;
      })
      .catch(error => {
        alert(error.message);
        this.$router.push({ name: "AdminLogin" });
      });
  },
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
  width: 80%;
  background-color: aliceblue;
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
  color: #fff;
  background: linear-gradient(to right, #25aae1, #4481eb, #04befe, #3f86ed);
}

p {
  text-align: center;
  font-weight: bolder;
}
</style>
  