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
    <div class="col-md-8">
      <h2>Chat</h2>
      <chat v-bind:projectId="projectId"></chat>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import chat from './Chat'

export default {
  name: 'project',
  data () {
    return {
        memberList: [
            '-'
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
