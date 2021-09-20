<template>
  <v-container grid-list-xl fluid>
    <v-flex lg12 sm12 xs12>
      <v-card>
        <v-card-title>
          <h3 style="margin-right: 40px">
            User authenticators (card, tag, device)
          </h3>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="userSearch"
            append-icon="search"
            label="Search"
            single-line
            style="padding-left: 15px; padding-right: 15px"
            hide-details
          ></v-text-field>
        </v-card-title>

        <!--- 
          offset-xs6 
        -->
        <v-flex
          v-if="searchEnable"
          lg4
          sm6
          xs10
          offset-lg0
          offset-sm6
          offset-xs1
        >
        </v-flex>
        <v-data-table
          :headers="userAuthenticatorHeaders"
          :items="userAuthenticators"
          :search="userSearch"
        >
          <template v-slot:item.actions="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-btn
                  color="success"
                  :disabled="item.auth_status !== 'Unset'"
                  v-on="on"
                  @click="clickAssignAuthenticator(item)"
                  fab
                  x-small
                >
                  <v-icon>credit_card</v-icon>
                </v-btn>
              </template>
              <span>Assign authenticator</span>
            </v-tooltip>
            <v-tooltip
              bottom
              v-for="action in userAuthenticatorActions"
              v-bind:key="action.name"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  v-if="item.hasOwnProperty(action.name)"
                  :color="action.color"
                  v-on="on"
                  @click="
                    requestViewAction(
                      'users',
                      'userAuthenticatorList',
                      action.action,
                      item
                    )
                  "
                  :disabled="!item[action.name]"
                  fab
                  x-small
                  :dark="item[action.name]"
                >
                  <v-icon>{{ action.icon }}</v-icon>
                </v-btn>
              </template>
              <span>{{ action.tooltip }}</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-card>
      <br />
      <v-card>
        <v-card-title>
          <h3 style="margin-right: 40px">Authenticator assign requests</h3>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="authenticatorSearch"
            append-icon="search"
            label="Search"
            single-line
            style="padding-left: 15px; padding-right: 15px"
            hide-details
          ></v-text-field>
        </v-card-title>

        <!--- 
          offset-xs6 
        -->
        <v-flex
          v-if="searchEnable"
          lg4
          sm6
          xs10
          offset-lg0
          offset-sm6
          offset-xs1
        >
        </v-flex>
        <v-data-table
          :headers="authenticatorHeaders"
          :items="authenticators"
          :search="authenticatorSearch"
        ></v-data-table>
      </v-card>
    </v-flex>
    <AssignAuthenticatorDialog
      :userId="selectedUserId"
      :show.sync="showAssignAuthenticatorDialog"
    />
  </v-container>
</template>

<script>
import * as actionBuilder from "@/api/actionBuilder";
import * as viewParser from "@/api/viewParser";

import { createHelpers } from "vuex-map-fields";
import { mapState } from "vuex";

import AssignAuthenticatorDialog from "~/components/dialogs/assignAuthenticatorDialog";

// The getter and mutation types are provided to the vue module
// they must be the same as the function names used in the store.
const { mapFields } = createHelpers({
  getterType: "views/getView",
  mutationType: "views/updateView",
});

export default {
  layout: "dashboard",
  components: {
    AssignAuthenticatorDialog,
  },
  data: () => ({
    search: "",
    searchEnable: true,
    authenticators: [],
    authenticatorHeaders: [],
    authenticatorActions: [],
    authenticatorSearch: "",
    userAuthenticators: [],
    userAuthenticatorHeaders: [],
    userAuthenticatorActions: [],
    userSearch: "",
    selectedUserId: null,
    showAssignAuthenticatorDialog: false,
  }),
  methods: {
    clickAssignAuthenticator(item) {
      this.selectedUserId = item.email;
      this.showAssignAuthenticatorDialog = true;
    },
    requestViewAction(workspace, view, action, item) {
      let r = actionBuilder.requestViewAction(
        workspace,
        view,
        action,
        item,
        this.userAuthenticatorActions
      );
      this.$store.dispatch("actions/emitActionRequest", r);
    },
  },
  computed: {
    ...mapState("views", ["viewDictionary"]),
    ...mapState("views", ["viewStates"]),
  },
  watch: {
    viewStates(newValue, oldValue) {
      //console.log("change on viewStates detected with", newValue, oldValue);
      if (newValue["users/authenticatorList"] === "ready") {
        this.authenticators = viewParser.parseEntries(
          "users/authenticatorList",
          this.viewDictionary
        );
        this.authenticatorHeaders = viewParser.parseHeader(
          "users/authenticatorList",
          this.viewDictionary
        );
        this.authenticatorActions = viewParser.parseActions(
          "users/authenticatorList",
          this.viewDictionary
        );
      }
      if (newValue["users/userAuthenticatorList"] === "ready") {
        this.userAuthenticators = viewParser.parseEntries(
          "users/userAuthenticatorList",
          this.viewDictionary
        );
        this.userAuthenticatorHeaders = viewParser.parseHeader(
          "users/userAuthenticatorList",
          this.viewDictionary
        );
        this.userAuthenticatorActions = viewParser.parseActions(
          "users/userAuthenticatorList",
          this.viewDictionary
        );
      }
    },
  },
  mounted() {
    let getViewAction = [
      actionBuilder.newGetViewAction("users", "authenticatorList"),
      actionBuilder.newGetViewAction("users", "userAuthenticatorList"),
    ];
    this.$store.dispatch("actions/emitActionRequest", getViewAction);
  },
};
</script>

<style scoped>
.zindex-repair {
  z-index: 1;
}
</style>
