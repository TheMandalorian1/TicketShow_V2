<template>
  <div>

    <adminav></adminav>

    <div style="max-height: 91.5vh; min-height: 50vh; width: 100%; overflow: auto;">
      <div class="flex-container">
        <template v-if="movie_details.length > 0">
          <template v-for="m in movie_details.slice().reverse()">
            <div class="card">
              <img :src="getImageUrl(m.picture)" class="card-img-top" alt="..."
                style="object-fit: fill; height: 200px; width: 300px" />
              <div class="card-header">
                <i class="bi bi-film"></i> {{ m.movie_name }}
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item" style="min-height: 65px">
                  {{ m.description }}
                </li>
                <li class="list-group-item">
                  <i class="bi bi-star-fill" style="color: gold"></i>
                  {{ m.movie_rating }} / 10
                </li>
              </ul>
              <p style="margin-bottom: 0px; margin-top: 6px">
                <router-link :to="'/editmovie/' + m.movie_id">
                  <button class="btn btn-success" style="margin-left: 190px; margin-right: 10px; border-radius: 18px;">
                    <i class="bi bi-pencil"></i>
                  </button>
                </router-link>
                <router-link :to="'/deletemovie/' + m.movie_id">
                  <button class="btn btn-danger" style="border-radius: 18px; ">
                    <i class="bi bi-trash3"></i>
                  </button>
                </router-link>
              </p>
            </div>
          </template>
        </template>
      </div>

      <template v-if="venue_details.length > 0">
        <template v-for="v in venue_details">
          <div class="flex-container"
            style="margin: 3px; border: 5px solid #0c088d; overflow-y: hidden; height: 240px;">
            <div class="card" style="height: 210px; width: 230px; background: rgb(220, 233, 178); border: none; border-radius: 0px;">
              <div class="" style="text-align: center;font-weight: bold;padding-top: 10px; padding-bottom: 10px;">
                {{ v.venue_name }}
              </div>
              <div class="">
                <p class="p">Location: {{ v.venue_location }}</p>
                <p class="p">Total Seats: {{ v.capacity }}</p>
              </div>
              <div class="card-btn p" style="margin-top: 38px;">
                <router-link :to="'/editvenue/' + v.venue_id">
                  <button class="btn btn-success" style="margin-right: 5px; border-radius: 18px;">
                    <i class="bi bi-pencil"></i>
                  </button>
                </router-link>
                <router-link :to="'/deletevenue/' + v.venue_id">
                  <button style="margin-left: 5px; border-radius: 18px;" class="btn btn-danger">
                    <i class="bi bi-trash3"></i>
                  </button>
                </router-link>
                <router-link :to="'/addshow/' + v.venue_id">
                  <button class="card-btn btn btn-primary" style="margin-left: 10px; border-radius: 18px;">
                    <i class="bi bi-plus-circle"></i>
                  </button>
                </router-link>
              </div>
            </div>

            <template v-if="v.shows.length > 0">
              <template v-for="s in v.shows.slice().reverse()">
                <div class="card" style="height: 210px; width: 400px">
                  <div class="" style="text-align: center; font-weight: bold; padding-top: 10px;padding-bottom: 10px;">
                    Show | {{ s.movie_name }}
                  </div>
                  <div class="">
                    <p class="p" id="list">Venue | {{ s.venue_name }}</p>
                    <p class="p" id="list">
                      Tickets Available | {{ s.total_capacity }} &nbsp; &nbsp;||&nbsp; &nbsp; Price |
                      <i class="bi bi-currency-rupee"></i> {{ s.ticket_price }}
                    </p>
                    <p class="p" id="list">
                      <i class="bi bi-clock-fill"></i> Start:
                      {{ formatDateTime(s.start) }} &nbsp; &nbsp;
                      <i class="bi bi-clock-fill"></i>
                      {{ formatDateTime(s.end) }}
                    </p>
                  </div>
                  <div class="card-btn p">
                    <router-link :to="'/editshow/' + s.show_id">
                      <button class="btn btn-success p" style="margin-left: 250px; margin-right: 10px; border-radius: 18px;">
                        <i class="bi bi-pencil"></i>
                      </button>
                    </router-link>
                    <router-link :to="'/deleteshow/' + s.show_id">
                      <button class="btn btn-danger p" style="border-radius: 18px;">
                        <i class="bi bi-trash3"></i>
                      </button>
                    </router-link>
                  </div>
                </div>
              </template>
            </template>
          </div>
        </template>
      </template>
    </div>
  </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
  name: "AdminDashboard",

  components: {
    adminav: AdminNavbar,
  },
  data() {
    return {
      movie_details: [],
      venue_details: [],
    };
  },
  methods: {
    formatDateTime(dateTime) {
      return dateTime.replace("T", " ");
    },

    getImageUrl(filename) {
      return "/src/images/" + filename;
    },
  },
  mounted() {
    fetch(`http://127.0.0.1:5000/api/admin/dashboard`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("accessToken"),
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
          } else {
            throw new Error(res.status);
          }
        }
      })
      .then((data) => {
        this.movie_details = data.movies;
        this.venue_details = data.venues;
      })
      .catch((error) => {
        console.log(error);
        alert(error.message);
        this.$router.push({ name: "AdminLogin" });
      });
  },
};
</script>

<style scoped>
.p {
  text-align: center;
}

h1,
h2 {
  text-align: center;
}

.list-group-item {
  max-height: 40.8px;
  min-height: 40.8px;
  width: 300px;
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

.flex-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-y: none;
  overflow-x: scroll;
  height: 420px;
}

.card {
  flex: 0 0 auto;
  width: 300px;
  height: 400px;
  margin-top: 5px;
  margin-left: 5px;
  margin-right: 5px;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  font-weight: bold;
  overflow-y: auto;
  max-height: 40.8px;
  /* min-height: 40.8px; */
  border-bottom: 1px solid #000000;
}

ul {
  display: flex;
}

.list-group-flush {
  display: flex;
}

.list-group-item {
  overflow-y: auto;
  max-width: 300px;
  max-height: 40.8px;
}
</style>
