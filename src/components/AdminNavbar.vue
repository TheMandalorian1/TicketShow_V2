<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-navbar-light bg- bgcolor">
        <router-link to="/admin/dashboard" class="navbar-brand">TicketShow : Admin </router-link>

        <!-- Toggle button for small screens -->
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon navbar-toggler-white"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <router-link to="/addvenue" class="nav-link">Add Venue</router-link>
                </li>

                <li class="nav-item">
                    <router-link to="/addmovie" class="nav-link">Add Movie</router-link>
                </li>

                <li class="nav-item">
                    <router-link :to="{ path: '/export' }">
                        <button class="btn btn-success" style="margin-top: 4px; margin-left: 5px">Export</button>
                    </router-link>
                </li>

                <li class="nav-item">
                    <button class="btn btn-danger ml-3" @click="adminLogout" style="margin-top: 4px; margin-left: 5px">
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
        return {};
    },
    methods: {
        adminLogout() {
            localStorage.removeItem("accessToken");
            this.$router.replace({ name: "AdminLogin" });
        },
    },
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
