<template>
           <!-- this shouldn't be here. but for now, there is no other place to put it -->
          <div id = "chat">
            <ul>
            <li v-for="(history, index) in history">{{ history }}</li>
            </ul>

            <div id = "sendMessage">
              <input v-model="msg"/>
              <button v-on:click="send">Skicka</button>
            </div>
          </div>

</template>

<script>
  import '../flask-socketio.js'
  export default {
    name: 'chat',
    data() {
    return {
        msg: "",
        history: [

        ]
      }
    },
    methods: {
      send: function () {
          let username = this.$store.state.userStore.authUser.username;
          socket.send(username + ": " + this.msg);
          this.msg = ''
      }
    },
    computed: {
        user () {
            return this.$store.state.authUser;
        }
    },
    mounted () {
        //connecting the user

      socket.on('connect', function() {
      //socket.send('User has connected!');
      });

    //recieving messages and pushing the messages to the history array
      socket.on('message', function (msg) {
      this.history.push(msg);
      console.log('Received message: ' + msg);
      }.bind(this));
    }
  };

  let socket = io.connect('http://127.0.0.1:5000');
  //need to have this instance because the ease of accessing the history array from outside
/*  import Vue from 'vue'
    var vm = new Vue ( {
      el: "#chat",
      data: {
        history: [

        ]
      }
  });*/
</script>

<style>
  #sendMessage {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
