<template>
    <usernav></usernav>

    <div class="container">
        <form class="form-1" @submit.prevent="book">
            <h1>Book Show</h1>
            <p>Show: {{ movie_name }}</p>
            <p>Venue: {{ venue_name }}</p>
            <p>Start: <input type="datetime-local" :value="start" disabled /></p>
            <p>End: <input type="datetime-local" :value="end" disabled /></p>
            <p>Tickets Available: {{ available_capacity - noOfTickets }}</p>

            <label for="seat">No of Tickets:</label>
            <select id="seat" name="seat" required v-model="noOfTickets">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="50">50</option>
            </select>

            <input type="submit" value="Book" class="btn btn-primary" style="margin-left: 380px;"/>
        </form>
    </div>
</template>

<script>
import UserNavbar from "./UserNavbar.vue";

export default {
    components: {
        usernav: UserNavbar,
    },
    name: "TicketBooking",
    data() {
        return {
            movie_name: "",
            venue_name: "",
            start: "",
            end: "",
            available_capacity: 0,
            noOfTickets: "",
        };
    },
    methods: {
        book() {
            fetch(`http://127.0.0.1:5000/api/book/${this.$route.params.sid}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: localStorage.getItem("token"),
                },
                body: JSON.stringify({
                    no_of_tickets: this.noOfTickets,
                    uid: localStorage.getItem("uid"),
                }),
            })
                .then((res) => {
                    if (res.ok) {
                        return res.json();
                    } else {
                        if (res.status === 401) {
                            throw new Error("Token is not passed or invalid!");
                        }
                        if (res.status === 409) {
                            throw new Error("Oops! Show is Housefull.");
                        }
                        if (res.status === 403) {
                            throw new Error("User access required");
                        } else {
                            throw new Error(res.status);
                        }
                    }
                })
                .then((data) => {
                    if (data.error) {
                        alert(data.error);
                        this.$router.push({ name: "UserDashboard" });
                    }
                    else {
                        alert(data.message);
                        this.$router.push({ name: "UserDashboard" });
                    }
                })
                .catch((error) => {
                    alert(error.message);
                    this.$router.push({ name: "UserDashboard" });
                });
        },
    },
    mounted() {
        fetch(`http://127.0.0.1:5000/api/admin/show/${this.$route.params.sid}`, {
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
                this.venue_name = data.venue_name;
                this.movie_name = data.movie_name;
                this.start = data.start;
                this.end = data.end;
                this.available_capacity = data.total_capacity - data.ticket_booked;
                this.ticketPrice = data.ticket_price;
            })
            .catch((error) => {
                alert(error.message);
                this.$router.push({ name: "UserDashboard" });
            });
    },
};
</script>

<style scoped>
.container {
    margin: 50px auto;
    max-width: 500px;
    background-color: aliceblue;
}

.form-1 {
    padding: 20px;
    width: 100%;
    max-width: 500px;
    /* border: 1px solid #ccc;
    border-radius: 4px; */
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

input[type="datetime-local"],
select {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
}

input[type="submit"] {
    cursor: pointer;
    margin-top: 10px;
    margin-right: 0;
}
</style>
