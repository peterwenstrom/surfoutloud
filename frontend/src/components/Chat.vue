<template>
  <div id = "chat">


    <!--<div>
      <h5>Active Users</h5>
      <ul>
        <li v-for="item in activeUser.user">
          {{ item }}
        </li>
        <li v-for="item in activeUser.inRoom">
          {{ item }}
        </li>
      </ul>
    </div>-->




    <div id = "sendMessage">
      <!--<input v-model="roomNo" v-on:keyup.enter="joinRoom" placeholder="roomNo"/>
      <button class="send-btn btn" v-on:click="joinRoom">Activate room</button>

      <input v-model="roomNo" v-on:keyup.enter="leaveRoom" placeholder="roomNo"/>
      <button class="send-btn btn" v-on:click="leaveRoom">Deactivate room</button>
      <p>Current room number: No room selected</p>-->

      <div class="messageWin">
      <div v-for="(history, index) in history">
        <p class = "me" v-if="history.from = 'me'">{{ history.message }}</p>
        <p class = "you" v-else>{{ history.message }}</p>
      </div>
      </div>


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
        roomNo: "1",
        selectedRoomNo: [],
        history: [
          { from: '' },
          { message: '' }
        ],
        socket: io.connect('http://127.0.0.1:5000'),
        chatmessage: {
            msg: "",
            from: ""
        },
        activeUser: {
            user: [],
            inRoom: []
        }
      }
    },
    methods: {
      sendInRoom: function () {
          this.chatmessage.from = this.authUser.username;

          this.socket.emit('sendInRoom', {data: this.chatmessage, room: this.roomNo});
      },
      sendInRoomResponse: function() {
        //recieving messages and pushing the messages to the history array

        this.socket.on('room_response', function(response) {
              console.log("from: " + this.authUser.username);
              console.log("responsefrom: " + response.data.from);
              if(response.data.from === this.authUser.username){
                this.history.push({ from: 'me' });
                this.history.push({ message: response.data.msg});
                //+ " /--/ sent in room " + response.room

              }else{
                this.history.push({ from: 'you' });
                this.history.push({ message: response.data.from + ": " + response.data.msg});
                //+ " /--/ sent in room " + response.room
              }
              }.bind(this));
      },
      joinRoom: function() {

          /* Right now you can join as many rooms as you like, but not leave them.
           * There is no sign of how many rooms, or which, you are active in.
           * Todo: probably add something visual soon, or it gets pretty messy
           * see todo on "connect".
           * Had some idea of having room 0 as active users, not perfect though */
          this.socket.emit('join', {room: this.roomNo});

          //this should probably be updated after the socket response
          this.selectedRoomNo.push(this.roomNo);
      },
      joinRoomResponse: function() {
        this.socket.on('join_room_response', function(response) {
            let res = response.data.split(",");
            console.log("resTot: " + res);
            console.log("joined room: " + this.roomNo);
            //this.activeUser.inRoom.push(res[1]);
        }.bind(this));
      },leaveRoom: function() {
          this.socket.emit('leave', {room: this.roomNo});

          //this should probably be updated after the socket response
          this.selectedRoomNo.slice(this.selectedRoomNo.indexOf(this.roomNo));
      },
      leaveRoomResponse: function() {
        this.socket.on('leave_room_response', function(response) {
            let res = response.data.split(",");
            console.log("resTot: " + res);
            console.log("left room no: " + this.roomNo);
            //this.activeUser.inRoom.push(res[1]);
        }.bind(this));
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


      this.joinRoom();
      this.sendInRoomResponse();
      this.joinRoomResponse();
      this.leaveRoomResponse();
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
  .messageWin{
    overflow: scroll;
    height: 200px;
    border-style: dashed;
  }
  .me {
    float: right;
  }
  .you {
    float: left;
  }


</style>
