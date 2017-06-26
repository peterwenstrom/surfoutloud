<template>
  <div class="col-md-5 border-right">
    <h3>Chat</h3>
      <b-tabs :value="tabValue" >
        <b-tab title="room">
          <room v-bind:username="username" v-bind:socket="socket"
                v-bind:roomNumber="roomNumber" member="room"></room>
        </b-tab>
        <template v-for="member in privateRooms">
          <b-tab :headHtml="showRoom(member)" :title="member">

            <div class="icon-container" v-on:click="hideRoom(member)">
              <icon name="window-close-o" class="hej"></icon>
            </div>

            <room v-bind:username="username" v-bind:socket="socket"
                  v-bind:roomNumber="roomNumber" v-bind:member="member"></room>

          </b-tab>
        </template>

      </b-tabs>
  </div>

</template>

<script>
  import Room from './Room.vue'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/window-close-o'

  export default {
    name: 'chat',
    props: ['user', 'projectId', 'members', 'openRooms'],
    data() {
      return {
        tabValue: 1,
        username: this.user.username,
        roomNumber: this.projectId.toString(),
        socket: io.connect(API_URL)
      }
    },
    computed: {
      privateRooms () {
        let rooms = [];
        this.members.forEach(member => {
          if (member !== this.username) {
            rooms.push(member)
          }
        });
        return rooms;
      }
    },
    components: {
      Room,
      Icon
    },
    methods: {
      showRoom (member) {
        if (this.openRooms.indexOf(member) > -1) {
          // Show room
          return '';
        } else {
          // Do not show room
          return ' ';
        }
      },
      hideRoom (member) {
        this.$emit('closeRoom', member);
        if (this.tabValue === 0) {
          this.tabValue = -1;
          setTimeout(() => {
            this.tabValue = 0;
          }, 10);
        } else {
          this.tabValue = 0;

        }
      },
      joinRoomResponse () {
        this.socket.on('join_room_response', response => {

          this.$emit('activeUpdate', response.active_users);
        });
      },
      leaveRoom () {
        this.socket.emit('leave_room', {user: this.username, room: this.roomNumber});
      },
      leaveRoomResponse () {
        this.socket.on('leave_room_response', response => {

          this.$emit('activeUpdate', response.active_users);
        });
      },
      newMemberJoin () {
        this.socket.on('member_join_response', response => {

          this.$emit('memberJoin', response.data);
        });
      },
      closeChatHandler() {
        this.leaveRoom();
        return null
      }
    },
    created () {
      window.addEventListener('beforeunload', this.closeChatHandler);

      this.joinRoomResponse();
      this.leaveRoomResponse();
      this.newMemberJoin();
    },
    beforeDestroy () {
      this.leaveRoom();
      window.removeEventListener('beforeunload', this.closeChatHandler);
    }
  }
</script>


<style scoped>
  .border-right {
    border-right: 1px solid #eceeef;
  }
  .icon-container {
    position: absolute;
    z-index: 1000;
    cursor: pointer;
    margin: 0 5px 0 5px;
  }
  .icon-container svg {
    margin: auto;
    vertical-align: middle;
  }
  .icon-container svg:hover {
    color: #f66;
  }
</style>
