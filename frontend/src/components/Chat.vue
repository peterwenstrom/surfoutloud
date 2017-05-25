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




    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="panel panel-primary">
            <div id="chatWindow" class="panel-body">
              <ul class="chat">
                <div id="newest" v-for="value in history">
                  <span class = "bubble bubble-alt" v-if="value.who === 'me'">
                    <div class="chat-body clearfix">
                       {{ value.message }}
                    </div>
                    </span>
                  <span class = "bubble" v-if="value.who === 'you'">
                    <div class="chat-body clearfix">
                        {{ value.message }}
                    </div>
                  </span>
                </div>
              </ul>
            </div>
            <div class="panel-footer">
              <div class="input-group">
                <input id="btn-input" type="text" class="form-control input-sm" placeholder="Type your message here..." v-model="chatmessage.msg" v-on:keyup.enter="sendInRoom" />
                <span class="input-group-btn">
                            <button class="btn btn-warning btn-sm send-btn" id="btn-chat" v-model="chatmessage.msg" v-on:click="sendInRoom">
                                Send</button>
                        </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>



    <!--    <div class = "container">
          &lt;!&ndash;<input v-model="roomNo" v-on:keyup.enter="joinRoom" placeholder="roomNo"/>
          <button class="send-btn btn" v-on:click="joinRoom">Activate room</button>

          <input v-model="roomNo" v-on:keyup.enter="leaveRoom" placeholder="roomNo"/>
          <button class="send-btn btn" v-on:click="leaveRoom">Deactivate room</button>
          <p>Current room number: No room selected</p>&ndash;&gt;

          <div v-for="value in history">
            <span class = "bubble bubble-alt" v-if="value.from === 'me'">{{ value.message }}</span>
            <span class = "bubble" v-if="value.from === 'you'">{{ value.message }}</span>
          </div>


          <input v-model="chatmessage.msg" v-on:keyup.enter="sendInRoom"/>
          <button v-model="chatmessage.msg" class="send-btn btn" v-on:click="sendInRoom">Send</button>

        </div>-->
  </div>


</template>

