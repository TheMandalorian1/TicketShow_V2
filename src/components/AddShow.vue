<template>
  <adminav></adminav>

  <div class="container">
    <form class="form-1" @submit.prevent="createShow">
      <h1>Create Show</h1>

      <label for="venue_name">Venue Name:</label>
      <select id="venue_name" v-model="selectedVenue" required>
        <option :value="venue.venue_id" v-for="venue in venue_details" :key="venue.venue_id">
          {{ venue.venue_name + ', ' + venue.venue_location }}
        </option>
      </select>

      <label for="movie_name">Movie Name:</label>
      <select id="movie_name" v-model="selectedMovie" required>
        <option :value="movie.movie_id" v-for="movie in movie_details" :key="movie.movie_id">
          {{ movie.movie_name }}
        </option>
      </select>

      <label for="start_time">Start Time:</label>
      <input type="datetime-local" v-model="startTime" required>
      <br>
      <label for="end_time">End Time:</label>
      <input type="datetime-local" v-model="endTime" required>
      <br>
      <label for="price">Price:</label>
      <input type="number" id="price" v-model="ticketPrice" placeholder="Enter show price" max="5000" min="50" step="25"
        required>

      <input type="submit" value="Create">
    </form>
  </div>
</template>
  
<script>
import AdminNavbar from './AdminNavbar.vue'

export default { 
  name: "AddShow",
  components: {
        adminav: AdminNavbar,
    },
  data() {
    return {
      venue_details: "",
      movie_details: "",
      selectedVenue: "",
      selectedMovie: "",
      startTime: "",
      endTime: "",
      ticketPrice: 50
    };
  },
  methods: {
    createShow() {
      fetch('http://127.0.0.1:5000/api/admin/show', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Authorization': localStorage.getItem('accessToken')
        },
        body: JSON.stringify({
          movie_id: this.selectedMovie,
          venue_id: this.selectedVenue,
          start: this.startTime,
          end: this.endTime,
          ticket_price: this.ticketPrice,
        })
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
          }else {
            throw new Error(res.status);
          }
        }
      })  
        .then((data) => {
          if (data.error) {
            alert(data.error)
            this.$router.push({ name: "AdminDashboard" })
          }
          else {
            alert(data.message)
            this.$router.push({ name: "AdminDashboard" })
          }
        })
        .catch(error => {
          console.log(error);
          alert(error.message);
          this.$router.push({ name: "AdminDashboard" })
        });
    }
  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/admin/dashboard`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
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
            throw new Error("Admin access required");
          }else {
            throw new Error(res.status);
          }
        }
      })  
      .then((data) => {
        this.movie_details = data.movies;
        this.venue_details = data.venues;
        this.selectedVenue = this.$route.params.vid;
      })
      .catch(error => {
        console.log(error);
        alert(error.message);
        this.$router.push({ name: "AdminDashboard" })
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
  top: 53%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: aliceblue;
  width: 40%;
  box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3);
}

.form-1 h1 {
  text-align: center;
  margin-top: 0.7rem;
  margin-bottom: 1.5rem;
}

input[type="number"],
input[type='datetime-local'],
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