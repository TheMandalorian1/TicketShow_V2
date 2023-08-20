<template>
  <usernav></usernav>

  <div class="flex-container">
    <template v-if="matchedShows.length > 0">
      <div v-for="s in matchedShows.slice().reverse()" :key="s.show_id" class="card"
        style="height: 270px; width: 485px; margin: 8px">
        <div class="card-header">Show | {{ s.movie_name }}</div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item" id="list">Venue | {{ s.venue_name }}</li>
          <li class="list-group-item" id="list">
            Rating: &nbsp; <i class="bi bi-star-fill"></i> &nbsp;
            {{ s.movie_rating }} / 10
          </li>
          <li class="list-group-item" id="list">
            Seats Available: {{ s.available_capacity }} &nbsp; &nbsp;|
            &nbsp;&nbsp; Price: <i class="bi bi-currency-rupee"></i>{{ s.ticket_price }}
          </li>
          <li class="list-group-item" id="list">
            <i class="bi bi-clock-fill"></i> Start |
            {{ s.start.replace("T", "") }} &nbsp; &nbsp;
            <i class="bi bi-clock-fill"></i> End | {{ s.end.replace("T", " ") }}
          </li>
        </ul>
        <div class="card-body" style="">
          <router-link :to="{ path: `/book/${s.show_id}` }">
            <button class="btn btn-success" style="margin-left: 350px; ">
              Book Now
            </button>
          </router-link>
        </div>
      </div>
    </template>
    <template v-else>
      <h3>No shows matching your search!</h3>
    </template>
  </div>
</template>

<script>
import UserNavbar from './UserNavbar.vue';

export default {
  components: {
    usernav: UserNavbar,
  },
  name: "SearchResult",
  data() {
    return {
      matchedShows: [],
    };
  },
  methods: {
    searchShows() {
      if ("mid" in this.$route.query) {
        fetch(`http://127.0.0.1:5000/api/search?mid=${this.$route.query.mid}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            'Authorization': localStorage.getItem('token')
          },
        })
          .then((res) => res.json())
          .then((data) => {
            this.matchedShows = data.matched_shows;
          })
          .catch((error) => {
            console.log(error);
            alert(error.message);
            this.$router.push({ name: "UserDashboard" });
          });
      } else {
        fetch(`http://127.0.0.1:5000/api/search?q=${this.$route.query.q}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            'Authorization': localStorage.getItem('token')
          },
        }
        )
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
            this.matchedShows = data.matched_shows;
          })
          .catch((error) => {
            console.log(error);
            alert(error.message);
            this.$router.push({ name: "UserDashboard" });
          });
      }
    },
  },
  mounted() {
    this.searchShows()
  },
  watch: {
    // Watch for changes in the query object of the route
    '$route.query': {
      handler(newQuery, oldQuery) {
        // Check if the query has changed
        if (JSON.stringify(newQuery) !== JSON.stringify(oldQuery)) {

          // Reload the page when the query changes
          // location.reload()

          // Remount the page when the query changes
          this.searchShows()

        }
      },
      deep: true // Watch for nested changes in the query object
    }
  }
};
</script>

<style scoped>
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    border-radius: 30px;
    border: 1px solid #ccc;
    background-color: #deeaee;
}

::-webkit-scrollbar-thumb:hover {
    background: #ccc;
}

body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    font-family: sans-serif;
}


h1 {
    margin: 20px;
}

.flex-container {
    display: flex;
    flex-wrap: wrap;
    max-height: 90.7vh;
    min-height: 89vh;
    max-width: 100%;
    overflow-y: auto;
    scroll-margin-right: 0px;
}

.card {
    margin: 6px;
    flex: 0 0 auto;
    width: 485px;
    height: 150px;
    margin-right: 10px;
    background-color: #f2f2f2;
    box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.list-group-item {
    /* background-color: rgb(246, 231, 231); */
    overflow: auto;
    max-width: 485px;
    max-height: 40.8px;
}

.card-header {
    font-weight: bold;
    overflow: auto;
    max-width: 485px;
    max-height: 40.8px;
    min-height: 40.8px;
}
</style>
