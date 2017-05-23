<template>
  <div class="hello row">
    <div class="col-md-4">
      <h2>Members</h2>

      <div v-for="item in memberList">
        {{ item[0] }}
        </div>



    </div>
    <div class="col-md-8">
      <h2>Chat</h2>
      <chat v-bind:projectId="projectId"></chat>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import chat from './Chat'
  const API_URL = 'http://localhost:5000/';
  const GETMEMBERS_URL = API_URL + 'getmembers';

  export default {
    name: 'project',
    data () {
      return {
        memberList: [

        ],
        projectId: ""
      }
    },
    methods: {

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
        this.memberList = response.data.members;
        console.log("member array: " + response.data.members);
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
</style>
