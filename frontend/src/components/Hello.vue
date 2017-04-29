<template>
  <div class="hello">
    <h2>{{ msg }}</h2>
    <button v-on:click="getServerData">Skicka</button>
  </div>
</template>

<script>
  import axios from 'axios'
  import auth from '../auth'

export default {
  name: 'hello',
  data () {
    return {
      msg: []
    }
  },
  methods: {
    getServerData () {
        axios.get('http://localhost:5000/test_token', auth.getAuthHeader())
          .then( response => {this.msg = response.data})
    }
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
