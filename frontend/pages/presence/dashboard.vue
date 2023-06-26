<template>
  <v-container fluid>
      <v-img
          cover
          src="/images/roseguarden_spaces.png">
        </v-img>
    <v-card height="100%">
      <v-card-title>
        <h3>
          #Rosenwerk Anwesenheit
        </h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-simple-table height="300px">
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left presence_table_header_spaces" >
            Name
          </th>
          <th v-for="d in days" :key="d.date" 
                class="text-center presence_table_header_dates">
                  {{ d.date }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in desserts"
          :key="item.name"
        >
          <th class="text-left presence_table_header_spaces" >{{ item.name }}</th>
          <td>

            <v-btn
              fab
              small
              max-width="30px"
              min-width="30px"
              max-height="30px"
              min-height="30px"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              color="red"
              style="margin-right:-25px;border: 1px solid black !important;">
              MM
            </v-btn>
            <v-btn
              fab
              small
              max-width="30px"
              min-width="30px"
              max-height="30px"
              min-height="30px"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              color="red lighten-3"
              style="margin-right:-25px;border: 1px solid black !important;">
              MM
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              fab
              small
              max-width="30px"
              min-width="30px"
              max-height="30px"
              min-height="30px"
              elevation="0"
              v-bind="attrs"
              v-on="on"
              color="red"
              style="margin-right:-25px;border: 1px solid black !important;">
              MM
            </v-btn>

          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
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
    consumptionsActions : [],
    days: [
      
    ],
    desserts: [
      {
        name: 'Nähwerk',
        calories: 159,
      },
      {
        name: 'Elektronik',
        calories: 237,
      },
      {
        name: 'Laser',
        calories: 262,
      },
      {
        name: 'Büro',
        calories: 305,
      },
      {
        name: 'Holz',
        calories: 356,
      },
      {
        name: 'CNC',
        calories: 237,
      },
      {
        name: 'Eclair',
        calories: 262,
      },
      {
        name: 'Cupcake',
        calories: 305,
      },
      {
        name: 'Plastik',
        calories: 356,
      },
      {
        name: 'Siebdruck',
        calories: 356,
      }      
    ],

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

      // start date
      const startDate = new Date();

      // end date
      const endDate =  new Date()
      endDate.setDate(startDate.getDate() + 14);

      console.log("++++", startDate, endDate)
      // loop from start date to end date
      for (
            let date = startDate; 
            date <= endDate; 
            date.setDate(date.getDate() + 1)
          ) 
      {
        console.log("++++", new Date(date))
        this.days.push({date: new Date(date).toISOString().split('T')[0]});
      }
      console.log("+++++++++++", this.days)
  },
};
</script>

<style scoped>

.presence_table_header_spaces {
  min-width:  unset;
}

.presence_table_header_dates {
  min-width: 250px !important;
}


table {
  white-space: nowrap;
  margin: 0;
  border: none;
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed;
}
table td,
table th {
  padding: 0.5rem 1rem;
}
table thead th {
  padding: 3px;
  position: sticky;
  top: 0;
  z-index: 1;
  width: 25vw;
  background: white;
}
table td {
  background: #fff;
  padding: 4px 5px;
  text-align: center;
}

table tbody th {
  text-align: left;
  position: relative;
}
table thead th:first-child {
  position: sticky;
  left: 0;
  z-index: 2;
}
table tbody th {
  position: sticky;
  left: 0;
  background: white;
  z-index: 1;
}

</style>
