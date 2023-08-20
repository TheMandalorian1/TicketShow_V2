<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-navbar-light bg- bgcolor">
    <router-link to="/dashboard" class="navbar-brand">TicketShow : {{ name }} </router-link>
    <!-- Toggle button for small screens -->
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav"
      aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon navbar-toggler-white"></span>
    </button>


    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">

        <!-- Search Box -->
        <li class="nav-item">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" 
          @keyup.enter="search" name="query" v-model="searchQuery" style="height: 38px; width: 230px;">
        </li>
        <li class="nav-item">
          <button type="submit" class="btn btn-primary" @click="search" style="margin-right: 10px; margin-left: 5px">
            <i class="bi bi-search"></i>
          </button>
        </li>

        <li class="nav-item">
          <router-link :to="{ path: '/booked' }">
            <button class="btn btn-primary">Booked</button>
          </router-link>
        </li>

        <li class="nav-item">
          <button class="btn btn-danger ml-3" @click="logout" style="margin-left: 5px">
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      searchQuery: '',
    };
  },
  methods: {
    search() {
      this.$router.push({ path: "/search", query: { q: this.searchQuery } });
    },

    getImageUrl(picture) {
      return '/src/images/' + picture;
    },

    formatDateTime(dateTime) {
      return dateTime.replace('T', ' ');
    },

    logout() {
      fetch(`http://127.0.0.1:5000/api/logout`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          localStorage.removeItem('token');
          localStorage.removeItem("uname");
          this.$router.replace({ name: "Login" })
        })
        .catch((error) => {
          console.log(error);
          alert(+ error.message);
          this.$router.push({ name: "UserDashboard" });
        });
    },
  },
  mounted() {
    this.name = localStorage.getItem('uname');
  }
};
</script>


<style scoped>
.bgcolor {
  background-color: #0c088d;
  min-height: 60px;
}

.nav-link {
  color: white;
  font-size: larger;
}

.navbar-brand {
  margin-left: 10px;
  color: white;
  font-weight: bold;
  font-size: x-large;
}

ul {
  margin-right: 10px;
}

.navbar-toggler-white {
  color: white;
  background-color: white;
}
</style>