<template>
  <div class="row">
    <div class="col-md-12">
      <div class="panel panel-primary">

        <ul id="chat-window" class="panel-body chat">

          <li v-for="message in roomMessages">
            <span class="bubble bubble-alt yellow" v-if="message.user === username">
              <div class="chat-body clearfix">
                {{ message.text }}
              </div>
            </span>
            <span class="bubble" v-else>
              <div class="chat-body clearfix">
                {{message.user}}: {{ message.text }}
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
                   v-model="newMessage.text"
                   v-on:keyup.enter="messageRoom" />
            <span class="input-group-btn">
              <button class="btn btn-sm send-btn" id="btn-chat" v-on:click="messageRoom">
                Send
              </button>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'room',
    props: ['username', 'socket', 'roomNumber', 'member'],
    data () {
      return {
        newMessage: {user: '', text: ''},
        roomMessages: []
      }
    },
    computed: {
      room () {
        if (this.member) {
          let usersInDirectChat = [this.username, this.member];
          usersInDirectChat.sort();
          return this.roomNumber + usersInDirectChat[0] + usersInDirectChat[1];
        } else {
          return this.roomNumber;
        }
      }
    },
    methods: {
      joinRoom () {
        const isPrivateRoom = (!!this.member);
        this.socket.emit('join_room', {user: this.username, room: this.room, private_room: isPrivateRoom})
      },
      messageRoom () {
        this.newMessage.user = this.username;
        this.socket.emit('message_room', {data: this.newMessage, room: this.room});
        this.newMessage.text = '';
      },
      messageRoomResponse () {
        this.socket.on('message_room_response', response => {
          if (response.room === this.room) {
            this.roomMessages.push(response.data);
          }
        });
      }
    },
    created () {
      this.joinRoom();
      this.messageRoomResponse();
    }
  }

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
