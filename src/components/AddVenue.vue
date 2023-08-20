<template>

<adminav></adminav>

    <div class="container">
    <form class="cont" @submit.prevent="addVenue">
      <h1>Add Venue</h1>
      <label for="venue_name">Venue Name:</label>
      <input type="text" id="venue_name" v-model="venueName" placeholder="Venue name" required>
      <br>
      <label for="location">Address/Location:</label>
      <input type="text" id="location" v-model="location" placeholder="Full address/location of venue" required> 
      <br>
      <label for="capacity">Capacity:</label>
      <select id="capacity" v-model="capacity" required>
        <option value="100">100</option>
        <option value="200">200</option>
        <option value="300">300</option>
        <option value="400">400</option>
        <option value="500">500</option>
      </select>
      <br>
      <input type="submit" value="ADD">
    </form>
  </div>
</template>
 
<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  name: "AddVenue",
  components: {
        adminav: AdminNavbar,
    },
  data() {
    return {
      venueName: "",
      location: "",
      capacity: ""
    };
  },
  methods: {
    addVenue() {
      fetch('http://127.0.0.1:5000/api/admin/venue', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Authorization': localStorage.getItem('accessToken')
        },
        body: JSON.stringify({
          venue_name: this.venueName,
          address: this.location,
          capacity: this.capacity,
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
            this.$router.push({ name: "AdminDashboard" });
          }
          else {
            alert(data.message);
            this.$router.push({ name: "AdminDashboard" })
          }

        })
        .catch(error => {
          alert(error.message);
          this.$router.push({ name: "AdminDashboard" })
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

.cont {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: aliceblue;
  width: 80%;
  max-width: 550px;
  box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3);
}

.cont h1 {
  text-align: center;
  margin-top: 0.7rem;
  margin-bottom: 1.5rem;
}

input[type="number"],
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
</style>  -->
  