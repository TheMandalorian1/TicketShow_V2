<template>
  <usernav></usernav>
  <div style="max-height: 91vh; min-height: 91vh; width: 100%; overflow: auto">
    <div class="flex-container" style="min-height: 400px; margin-bottom: 10px;">
      <template v-if="movieDetails.length > 0">
        <template v-for="m in movieDetails.slice().reverse()">
          <div class="card">
            <img :src="getImageUrl(m.picture)" class="card-img-top" alt="..."
              style="object-fit: fill; height: 200px; width: 300px;" />

            <div class="card-header"><i class="bi bi-film"></i> {{ m.movie_name }}</div>

            <ul class="list-group list-group-flush">
              <li class="list-group-item" style="max-height: 40.8px; overflow-y: auto;">{{ m.description }}</li>
              <li class="list-group-item">
                <i class="bi bi-star-fill" style="color: gold;"></i> {{ m.movie_rating }} / 10
              </li>
            </ul>
            <p style="margin-bottom: 0px; margin-top: 6px;">
              <router-link :to="{ path: '/search', query: { mid: m.movie_id } }">
                <button class="btn btn-success" style="margin-left: 100px; margin-right: 10px;">
                  Book Now
                </button>
              </router-link>
              <router-link :to="{ path: '/rate', query: { mid: m.movie_id } }">
                <button class="btn btn-warning">
                  <i class="bi bi-star-fill"></i> Rate
                </button>
              </router-link>
            </p>
          </div>
        </template>
      </template>
    </div>

    <div class="flex-container" style="margin: 0px; border: 0px solid black">
      <template v-if="showDetails.length > 0">
        <div v-for="s in showDetails.slice().reverse()" :key="s.show_id" class="card show">
          <div class="card-header">Show | {{ s.movie_name }}</div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" id="list">Venue | {{ s.venue_name }}</li>
            <li class="list-group-item" id="list">
              Rating: &nbsp; <i class="bi bi-star-fill"></i> &nbsp;
              {{ s.movie_rating }} / 10
            </li>
            <li class="list-group-item" id="list">

              <template v-if="s.total_capacity - s.ticket_booked === 0">
                Show is Housefull &nbsp; &nbsp;|
                &nbsp;&nbsp; Price: <i class="bi bi-currency-rupee"></i>{{ s.ticket_price }}
              </template>
              <template v-else>
                Seats Available: {{ s.total_capacity - s.ticket_booked }} &nbsp; &nbsp;|
                &nbsp;&nbsp; Price: <i class="bi bi-currency-rupee"></i>{{ s.ticket_price }}
              </template>

            </li>
            <li class="list-group-item" id="list">
              <i class="bi bi-clock-fill"></i> Start |
              {{ s.start.replace("T", "") }} <i class="bi bi-clock-fill"></i>  &nbsp;&nbsp; End | {{ s.end.replace("T", " ") }}
            </li>
          </ul>
          <template v-if="s.total_capacity - s.ticket_booked === 0">
            <button class="btn btn-danger" style="margin-top: 4px; margin-left: 300px; margin-right: 10px;">
              Housefull
            </button>
          </template>
          <template v-else>
          <router-link :to="{ path: `/book/${s.show_id}` }">
            <button class="btn btn-primary" style="margin-top: 4px; margin-left: 310px;">
              Book Now
            </button>
          </router-link>
        </template>
        </div>
      </template>
    </div>
  </div>
</template>
  
<script>
import UserNavbar from './UserNavbar.vue';

export default {
  components: {
    usernav: UserNavbar,
  },
  data() {
    return {
      name: '',
      searchQuery: '',
      movieDetails: [],
      showDetails: []
    };
  },
  methods: {
    getImageUrl(picture) {
      return '/src/images/' + picture;
    },

    formatDateTime(dateTime) {
      return dateTime.replace('T', ' ');
    },

  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/dashboard`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        'Authorization': localStorage.getItem('token')
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
            throw new Error("User access required");
          } else {
            throw new Error(res.status);
          }
        }
      })
      .then((data) => {
        this.movieDetails = data.movies;
        this.showDetails = data.shows;
        this.name = localStorage.getItem('uname')
      })
      .catch(error => {
        console.log(error);
        alert(error.message);
        this.$router.push({ name: "Login" })
      });
  }
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

::-webkit-scrollbar {
  width: 8px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 30px;
  border: 1px solid #75d2f1;
  background-color: #75d2f1;
}

::-webkit-scrollbar-thumb:hover {
  background: #75d2f1;
}

.flex-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-y: none;
  overflow-x: scroll;
  height: 280px;
}

.card {
  flex: 0 0 auto;
  width: 300px;
  height: 375px;
  margin-top: 5px;
  margin-left: 5px;
  margin-right: 5px;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.show {
  flex: 0 0 auto;
  width: 425px;
  height: 255px;
  margin-top: 5px;
  margin-left: 5px;
  margin-right: 5px;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

ul {
  display: flex;
}

.list-group-flush {
  display: flex;
}

.list-group-item {
  background-color: aliceblue;
  overflow-y: auto;
  max-width: 300px;
  max-height: 40.8px;
}

#list {
  max-width: 450px;
}

::-webkit-scrollbar {
  width: 8px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 30px;
  border: 1px solid #ccc;
  background-color: #deeaee;
}

::-webkit-scrollbar-thumb:hover {
  background: #ccc;
}

.card-header {
  font-weight: bold;
  overflow-y: auto;
  max-height: 40.8px;
  /* min-height: 40.8px; */
  border-bottom: 1px solid #000000;
}

.list-group-item {
  overflow-y: auto;
  max-width: 300px;
  max-height: 40.8px;
}</style>