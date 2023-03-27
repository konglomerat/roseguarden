<template>
  <div v-if="group != null">
    <v-row dense>
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Name:</v-subheader>
        <v-text-field
          label="Name"
          v-model="group.name"
          hide-details
          solo
          dense
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Note:</v-subheader>
        <v-text-field
          label="Note"
          v-model="group.note"
          hide-details
          solo
          dense
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Access type:</v-subheader>
        <v-select
          :items="accessTypeItems"
          v-model="group.type"
          label="Access type"
          dense
          solo
          hid-details
        ></v-select>
      </v-col>
    </v-row>

    <v-row dense v-if="userBudgetVisibility">
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Start budget</v-subheader>
        <v-text-field
          label="Users start budget"
          type="number"
          v-model="group.start_budget"
          hide-details
          solo
          dense
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row dense v-if="groupBudgetVisibility">
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Start budget:</v-subheader>
        <v-text-field
          label="Users start budget"
          type="number"
          v-model="group.start_budget"
          hide-details
          solo
          dense
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row dense v-if="groupBudgetVisibility">
      <v-col cols="1" />

      <v-col cols="10">
        <v-subheader>Actual shared group budget:</v-subheader>
        <v-text-field
          label="Group budget"
          type="number"
          v-model="group.group_budget"
          hide-details
          solo
          dense
        ></v-text-field>
      </v-col>
    </v-row>


    <v-row dense v-if="rechargeSectionsVisibility">
      <v-col cols="1" />

      <v-col cols="6">
        <v-subheader>Automatic budget recharge with:</v-subheader>
      </v-col>
    </v-row>

    <v-row dense wrap v-if="rechargeSectionsVisibility">
      <v-col cols="1" />

      <v-col cols="4">
        <v-text-field
          v-model="group.recharge_budget_amount"
          type="number"
          dense
          solo
          hid-details
          :suffix="group.entry_accounting"
          label="Number"
        ></v-text-field>
      </v-col>

      <v-col cols="1">
        <div class="text-center" style="margin-top: 10px; align: center">
          every
        </div>
      </v-col>

      <v-col cols="2">
        <v-text-field
          v-model="group.recharge_budget_every_periods"
          dense
          solo
          hid-details
          label="Number"
          reverse
        ></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-select
          :items="periodItems"
          v-model="group.recharge_budget_period"
          label="Access type"
          dense
          solo
          hid-details
        ></v-select>
      </v-col>
    </v-row>

    <v-row dense v-if="rechargeSectionsVisibility">
      <v-col cols="1" />
      <v-col cols="3" height="100%">
        <v-subheader>Limit recharge:</v-subheader>
        <v-switch
          v-model="group.recharge_budget_gets_cutoff"
          hide-details
          color="indigo"
          class="mx-2"
          style="margin-top: 0px; padding-left: 15%"
        ></v-switch>
      </v-col>
      <v-col cols="7" align-end justify-end height="100%">
        <v-subheader>To</v-subheader>
        <v-text-field
          v-model="group.recharge_budget_cutoff_max"
          type="number"
          suffix="days"
          :disabled="!group.recharge_budget_gets_cutoff"
          dense
          solo
          hid-details
          label="Number"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row dense wrap v-if="commonSectionsVisibility">
      <v-col cols="1" />
      <v-subheader>Access on following weekdays:</v-subheader>
    </v-row>
    <v-row
      v-if="commonSectionsVisibility"
      align="center"
      justify="center"
      dense
      wrap
    >
      <v-col cols="1" />
      <v-checkbox
        v-model="days[0]"
        label="Mon"
        color="indigo"
        hide-details
        class="mx-2"
      ></v-checkbox>
      <v-checkbox
        v-model="days[1]"
        class="mx-2"
        label="Tue"
        color="indigo"
        hide-details
      ></v-checkbox>
      <v-checkbox
        v-model="days[2]"
        class="mx-2"
        label="Wen"
        color="indigo"
        hide-details
        inset
      ></v-checkbox>
      <v-checkbox
        v-model="days[3]"
        class="mx-2"
        label="Thu"
        color="indigo"
        hide-details
        inset
      ></v-checkbox>
      <v-checkbox
        v-model="days[4]"
        class="mx-2"
        label="Fri"
        color="indigo"
        hide-details
        inset
      ></v-checkbox>
      <v-checkbox
        v-model="days[5]"
        label="Sat"
        color="indigo"
        hide-details
        class="mx-2"
        inset
      ></v-checkbox>
      <v-checkbox
        v-model="days[6]"
        label="Sun"
        color="indigo"
        hide-details
        class="mx-2"
      ></v-checkbox>
      <v-col cols="1" />
    </v-row>
    <br />

    <v-row v-if="commonSectionsVisibility" dense>
      <v-col cols="1" />
      <v-col cols="4">
        <v-subheader>Access from:</v-subheader>
        <v-menu
          ref="menu1"
          v-model="menu1"
          :close-on-content-click="false"
          :nudge-right="40"
          :return-value.sync="group.daily_start_time"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="group.daily_start_time"
              label="Daily start time"
              prepend-icon="access_time"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="menu1"
            v-model="group.daily_start_time"
            format="24hr"
            full-width
            @click:minute="$refs.menu1.save(group.daily_start_time)"
          ></v-time-picker>
        </v-menu>
      </v-col>
      <v-col cols="2">
        <v-subheader></v-subheader>
        <div class="text-center" style="margin-top: 20px; align: center">
          to
        </div>
      </v-col>
      <v-col cols="4">
        <v-subheader></v-subheader>
        <v-menu
          ref="menu2"
          v-model="menu2"
          :close-on-content-click="false"
          :nudge-right="40"
          :return-value.sync="group.daily_end_time"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="group.daily_end_time"
              label="Daily end time"
              prepend-icon="access_time"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="menu2"
            v-model="group.daily_end_time"
            format="24hr"
            full-width
            @click:minute="$refs.menu2.save(group.daily_end_time)"
          ></v-time-picker>
        </v-menu>
      </v-col>
    </v-row>

    <v-row dense v-if="commonSectionsVisibility">
      <v-col cols="1" />
      <v-col cols="3" height="100%">
        <v-subheader>Access expires: </v-subheader>
        <v-switch
          v-model="group.expires_as_default"
          hide-details
          color="indigo"
          class="mx-2"
          style="margin-top: 5px; padding-left: 15%"
        ></v-switch>
      </v-col>
      <v-col cols="2">
        <v-subheader></v-subheader>
        <div class="text-center" style="margin-top: 10px; align: center">
          after
        </div>
      </v-col>

      <v-col cols="5" align-end justify-end height="100%">
        <v-subheader></v-subheader>
        <v-text-field
          v-model="group.expires_after_days_default"
          type="number"
          suffix="days"
          :disabled="!group.expires_as_default"
          dense
          solo
          hid-details
          label="Number"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row dense v-if="commonSectionsVisibility">
      <v-col cols="1" />
      <v-col cols="10">
        <v-subheader>Access to following spaces</v-subheader>
        <v-card class="mx-auto" tile dense>
          <v-list shaped>
            <v-list-item-group v-model="group.spaces" multiple>
              <v-list-item
                v-for="(item, i) in spaces"
                :key="i"
                :value="item.id"
                active-class="blue--text text--accent-4"
              >
                <template v-slot:default="{ active, toggle }">
                  <v-list-item-content>
                    <v-list-item-title v-text="item.name" />
                    <v-list-item-subtitle v-text="item.description" />
                  </v-list-item-content>

                  <v-list-item-action>
                    <v-icon>{{
                      active ? "check_box" : "check_box_outline_blank"
                    }}</v-icon>
                  </v-list-item-action>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col cols="11" class="text-right">
        <v-spacer></v-spacer>
        <v-btn color="warning" v-on:click="onCancel">Cancel</v-btn>
        <v-btn color="success" v-on:click="onSubmit">Submit</v-btn>
      </v-col>
    </v-row>
    <br />
  </div>
