<template>
  <div class="hello row">
    <div class="col-md-4">
      <h2>Members</h2>
      <ul>
        <li v-for="item in memberList">
          {{ item }}
        </li>
      </ul>
    </div>
    <div class="col-md-4">
      <h2>Chat</h2>
      <chat></chat>
    </div>
    <div class="col-md-4">
      <router-link to="/CreateNewProject">
        <h2>Create new project</h2>
        <h6>TODO: Move to dashboard when it has been dynamic</h6>

      </router-link>

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import auth from '../auth'
  import chat from './Chat'

export default {
  name: 'project',
  data () {
    return {
        memberList: [
            '-'
        ]
    }
  },
  methods: {

  },
  components:{
    'chat':chat
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
