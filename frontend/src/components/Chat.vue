<template>
  <div id = "sendMessage">
    <input v-model="msg"/>
    <button v-on:click="send">Skicka</button>
  </div>

</template>

<script>
  import '../flask-socketio.js'
  export default {
    name: 'chat',
    data() {
    return {
        msg: ""
      }
    },
    methods: {
      send: function () {
          socket.send(this.msg);
          this.msg = ''
      }
    }
  };
  //need to have this instance because the ease of accessing the history array from outside
  import Vue from 'vue'
    var vm = new Vue ( {
      el: "#chat",
      data: {
        history: [

        ]
      }
  });

//connecting the user
  var socket = io.connect('http://127.0.0.1:5000');
  socket.on('connect', function() {
    socket.send('User has connected!');
  });

//recieving messages and pushing the messages to the history array
  socket.on('message', function (msg) {
      vm.history.push(msg);
      console.log('Received message: ' + msg);
  });

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