</template>

<script>
export default {
  props: {
    group: {
      required: true,
      default: function () {
        return {};
      },
    },
    groupProps: {
      required: true,
      default: function () {
        return {};
      },
    },
    spaces: {
      required: true,
      default: function () {
        return {};
      },
    },
  },
  data: () => ({
    state: true,
    menu2: false,
    modal2: false,
    time: null,
    menu1: false,
    modal1: false,
    time1: null,
    doors: Array(8).fill(false),
    days: Array(7).fill(false),
  }),
  computed: {
    accessTypeItems: function () {
      if (this.groupProps.hasOwnProperty("type")) {
        return this.groupProps.type.selection;
      } else {
        return [];
      }
    },
    periodItems: function () {
      if (this.groupProps.hasOwnProperty("recharge_budget_period")) {
        return this.groupProps.recharge_budget_period.selection;
      } else {
        return [];
      }
    },
    commonSectionsVisibility: function () {
      if (this.group) {
        if (this.group.type === "No access") {
          return false;
        } else {
          return true;
        }
      } else {
        return true;
      }
    },
    rechargeSectionsVisibility: function () {
      if (this.group) {
        if (
          this.group.type === "Auto-recharged user budget" ||
          this.group.type === "Auto-recharged group budget"
        ) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
    groupBudgetVisibility: function () {
      if (this.group) {
        if (
          this.group.type === "Group Budget" ||
          this.group.type === "Auto-recharged group budget"
        ) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
    userBudgetVisibility: function () {
      if (this.group) {
        if (
          this.group.type === "User Budget" ||
          this.group.type === "Auto-recharged user budget"
        ) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },    
  },
  watch: {
    open: function (newVal, oldVal) {
      console.log("open");
    },
    group(newValue, oldValue) {
      console.log("group changed", newValue);

      if (!newValue) {
        this.doors = Array(8).fill(false);
        this.days = Array(8).fill(false);
        return;
      }

      if (newValue.hasOwnProperty("doors_mask")) {
        for (var i = 0; i < this.doors.length; i++) {
          if (((1 << i) & newValue.doors_mask) !== 0) {
            this.doors[i] = true;
          } else {
            this.doors[i] = false;
          }
        }
      } else {
        this.doors = Array(8).fill(false);
      }

      if (newValue.hasOwnProperty("days_mask")) {
        for (var i = 0; i < this.days.length; i++) {
          if (((1 << i) & newValue.days_mask) !== 0) {
            this.days[i] = true;
          } else {
            this.days[i] = false;
          }
        }
      } else {
        this.days = Array(8).fill(false);
      }
    },
  },
  methods: {
    onSubmit() {
      this.group.doors_mask = 0;
      for (var i = 0; i < this.doors.length; i++) {
        if (this.doors[i] === true) {
          this.group.doors_mask |= 1 << i;
        }
      }
      this.group.days_mask = 0;
      for (var i = 0; i < this.days.length; i++) {
        if (this.days[i] === true) {
          this.group.days_mask |= 1 << i;
        }
      }

      this.$emit("submit");
    },
    onCancel() {
      this.$emit("cancel");
    },
    mounted() {},
  },
};
</script>
