<template>
    <adminav></adminav>

    <div class="flex-container" style="margin: 0px; border: 0px solid black">
        <div v-if="venues.length > 0" v-for="v in venues.slice().reverse()" :key="v.venue_id" class="card">
            <div class="card-header">Venue | {{ v.venue_name }}</div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item" id="list">Address | {{ v.venue_location }}</li>
                <li class="list-group-item" id="list">Capacity: {{ v.capacity }}</li>
            </ul>
            <button class="btn btn-success" @click="exported(v.venue_id)">Export</button>
        </div>
        <h2 v-else>No venue is available!</h2>
    </div>
</template>
  
<script>
import AdminNavbar from './AdminNavbar.vue';

export default {
    components: {
        adminav: AdminNavbar,
    },
    name: "ExportVenue",
    data() {
        return {
            venues: []
        }
    },
    methods: {
        exported(venue_id) {
            fetch(`http://127.0.0.1:5000/api/admin/export/${venue_id}`, {
                method: "POST",
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
                    if (data.error) {
                        alert(error.error);
                        this.$router.push({ name: "AdminDashboard" });
                    } else {
                        alert(data.message);
                        this.$router.push({ name: "AdminDashboard" });
                    }
                })
                .catch((error) => {
                    alert(error.message);
                    this.$router.push({ name: "AdminDashboard" });
                });
        }

    },
    mounted() {
        fetch(`http://127.0.0.1:5000/api/admin/export`, {
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
                this.venues = data.venues;
            })
            .catch((error) => {
                console.log(error);
                alert(error.message);
                this.$router.push({ name: "AdminDashboard" });
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

.flex-container {
    display: flex;
    flex-wrap: wrap;
    max-height: 90vh;
    min-height: 90vh;
    max-width: 100%;
    overflow-y: auto;
    scroll-margin-right: 0px;
}

.card {
    margin: 6px;
    flex: 0 0 auto;
    width: 400px;
    height: 162px;
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
  