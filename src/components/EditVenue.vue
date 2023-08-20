<template>
  <adminav></adminav>

  <div class="container">
    <form class="form-1" @submit.prevent="editVenue">
      <h1>Edit Venue</h1>
      <label for="venue_name">Venue Name:</label>
      <input type="text" id="venue_name" v-model="venueName" required>
      <br>
      <label for="location">Location:</label>
      <input type="text" id="location" v-model="location" required>
      <br>
      <label for="capacity">Capacity:</label>
      <select id="capacity" v-model="capacity">
        <option :value="capacity">{{ capacity }}</option>
        <option :value="capacity + 25">{{ capacity + 25 }}</option>
        <option :value="capacity + 50">{{ capacity + 50 }}</option>
        <option :value="capacity + 100">{{ capacity + 100 }}</option>
        <option :value="capacity + 200">{{ capacity + 200 }}</option>
      </select>
      <br>
      <input type="submit" value="Edit">
    </form>
  </div>
</template>
  
<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  name: 'EditVenue',
  components: {
    adminav: AdminNavbar,
  },

  data() {
    return {
      venueName: "",
      location: "",
      capacity: "",
    };
  },
  methods: {
    editVenue() {
      fetch(`http://127.0.0.1:5000/api/admin/venue/${this.$route.params.vid}`, {
        method: "PUT",
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
        .then((res) => res.json())
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
  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/admin/venue/${this.$route.params.vid}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'Authorization': localStorage.getItem('accessToken')
      },
    })
      .then((res) => res.json())
      .then((data) => {
        this.venueName = data.venue_name;
        this.location = data.venue_location;
        this.capacity = data.capacity;
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
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: aliceblue;
  width: 80%;
  max-width: 550px;
  box-shadow: 0 19px 38px rgba(0, 0, 0, 0.3);
}

.form-1 h1 {
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
</style>
  