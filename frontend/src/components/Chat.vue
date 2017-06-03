<template>
  <div id="chat">

    <b-tabs>

      <template v-for="(item,index) in openChatRooms">
        <b-tab :title="item" @click="openRoom(item)">
          <div class="row">
            <div class="col-md-12">
              <div class="panel panel-primary">

                <ul id="chat-window" class="panel-body chat">
                  <div v-show="!(item === 'room')">
                    <b-btn size="sm" variant="danger" class="float-right" @click="closeRoom(item)">Close chat</b-btn>
                  </div>
                  <li v-for="value in chatArray[index].history">

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
                    <input id="btn-input"
                           class="form-control input-sm"
                           type="text"
                           placeholder="Type your message here..."
                           v-model="chatMessage.message"
                           v-on:focus="openRoom(item)"
                           v-on:keyup.enter="sendInRoom" />
                    <span class="input-group-btn">
                  <button class="btn btn-sm send-btn" id="btn-chat" v-model="chatMessage.message" v-on:click="sendInRoom">
                    Send</button>
                </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </b-tab>
      </template>

    </b-tabs>

  </div>
</template>

<script>
  import '../flask-socketio.js'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Chat',
    props: ['projectId', 'openChatRooms', 'chatArray', 'newDirectChat'],
    data() {
      return {
        roomNumber: this.projectId.toString(),
        socket: io.connect(API_URL),
        chatMessage: {
          message: "",
          who: ""
        },
        chatRoomNumber: this.projectId.toString(),
        activeChats: [this.projectId.toString()]
      }
    },
    computed: {
      ...mapGetters({
        user: 'user'
      })
    },
    watch: {
      newDirectChat: function(member) {
        // Watch if prop newDirectChat changes, if it does a name has been clicked in parent component
        // and we add to activeChats. If parameter member is empty a window has been closed.
        if (member) {
          let usersInDirectChat = [this.user.username, member];
          usersInDirectChat.sort();
          const directChatRoom = this.roomNumber + '.' + usersInDirectChat[0] + usersInDirectChat[1];
          this.socket.emit('join', {who: this.user.username, room: directChatRoom, direct_chat: true});
          if (this.activeChats.indexOf(directChatRoom) === -1) {
            this.activeChats.push(directChatRoom)
          }
        }
      }
    },
    methods: {
      sendInRoom: function () {
        this.chatMessage.who = this.user.username;
        this.socket.emit('sendInRoom', {data: this.chatMessage, room: this.chatRoomNumber});
        this.chatMessage.message = '';
      },
      sendInRoomResponse: function() {
        // Receiving messages and pushing the messages to the history array, handles the scrollbar
        // depending on who sent the message and the look of the current scroll
        this.socket.on('room_response', function(response) {
          let element = document.getElementById('chat-window');
          const scroll = element.scrollHeight - element.scrollTop;
          if (response.data.who === this.user.username){
            let index = this.activeChats.indexOf(response.room);
            this.chatArray[index].history.push({ who: 'me', message: response.data.message});
            setTimeout( () => {
              element = document.getElementById('chat-window');
              element.scrollTop = element.scrollHeight
            }, 100)
          } else {
            let index = this.activeChats.indexOf(response.room);
            this.chatArray[index].history.push(
                { who: 'you', message: response.data.who + ": " + response.data.message});
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
        this.socket.emit('join', {who: this.user.username, room: this.chatRoomNumber, direct_chat: false})
      },
      joinRoomResponse: function() {
        this.socket.on('join_room_response', function(response) {

          this.$emit('activeUpdate', response.active_users);
        }.bind(this));
      },
      leaveRoom: function() {
        this.socket.emit('leave',
          {who: this.user.username, room: this.roomNumber, direct_chat: false});
      },
      leaveRoomResponse: function() {
        this.socket.on('leave_room_response', function(response) {

          this.$emit('activeUpdate', response.active_users);
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
          //console.log(Math.round(10 * sum / ping_pong_times.length) / 10);
        }.bind(this));
      },
      newMemberJoin: function () {
        this.socket.on('member_join_response', function(response) {

          this.$emit('memberJoin', response.data);
        }.bind(this));
      },
      leaveDirectChatRoom() {
        this.socket.emit('leave',
          {who: this.user.username, room: this.chatRoomNumber, direct_chat: true});
      },
      openRoom(member){
        // When tab is clicked set the chatRoomNumber to the correct value so that messages
        // can be sent in the right room
        if (member === 'room') {
          this.chatRoomNumber = this.roomNumber;
        } else {
          let usersInDirectChat = [this.user.username, member];
          usersInDirectChat.sort();
          this.chatRoomNumber = this.roomNumber + '.' + usersInDirectChat[0] + usersInDirectChat[1];
        }
      },
      closeRoom(member){
        let usersInDirectChat = [this.user.username, member];
        usersInDirectChat.sort();
        this.chatRoomNumber = this.roomNumber + '.' + usersInDirectChat[0] + usersInDirectChat[1];
        let index = this.activeChats.indexOf(this.chatRoomNumber);
        this.activeChats.splice(index, 1);
        this.leaveDirectChatRoom();
        this.$emit('closeRoom', member)
      },
      closeChatHandler() {
        this.leaveRoom();
        return null
      }
    },
    created () {
      window.addEventListener('beforeunload', this.closeChatHandler);

      this.joinRoom();
      this.sendInRoomResponse();
      this.joinRoomResponse();
      this.leaveRoomResponse();
      this.pingUser();
      this.pongUser();
      this.newMemberJoin();
    },
    beforeDestroy() {
      // Make sure to leave the room on server by calling leaveRoom and remove event listener
      this.leaveRoom();
      window.removeEventListener('beforeunload', this.closeChatHandler);
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
