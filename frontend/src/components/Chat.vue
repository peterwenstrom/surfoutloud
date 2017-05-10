<template>
  <div id = "chat">

      <p v-for="(history, index) in history">{{ history }}</p>


    <div id = "sendMessage">
      <input v-model="roomNo" v-on:keyup.enter="joinRoom" placeholder="roomNo"/>
      <button class="send-btn btn" v-on:click="joinRoom">Activate room</button>
      <p>Current room number: {{ selectedRoomNo }}</p>
      <input v-model="chatmessage.msg" v-on:keyup.enter="sendInRoom"/>
      <!-- Todo: if room number not specified = disable send button-->
      <button class="send-btn btn" v-on:click="sendInRoom">Send</button>
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
        roomNo: "",
        selectedRoomNo: "No room selected",
        history: [],
        socket: io.connect('http://127.0.0.1:5000'),
        chatmessage: {
            msg: "",
            from: ""
        }
      }
    },
    methods: {
      sendInRoom: function () {
          this.chatmessage.from = this.authUser.username;
          this.socket.emit('sendInRoom', {data: this.chatmessage, room: this.roomNo});
      },
      joinRoom: function() {
          this.socket.emit('join', {room: this.roomNo});

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
          //todo: greenlight active members in the project
        //this.socket.send(this.authUser.username + ' has connected!');
      }.bind(this));

    //recieving messages and pushing the messages to the history array
      this.socket.on('join_room_response', function(response) {
          console.log(response.data);
          this.selectedRoomNo = response.data.inRoom;
      }.bind(this));

      this.socket.on('room_response', function(response) {
          console.log(response.data);
          this.history.push(response.data.from + ": " + response.data.msg);
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
