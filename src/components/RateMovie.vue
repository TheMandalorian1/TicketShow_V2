<template>

<usernav></usernav>

    <div class="container">
        <div class="box">
            <h2>Rate the Movie!</h2>
            <form @submit.prevent="rateMovie">
                <div class="form-group">
                    <label for="movieName">Movie Name:</label>
                    <input type="text" id="movieName" v-model="movieName" disabled>
                </div>
                <div class="form-group">
                    <label for="description">Description:</label>
                    <textarea id="description" v-model="description" disabled></textarea>
                </div>
                <div class="form-group">
                    <label for="rating">Rating (0-10):</label>
                    <input type="number" id="rating" v-model.number="points" min="1" max="10" step="0.5" required>
                </div>
                <input type="submit" value="Rate" class="btn btn-warning" style="margin-left: 370px; color: black;">
            </form>
            <!-- <div class="cancel-button">
                <button onclick="history.back()" class="btn btn-primary">Cancel</button>
            </div> -->
        </div>
    </div>
</template>
  
<script>
import UserNavbar from './UserNavbar.vue';
export default {
    components: {
        usernav: UserNavbar,
    },
    name: "RateMovie",
    data() {
        return {
            movieName: "",
            description: "",
            points: '',
        };
    },
    methods: {
        rateMovie() {
            fetch(`http://127.0.0.1:5000/api/rate?mid=${this.$route.query.mid}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': localStorage.getItem('token')
                },
                body: JSON.stringify({
                    points: this.points,
                })
            })
                .then((res) => res.json())
                .then((data) => {
                    alert(data.message);
                    this.$router.push({ name: "UserDashboard" })
                })
                .catch(error => {
                    alert(error.message);
                    this.$router.push({ name: "UserDashboard" })
                });
        },
    },
    mounted() {
        fetch(`http://127.0.0.1:5000/api/admin/movie/${this.$route.query.mid}`, {
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
          }else {
            throw new Error(res.status);
          }
        }
      })  
            .then((data) => {
                this.movieName = data.movie_name;
                this.description = data.description;
                this.movieRating = data.movie_rating
            })
            .catch(error => {
                console.log(error);
                alert(error.message);
                this.$router.push({ name: "UserDashboard" })
            });
    }
};
</script>
  
<style scoped>
.container {
    margin: 50px auto;
    max-width: 500px;
}

.box {
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: aliceblue;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="text"],
input[type="number"],
textarea {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
}

input[type="submit"] {
    color: white;
    cursor: pointer;
}

.cancel-button {
    text-align: center;
    margin-top: 10px;
}

</style>
