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
          v-for="space in spaces"
          :key="space.name"
        >
          <th class="text-left flex presence_table_header_spaces" >
            <span>
              {{ space.name }}

            </span>
            <span>
              <v-row  style="min-height: 50px;" v-for="slot in space.slots" :key="slot.name" no-gutters align="center" justify="center">
                {{ slot.name }}
              </v-row>
            </span>

          </th>
          <td v-for="(booking, bookingindex) in space.bookings" :key="bookingindex">
            <br/>
            <div  v-for="(bookingslot, bookingslotindex) in booking" :key="bookingslotindex">       
                <v-row style="min-height: 50px;" no-gutters align="center">

                    <v-col cols="1"/>

                    <v-col cols="6">
                      <v-btn
                        v-for="(person, personindex) in bookingslot.persons" :key="personindex"    
                        fab
                        small
                        max-width="30px"
                        min-width="30px"
                        max-height="30px"
                        min-height="30px"
                        elevation="0"
                        :color="person.color + ' lighten-3'"
                        style="margin-right:-25px;border: 1px solid black !important;">
                        {{ person.initials }}
                      </v-btn>
                      <span style="margin-right: 25px;"></span>
                  </v-col>

                  <v-col cols="4">

                    <v-btn
                      v-if="!(bookingslot.isFull)"
                      fab
                      small
                      max-width="30px"
                      min-width="30px"
                      max-height="30px"
                      min-height="30px"
                      color="success">
                      <v-icon small>
                        mdi-plus
                      </v-icon>
                    </v-btn>
                  </v-col>
                  <v-col cols="1"/>

                </v-row>
            </div>

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
    spaces: [
    {
        name: 'Büro',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : [
                {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "TT",
                  color: "blue"
                }
              ]
            },
            {
              persons : []
            }
          ],
          [
            {
              persons : [
                {
                  initials: "MD",
                  color: "red"
                },

              ]
            },
            {
              persons : []
            }
          ],
          [
            {
              persons : []
            },
            {
              persons : [
                {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "SK",
                  color: "yellow"
                },
                {
                  initials: "MZ",
                  color: "orange"
                }
              ]
            }
          ],
          [
            {
              persons : [
                {
                  initials: "AB",
                  color: "green"
                }                
              ]
            },
            {
              isFull: true,
              persons : [
                {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "SK",
                  color: "yellow"
                },
                {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "SK",
                  color: "yellow"
                },
                {
                  initials: "AB",
                  color: "green"
                }
              ]
            }
          ],
          [
            {
              persons : [
              ]
            },
            {
              persons : [
              {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "TT",
                  color: "blue"
                }                
              ]
            }
          ],
          [
            {
              persons : [
                {
                  initials: "TT",
                  color: "blue"
                }                     

              ]
            },
            {
              persons : [
              {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "ZT",
                  color: "grey"
                }                
              ]
            }
          ]
        ]
      },
      {
        name: 'Nähwerk',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : [
                {
                  initials: "MD",
                  color: "red"
                },
                {
                  initials: "BU",
                  color: "yellow"
                },                
              ]
            }
          ],
          [
            {
              persons : [
               {
                  initials: "LO",
                  color: "blue"
                },                   
              ]
            },
            {
              persons : [
                {
                  initials: "SZ",
                  color: "red"
                },
                {
                  initials: "LO",
                  color: "blue"
                },                
              ]
            }
          ],
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ],
          [
            {
              persons : []
            },
            {
              persons : [
                {
                  initials: "SZ",
                  color: "green"
                },                
              ]
            }
          ],
          [
            {
              persons : [
                {
                  initials: "LU",
                  color: "red"
                },                   
              ]
            },
            {
              persons : [
                {
                  initials: "LU",
                  color: "red"
                },                   

              ]
            }
          ],
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]

        ]        
      },
      {
        name: 'Elektronik',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
      },
      {
        name: 'Laser',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
      },
      {
        name: 'Holz',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
      },
      {
        name: 'CNC',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
      },
      {
        name: 'Plastik',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
      },
      {
        name: 'Siebdruck',
        slots: [
          { 
            name: "Vormittag"
          },
          { 
            name: "Nachmittag"
          }          
        ],
        bookings: [
          [
            {
              persons : []
            },
            {
              persons : []
            }
          ]
        ]
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
  min-width: 160px !important;
}

.presence_table_header_dates {
  min-width: 160px !important;
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
