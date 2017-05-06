<template>
  <div class="hello row">
    <div class="col-md-4">
      <h2>Members</h2>
        <ul id="repeat-object" class="demo">
          <li v-for="value in object">
            {{ value }}
          </li>
        </ul>
    </div>
    <div class="col-md-4">
      <h2>Chat</h2>
      <chat></chat>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import auth from '../auth'
  import chat from './chat'

export default {
  name: 'project',
  data () {
    return {
      object: {
        firstName: 'John',
        lastName: 'Doe',
        age: 30
      }
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
