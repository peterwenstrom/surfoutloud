<template>
  <div class="col-md-2 border-right">
    <h3>Members</h3>
    <hr class="small">
    <p><small><i>Click on a person to start a private conversation</i></small></p>
    <table class="table table-striped">
      <tbody>
      <tr v-for="(member,index) in members">
        <td>
          <p v-if="member !== username" v-on:click="memberClick(member)" class="point">{{ member }}</p>
          <p v-else>{{ member }}</p>
        </td>
        <td>
          <icon v-if="ifMemberIsActive(member)" class="green" name="user"></icon>
          <icon v-else name="user"></icon>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/user'

  export default {
    name: 'member',
    props: ['username', 'members', 'activeMembers'],
    data() {
      return {}
    },
    methods: {
      ifMemberIsActive (user) {
        return (this.activeMembers.indexOf(user) > -1)
      },
      memberClick(member) {
        this.$emit('memberClick', member)
      }
    },
    components: {
      Icon
    }
  }
</script>

<style scoped>
  td p {
    text-align: left;
  }
  td * {
    vertical-align: middle;
    margin-top: 0;
    margin-bottom: 0;
  }
  .green {
    color: #41B883;
  }
  .border-right {
    border-right: 1px solid #eceeef;
  }
  .point {
    cursor: pointer;
  }
</style>
