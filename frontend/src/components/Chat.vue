<template>
  <div id="chat">
      <div class="row">
        <div class="col-md-12">
          <div class="panel panel-primary">
            <ul id="chat-window" class="panel-body chat">
              <li v-for="value in history">
                <span class="bubble bubble-alt" v-if="value.who === 'me'">
                  <div class="chat-body clearfix">
                    {{ value.message }}
                  </div>
                </span>
                <span class = "bubble" v-if="value.who === 'you'">
                  <div class="chat-body clearfix">
                    {{ value.message }}
                  </div>
                </span>
              </li>
            </ul>

            <div class="panel-footer">
              <div class="input-group">
                <input id="btn-input" type="text" class="form-control input-sm" placeholder="Type your message here..." v-model="chatmessage.msg" v-on:keyup.enter="sendInRoom" />
                <span class="input-group-btn">
                  <button class="btn btn-sm send-btn" id="btn-chat" v-model="chatmessage.msg" v-on:click="sendInRoom">
                    Send</button>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import '../flask-socketio.js'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Chat',
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
        username: '',
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
        console.log("thisroom no:");
        console.log(this.roomNo);
        this.socket.emit('sendInRoom', {data: this.chatmessage, room: this.roomNo});
        this.chatmessage.msg = '';
      },
      sendInRoomResponse: function() {
        //recieving messages and pushing the messages to the history array
        this.socket.on('room_response', function(response) {
          let element = document.getElementById('chat-window');
          const scroll = element.scrollHeight - element.scrollTop;
          if (response.data.who === this.authUser.username){
            this.history.push({ who: 'me',message: response.data.msg});
            setTimeout( () => {
              element = document.getElementById('chat-window');
              element.scrollTop = element.scrollHeight

            }, 100)
          } else {
            this.history.push({ who: 'you', message: response.data.who + ": " + response.data.msg});
            setTimeout( () => {
              if (scroll < 330) {
                element = document.getElementById('chat-window');
                element.scrollTop = element.scrollHeight
              }
            }, 100)
          }

        }.bind(this));
      },
      joinRoom: function() {
        this.socket.emit('join', {who: this.authUser.username, room: this.roomNo});
      },
      joinRoomResponse: function() {
        this.socket.on('join_room_response', function(response) {
          let res = response.data.split(",");
          console.log("resTot: " + res);
          console.log("joined room: " + this.roomNo);
        }.bind(this));
      },
      leaveRoom: function() {
        this.socket.emit('leave', {who: this.username, room: this.roomNo});
      },
      leaveRoomResponse: function() {
        this.socket.on('leave_room_response', function(response) {
          let res = response.data.split(",");
          console.log("resTot: " + res);
          console.log("left room no: " + this.roomNo);
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
      },
      newMemberJoin: function () {
        this.socket.on('member_join_response', function(response) {

            console.log("member_joinresponse: ");
            console.log(response);
            this.$emit('member_join', response.data);


        }.bind(this));
      },
      handleClose() {
        this.leaveRoom();
        return null
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    mounted () {
      this.username = this.authUser.username
    },
    created () {

      window.addEventListener('beforeunload', this.handleClose);

      this.joinRoom();
      this.sendInRoomResponse();
      this.joinRoomResponse();
      this.leaveRoomResponse();
      this.pingUser();
      this.pongUser();
      this.newMemberJoin();
    },
    beforeDestroy() {
      this.leaveRoom();
      window.removeEventListener('beforeunload', this.handleClose);
    }
  };


</script>

<style scoped>
  #chat-window {
    border: 1px solid rgba(0, 0, 0, 0.15);
    border-radius: 0.25rem;
    transition: transform 1s;
  }

  .send-btn {
    background-color: #35495E;
    color: #fff;
    cursor: pointer;
  }

  /** page structure **/
  .container {
    padding: 40px 20px;
    margin: 0 auto;
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
    margin: 5px 5px 5px 5px;
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

    border: solid 1px rgba(0,0,0,0.1);
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
    padding: 0;
  }

  .panel .slidedown .glyphicon, .chat .glyphicon
  {
    margin-right: 5px;
  }

  .panel-body
  {
    overflow-x: hidden;
    overflow-y: scroll;
    height: 330px;
    margin-bottom: 5px;
  }
</style>
