<template>
  <div id = "chat">

      <p v-for="(history, index) in history">{{ history }}</p>


    <div id = "sendMessage">
      <input v-model="msg" v-on:keyup.enter="send"/>
      <button class="send-btn btn" v-on:click="send">Send</button>
    </div>
  </div>

</template>

<script>
  import '../flask-socketio.js'
  import {mapGetters} from 'vuex'

  export default {
    name: 'chat',
    data() {
    return {
        msg: "",
        history: [],
        socket: io.connect('http://127.0.0.1:5000')
      }
    },
    methods: {
      send: function () {
          this.socket.send(this.authUser.username + ": " + this.msg);
          this.msg = ''
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    created () {
        //connecting the user
      this.socket.on('connect', function() {
        this.socket.send(this.authUser.username + ' has connected!');
      }.bind(this));

    //recieving messages and pushing the messages to the history array
      this.socket.on('message', function (msg) {
        this.history.push(msg);
      }.bind(this));
    }
  };


</script>

<style scoped>
  #sendMessage {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  .send-btn {
    background-color: #35495E;
    color: #fff;
  }
</style>
