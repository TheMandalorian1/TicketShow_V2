<template>

<usernav></usernav>

    <div class="flex-container">
        <div v-if="my_shows.length > 0" v-for="s in my_shows.slice().reverse()" :key="s.movie_name" class="card"
            style="height: 270px; width: 485px; margin: 8px">
            <div class="card-header">Show | {{ s.movie_name }}</div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item" id="list">Venue | {{ s.venue_name }}</li>
                <li class="list-group-item" id="list">
                    Rating: {{ s.movie_rating }} / 10
                </li>
                <li class="list-group-item" id="list">
                    Seats Booked: {{ tickets[s.show_id] }} &nbsp; &nbsp;| &nbsp;&nbsp;
                    Price: <i class="bi bi-currency-rupee"></i>{{ s.ticket_price * tickets[s.show_id] }}
                </li>
                <li class="list-group-item" id="list">
                    <i class="bi bi-clock-fill"></i> Start |
                    {{ s.start.replace('T', ' ') }}
                </li>
                <li class="list-group-item" id="list">
                    <i class="bi bi-clock-fill"></i> End |
                    {{ s.end.replace("T", " ") }}
                </li>
            </ul>
        </div>
        <!-- <h2 v-else>You haven't booked any shows yet!</h2> -->
    </div>
</template>


<script>
import UserNavbar from './UserNavbar.vue';

export default {
    name: "BookedShow",
    components: {
        usernav: UserNavbar,
    },
    data() {
        return {
            name: '',
            my_shows: [],
            tickets: {}
        };
    },
    mounted() {
        const uid = localStorage.getItem('uid')
        fetch(`http://127.0.0.1:5000/api/booked/${uid}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: localStorage.getItem("token"),
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
                this.my_shows = data.shows;
                this.tickets = data.tickets;
                this.name = localStorage.getItem("uname");
                console.log(this.my_shows)
            })
            .catch((error) => {
                console.log(error);
                alert(error.message);
                this.$router.push({ name: "Login" });
            });
    },
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
    height: 180px;
    margin-right: 10px;
    background-color: rgb(235, 171, 178);
    border: 1px solid #ddd;
    box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.list-group-item {
    background-color: rgb(246, 231, 231);
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
