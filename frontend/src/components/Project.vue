<template>
  <div class="hello row">
    <div class="col-md-4">


      <h2>Members</h2>

      <div v-for="(item, index) in memberList">

        {{ item }}
          <span v-if="activeUserList[index] === 'true'" class='circle green'></span>
        <span v-if="activeUserList[index] === 'false'" class='circle'></span>
      </div>

    </div>
    <div class="col-md-8">
      <h2>Chat</h2>
      <chat v-bind:projectId="projectId" @active="onActiveUserUpdate"></chat>


    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import chat from './Chat'
  const GETMEMBERS_URL = API_URL + 'getmembers';

  export default {
    name: 'project',
    data () {
      return {
        memberList: [

        ],
        activeUserList: [

        ],
        isActive: false,
        projectId: ""
      }
    },
    methods: {
      onActiveUserUpdate (value) {
        let i = 0;

        for (i; i<this.memberList.length; i++){

          if (value.indexOf(this.memberList[i]) > -1 ){
            this.activeUserList.splice(i, 1, 'true');

          }else{
            this.activeUserList.splice(i, 1, 'false');
          }
        }

      }
    },
    components:{
      'chat':chat
    },
    created() {
      this.projectId = this.$route.query.attr;
    },
    mounted(){

      let projIdArray = {
        projectId: this.projectId
      };

      axios.post(GETMEMBERS_URL,
        projIdArray

      ).then( response => {
        let i = 0;

        for (i; i<response.data.members.length; i++){
            //the drawback here is that you cannot have usernames with space in it.. maybe we do not want it anyway
          Vue.set(this.memberList, i, JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''));
        }
      });
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
  .circle:before {
    content: ' \25CF';
    font-size: 20px;
    color: black;
  }

  .green:before {
    color: lawngreen;
  }

</style>
