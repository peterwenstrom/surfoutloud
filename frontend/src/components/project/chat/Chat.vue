<template>
  <div class="col-md-5 border-right">
    <h3>Chat</h3>
      <b-tabs>
        <b-tab title="room">
          <room v-bind:username="username" v-bind:socket="socket"
                v-bind:roomNumber="roomNumber" member="room"></room>
        </b-tab>
        <template v-for="member in privateRooms">
          <b-tab :headHtml="showRoom(member)" :title="member">
              <room v-bind:username="username" v-bind:socket="socket"
                    v-bind:roomNumber="roomNumber" v-bind:member="member"></room>
          </b-tab>
        </template>

      </b-tabs>
  </div>

</template>

<script>
  import Room from './Room.vue'

  export default {
    name: 'chat',
    props: ['user', 'projectId', 'members', 'openRooms'],
    data() {
      return {
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
      Room
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
</style>
