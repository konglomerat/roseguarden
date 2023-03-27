<template>
  <v-container fluid>
    <v-card >
      <v-card-title>
        <h3>
          Consumptions
        </h3>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="consumptionsHeaders"
        :items="consumptionsData"
        :items-per-page="15"
        :loading="viewStates['invoices/consumedList'] !== 'ready'"
        :search="search"
        class="elevation-1"        
      >
        <template v-slot:item.actions="{ item }">
          <v-tooltip bottom v-for="action in actions" v-bind:key="action.name">
            <template v-slot:activator="{ on }">
              <v-btn  v-if="item.hasOwnProperty(action.name)" :color="action.color" v-on="on" @click="requestViewAction('users', 'userList', action.action, item)" :disabled="!item[action.name]" fab x-small :dark="item[action.name]">
                  <v-icon>{{action.icon}}</v-icon>
              </v-btn>
            </template>
            <span>{{action.tooltip}}</span>
          </v-tooltip>            
        </template>
      </v-data-table>

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
    search: '',    
    isConsumptionsDataLoading: true,
    consumptionsData : [],
    consumptionsHeaders : [],
    consumptionsActions : []
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
        this.consumptionsData = viewParser.parseEntries('invoices/consumedList', this.viewDictionary);
        this.consumptionsHeaders = viewParser.parseHeader('invoices/consumedList', this.viewDictionary);
        this.consumptionsActions = viewParser.parseActions('invoices/consumedList', this.viewDictionary);
        this.isConsumptionsDataLoading = false;
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
