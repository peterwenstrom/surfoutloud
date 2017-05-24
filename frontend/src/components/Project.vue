<template>
  <div class="hello row">
    <div class="col-md-4">
      <h2>Members</h2>

      <div v-for="item in memberList">
        {{ item }}
        <span v-show="item.active === 'true'">
          <span class="circle green"></span>
        </span>
        <span v-show="item.active === 'false'">
          <span class="circle"></span>
        </span>

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
  const API_URL = 'http://localhost:5000/';
  const GETMEMBERS_URL = API_URL + 'getmembers';

  export default {
    name: 'project',
    data () {
      return {
        memberList: [
          { member: "", active: ""}

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

        console.log("value: ");
        console.log(value);
        console.log("memberList: ");
        console.log(this.memberList);

        console.log("hallladjfasdjfhl: ");

        let self = this;

        let objArray = [];
        self.memberList.filter(function( obj ) {
            console.log(obj.member);
            objArray.push(obj.member);
        });
        console.log("objArray: ");
        console.log(objArray);
        for (i; i<objArray.length; i++){


            let index = self.indexWhere(self.memberList, item => item.member === value[i]);

            console.log("index: " + index);



            console.log(value[i]);
            console.log(objArray[i]);
            if(JSON.stringify(objArray[i]).toLowerCase() === JSON.stringify(value[i])){
              console.log("ja");
              self.memberList.splice(index, 1, {member: objArray[i], active: "true"});
            } else {
              console.log("nej");
              self.memberList.splice(index, 1, {member: objArray[i], active: "false"});
            }


        }

      },
      indexWhere: function (array, conditionFn) {
        const item = array.find(conditionFn);
        return array.indexOf(item);
      },
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
        console.log("arrayMEMBERS: ");
        console.log(response.data);
        for (i; i<response.data.members.length; i++){

          Vue.set(this.memberList, i, {member: JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''), active: "false"});

          //this.memberList.push({member: JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''), active: "false"});
          //this.memberList.splice(i, 1, {member: JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''), active: "false"});
        }

        console.log("memberlist: ");
        console.log(this.memberList);
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
  .circle:before {
    content: ' \25CF';
    font-size: 20px;
    color: black;
  }

  .green:before {
    color: lawngreen;
  }

</style>