<script>
  import '../flask-socketio.js'
  import {mapGetters} from 'vuex'

  export default {
    name: 'chat',
    props: ['projectId'],
    data() {
      return {
        msg: "",
        roomNo: this.projectId.toString(),
        selectedRoomNo: [],
        history: [
          { who: "", message: "" }
        ],
        socket: io.connect(API_URL),
        chatmessage: {
          msg: "",
          who: ""
        },
        activeUsers: [

        ]

      }
    },
    methods: {
      sendInRoom: function () {
        this.chatmessage.who = this.authUser.username;
        this.socket.emit('sendInRoom', {data: this.chatmessage, room: this.roomNo});
        this.chatmessage.msg = '';
      },
      sendInRoomResponse: function() {
        //recieving messages and pushing the messages to the history array
        this.socket.on('room_response', function(response) {
          if(response.data.who === this.authUser.username){
            this.history.push({ who: 'me',message: response.data.msg});
            //+ " /--/ sent in room " + response.room
          }else{
            this.history.push({ who: 'you', message: response.data.who + ": " + response.data.msg});
            //+ " /--/ sent in room " + response.room
          }

        }.bind(this));
      },
      joinRoom: function() {
          console.log("chat_url: ");
          console.log(CHAT_URL);
        /* Right now you can join as many rooms as you like, but not leave them.
         * There is no sign of how many rooms, or which, you are active in.
         * Todo: probably add something visual soon, or it gets pretty messy
         * see todo on "connect".
         * Had some idea of having room 0 as active users, not perfect though */
        this.socket.emit('join', {who: this.authUser.username, room: this.roomNo});
      },
      joinRoomResponse: function() {
        this.socket.on('join_room_response', function(response) {
          let res = response.data.split(",");
          console.log("resTot: " + res);
          console.log("joined room: " + this.roomNo);
          //this.activeUser.inRoom.push(res[1]);
        }.bind(this));
      },leaveRoom: function() {
        this.socket.emit('leave', {who: this.authUser.username, room: this.roomNo});

      },
      leaveRoomResponse: function() {
        this.socket.on('leave_room_response', function(response) {
          let res = response.data.split(",");
          console.log("resTot: " + res);
          console.log("left room no: " + this.roomNo);
          //this.activeUser.inRoom.push(res[1]);
        }.bind(this));
      },
      pingUser: function() {
        let start_time;
        let self = this;

        start_time = (new Date).getTime();
        this.socket.emit('my_ping', {start: start_time});

        setTimeout(function(){ self.pingUser() }, 5000);


      },
      pongUser: function(){
        let ping_pong_times = [];
        this.socket.on('my_pong', function(response) {
          let latency = (new Date).getTime() - response.data;
          ping_pong_times.push(latency);
          ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
          let sum = 0;
          for (let i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
          console.log(Math.round(10 * sum / ping_pong_times.length) / 10);

          this.activeUsers = response.active_users;
          this.$emit('active', response.active_users);


        }.bind(this));
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    mounted () {

    },
    created () {
      //connecting the user
      //this.socket.on('connect', function() {
      //todo: greenlight active members in the project
      //this.socket.send(this.authUser.username + ' has connected!');
      //}.bind(this));


      this.joinRoom();
      this.sendInRoomResponse();
      this.joinRoomResponse();
      this.leaveRoomResponse();
      this.pingUser();
      this.pongUser();
    },
    //destroyed() {
    //  this.leaveRoom();
    //}
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
  /*.messageWin{
    overflow: scroll;
    height: 200px;
    border-style: dashed;
  }*/

  /*copied css v*/


  /** page structure **/
  .container {
    padding: 40px 20px;
    margin: 0 auto;
    max-width: 700px;
  }


  .datestamp {
    display: block;
    text-align: center;
    font-weight: bold;
    margin-bottom: 8px;
    color: #8b91a0;
    text-shadow: 1px 1px 0 rgba(255,255,255,0.6);
  }


  /** ios1-ios6 bubbles **/
  .bubble {
    box-sizing: border-box;
    float: left;
    width: auto;
    max-width: 80%;
    position: relative;
    clear: both;

    background: #95c2fd;
    background-image: -webkit-gradient(linear, left bottom, left top, color-stop(0.15, #bee2ff), color-stop(1, #95c2fd));
    background-image: -webkit-linear-gradient(bottom, #bee2ff 15%, #95c2fd 100%);
    background-image: -moz-linear-gradient(bottom, #bee2ff 15%, #95c2fd 100%);
    background-image: -ms-linear-gradient(bottom, #bee2ff 15%, #95c2fd 100%);
    background-image: -o-linear-gradient(bottom, #bee2ff 15%, #95c2fd 100%);
    background-image: linear-gradient(bottom, #bee2ff 15%, #95c2fd 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#95c2fd', endColorstr='#bee2ff');

    border: solid 1px rgba(0,0,0,0.5);
    -webkit-border-radius: 20px;
    -moz-border-radius: 20px;
    border-radius: 20px;

    -webkit-box-shadow: inset 0 8px 5px rgba(255,255,255,0.65), 0 1px 2px rgba(0,0,0,0.2);
    -moz-box-shadow: inset 0 8px 5px rgba(255,255,255,0.65), 0 1px 2px rgba(0,0,0,0.2);
    box-shadow: inset 0 8px 5px rgba(255,255,255,0.65), 0 1px 2px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    padding: 6px 20px;
    color: #000;
    text-shadow: 0 1px 1px rgba(255,255,255,0.8);
    word-wrap: break-word;
  }

  .bubble:before, .bubble:after {
    border-radius: 20px / 5px;
    content: '';
    display: block;
    position: absolute;
  }
  .bubble:before {
    border: 10px solid transparent;
    border-bottom-color: rgba(0,0,0,0.5);
    bottom: 0px;
    left: -7px;
    z-index: -2;
  }
  .bubble:after {
    border: 8px solid transparent;
    border-bottom-color: #bee2ff; /* arrow color */
    bottom: 1px;
    left: -5px;
  }

  .bubble-alt {
    float: right;
  }
  .bubble-alt:before {
    left: auto;
    right: -7px;
  }
  .bubble-alt:after {
    left: auto;
    right: -5px;
  }

  .bubble p {
    font-size: 1.4em;
  }

  /* yellow bubble */
  .yellow {
    background: #7acd47;
    background-image: -webkit-gradient(linear,left bottom,left top,color-stop(0.15, #fcf3c3),color-stop(1, #f4e371));
    background-image: -webkit-linear-gradient(bottom, #fcf3c3 15%, #f4e371 100%);
    background-image: -moz-linear-gradient(bottom, #fcf3c3 15%, #f4e371 100%);
    background-image: -ms-linear-gradient(bottom, #fcf3c3 15%, #f4e371 100%);
    background-image: -o-linear-gradient(bottom, #fcf3c3 15%, #f4e371 100%);
    background-image: linear-gradient(bottom, #fcf3c3 15%, #f4e371 100%);
    filter: progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4e371', endColorstr='#fcf3c3');
  }
  .yellow:after {
    border-bottom-color: #fcf3c3;
  }

  /*****/
  .chat
  {
    list-style: none;
    margin: 8px;
    padding: 0;
  }

  .chat li
  {
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px dotted #B3A9A9;
  }

  .chat li.left .chat-body
  {
    margin-left: 60px;
  }

  .chat li.right .chat-body
  {
    margin-right: 60px;
  }


  .chat li .chat-body p
  {
    margin: 0;
    color: #777777;
  }

  .panel .slidedown .glyphicon, .chat .glyphicon
  {
    margin-right: 5px;
  }

  .panel-body
  {
    overflow-y: scroll;
    height: 250px;
  }


  ::-webkit-scrollbar-track
  {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    background-color: #F5F5F5;
  }

  ::-webkit-scrollbar
  {
    width: 12px;
    background-color: #F5F5F5;
  }

  ::-webkit-scrollbar-thumb
  {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
    background-color: #555;
  }





</style>
