<template>
  <div id="chat">
    <ul id="messages"></ul>
    <input v-model="msg"/>
      <button v-on:click="send">Skicka</button>
    <ul>
      <li
        v-for="(history, index) in history"
      >{{ history }}</li>
    </ul>
  </div>


</template>

<script>
  import Vue from 'vue'
    var vm = new Vue ( {
      el: '#chat',
    name: 'chat',
    data: {
        msg: "",
        history: [

        ]
    },
    methods: {
      send: function (event) {
        if (event) {
          socket.send(this.msg);
          //this.history.push(this.msg)
          this.msg = ''
        }
      }
    }
  })

/*  export default {
    name: 'chat',
    data () {
      return {
        msg: "lol",
        history: [

        ]
      }
    },
    methods: {
      send: function (event) {
        if (event) {
          socket.send(this.msg);
          this.history.push(this.msg)
          this.msg = ''
        }
      }
    }
  }*/

  var socket = io.connect('http://127.0.0.1:5000');
  socket.on('connect', function() {
    socket.send('User has connected!');
  });

  socket.on('message', function (msg) {
    vm.history.push(msg);
    console.log('Received message: ' + msg);
  });


</script>

<style>
  #chat {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
