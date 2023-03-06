<template>
  <v-container fluid>
    <v-card >
      <v-card-title>
        <h3>Consumptions</h3>
      </v-card-title>
      <v-card-text dense>
        <v-progress-linear
          indeterminate
          color="primary"
          v-if="isUserDataLoading"
        ></v-progress-linear>
        <div v-else>
          <pre>{{userHeaders | prettyJson}}</pre>
          <br/>
          <pre>{{userData | prettyJson}}</pre>
          <br/>
          <pre>{{userActions | prettyJson}}</pre>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios);

import { createHelpers } from 'vuex-map-fields';
import { mapState } from 'vuex';

// The getter and mutation types are provided to the vue module
// they must be the same as the function names used in the store.
const { mapFields } = createHelpers({
  getterType: 'views/getView',
  mutationType: 'views/updateView',
});

import * as actionBuilder from '@/api/actionBuilder';
import * as viewParser from '@/api/viewParser'; 

export default {
  layout: "dashboard",
  components: {},
  data: () => ({
    info: "",
    isUserDataLoading: true,
    userData : [],
    userHeaders : [],
    userActions : []
  }),
  methods: {
    ok() {},
  },
  watch: {
    viewStates(newValue) {
      // check for view is loading
      if(newValue['invoices/consumedList'] === 'loading')  {
        this.isUserDataLoading = true;
      }
      // updates local data for state change
      if(newValue['invoices/consumedList'] === 'ready')  {
        this.userData = viewParser.parseEntries('invoices/consumedList', this.viewDictionary);
        this.userHeaders = viewParser.parseHeader('invoices/consumedList', this.viewDictionary);
        this.userActions = viewParser.parseActions('invoices/consumedList', this.viewDictionary);
        this.isUserDataLoading = false;
      } 
    }
  },
  filters: {
    prettyJson: function(value) {
      return (JSON.stringify(value, null, 3).trim());
    }
  },  
  computed: {
      ...mapState('views', ['viewDictionary']),
      ...mapState('views', ['viewStates']),
  },
  created() {},
  mounted() {
      // request the view by workspace uri `invoices` and view uri `consumedList`
      let getViewAction = [actionBuilder.newGetViewAction("invoices", "consumedList")];
      this.$store.dispatch('actions/emitActionRequest', getViewAction);          
  },
};
</script>

<style scoped></style>
