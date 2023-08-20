<template>
    <adminav></adminav>
    
    <div class="container">
        <h2>Are you sure you want to delete this Venue!</h2>
        <form @submit.prevent="deleteObject">
            <input type="submit" value="Delete" >
        </form>
        <div class="">
            <button onclick="history.back()" class="btn btn-primary"
            style="margin-left: 185px; margin-top: 10px;">Cancel</button>
        </div>
    </div>
</template>
  
<script>
import AdminNavbar from './AdminNavbar.vue'

export default {
    name: "RemoveVenue",
    components: {
        adminav: AdminNavbar,
    },
    data() {
        return {
            confirm: true
        };
    },
    methods: {
        deleteObject() {
            fetch(`http://127.0.0.1:5000/api/admin/venue/${this.$route.params.vid}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'Authorization': localStorage.getItem('accessToken')
                },
                body: JSON.stringify({
                    confirm: this.confirm,
                })
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
          }else {
            throw new Error(res.status);
          }
        }
      })  
                .then((data) => {
                    if (data.error) {
                        alert(data.error);
                        this.$router.push({ name: "AdminDashboard" })
                    }
                    else {
                        alert(data.message);
                        this.$router.push({ name: "AdminDashboard" })
                    }
                })
                .catch(error => {
                    console.log(error);
                    alert(error.message);
                    this.$router.push({ name: "AdminDashboard" })
                });
        },
    },
};
</script>
  
<style scoped>
.container {
    margin: 50px auto;
    max-width: 500px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: rgb(236, 133, 133);
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

input[type="submit"] {
    background-color: #f10d0d;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-left: 180px;
}

</style>