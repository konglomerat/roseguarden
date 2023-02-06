<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <h3>Deine Zugänge</h3>
        <v-spacer></v-spacer>
      </v-card-title>

      <v-row dense>
        <v-progress-linear
          indeterminate
          color="primary"
          v-if="loading"
        ></v-progress-linear>
      </v-row>
      <v-row dense>
        <v-col cols="2" />
        <v-col cols="8" align="center" justify="center">        
          <v-alert color="info"  dark shaped class="text-center" style="text-align: center; width: 100%;">
            <div style="font-weight: 700;">
            {{accountdata.access_budget_short}}
            </div>
          </v-alert>
        </v-col>
        <v-col cols="2" />
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Access info:</v-subheader>
          <v-text-field
            label="Access info"
            value="Max"
            v-model="accountdata.access_type_info"
            :loading="loading"
            hide-details
            readonly
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="3">
          <v-subheader>Access group:</v-subheader>
          <v-text-field
            label="Access group"
            v-model="accountdata.access_group"
            :loading="loading"
            hide-details
            readonly
            solo
            dense
          ></v-text-field>
        </v-col>
        <v-col cols="7">
          <v-subheader />
          <v-text-field
            label="Group desciption"
            v-model="accountdata.access_group_info"
            prepend-inner-icon="mdi-information-outline"
            :loading="loading"
            hide-details
            readonly
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="5">
          <v-subheader>Valid from:</v-subheader>
          <v-text-field
            name="pin"
            label="Valid from"
            id="pin"
            readonly
            hide-details
            solo
            dense
            v-model="accountdata.access_valid_start_date"
          >
          </v-text-field>
        </v-col>
        <v-col cols="5">
          <v-subheader>Expires at:</v-subheader>
          <v-text-field
            name="pin_verification"
            label="Expires at"
            id="pin_verification"
            readonly
            hide-details
            solo
            dense
            v-model="accountdata.access_valid_end_date"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>On following weekdays</v-subheader>
          <v-text-field
            label="Weekdays"
            v-model="accountdata.access_on_days"
            :loading="loading"
            readonly
            hide-details
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="5">
          <v-subheader>Opening at:</v-subheader>
          <v-text-field
            name="pin"
            label="Opening at"
            id="pin"
            readonly
            hide-details
            solo
            dense
            v-model="accountdata.access_valid_start_time"
          >
          </v-text-field>
        </v-col>
        <v-col cols="5">
          <v-subheader>Closing at:</v-subheader>
          <v-text-field
            name="pin_verification"
            label="Closing at"
            id="pin_verification"
            readonly
            hide-details
            solo
            dense
            v-model="accountdata.access_valid_end_time"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>To following spaces:</v-subheader>
          <v-text-field
            label="No spaces"
            v-model="accountdata.access_to_spaces"
            :loading="loading"
            hide-details
            readonly
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Last updated at:</v-subheader>
          <v-text-field
            label="Last updated"
            v-model="accountdata.access_updated_on_date"
            :loading="loading"
            hide-details
            readonly
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
    </v-card>
    <br />
  </v-container>
</template>

<script>
import Vue from "vue";
import * as actionBuilder from "@/api/actionBuilder";
import { createHelpers } from "vuex-map-fields";
import * as viewParser from "@/api/viewParser";
import { mapState } from "vuex";

// The getter and mutation types are provided to the vue module
// they must be the same as the function names used in the store.
const { mapFields } = createHelpers({
  getterType: "views/getView",
  mutationType: "views/updateView",
});

export default {
  layout: "dashboard",
  data() {
    return {
      showOld: false,
      showNew: false,
      showRepeat: false,
      loading: true,
      accountdata: {},
      valid_pin: true,
      valid_requestKey: true,
      pin_password: "",
      pin_verification: "",
      pin: "",
      valid_password: true,
      oldpassword: "",
      password: "",
      password_verification: "",
      cardStatus: "No card assigned",
      cardValid: true,
      cardRequestKey: "",
      rules: {
        required: (v) => !!v || "Is required",
        pin_digits: (v) => /([0-9]{6})/.test(v) || "Pin have to have 6 digits",
        pin_length: (v) => v.length == 6 || "Pin have to have 6 digits",
        requestKey_digits: (v) =>
          /([0-9A-Za-z]{12})/.test(v) ||
          "The request key have to have 12 characters",
        requestKey_length: (v) =>
          v.length == 12 || "The request key have to have 12 characters",
        pin: [
          (v) => /([0-9]{6})/.test(v) || "Pin have to have 6 digits",
          (v) => v.length == 6 || "Pin have to have 6 digits",
          (v) => !!v || "Pin is required",
        ],
        password: (v) =>
          /(.){7,}\w+/.test(v) || "Password have to have at least 8 characters",
        email: [
          (v) => !!v || "E-mail is required",
          (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
        ],
      },
    };
  },
  methods: {
    uppercase() {
      this.cardRequestKey = this.cardRequestKey.toUpperCase();
    },
    getAccountData(view) {
      if (this.viewDictionary.hasOwnProperty(view)) {
        return this.viewDictionary[view].entries[0];
      } else {
        return {};
      }
    },
    submitUnassignCard() {
      this.cardValid = false;
    },
    submitAssignCard() {
      this.cardValid = true;
    },
    cancelData() {
      this.accountdata = Object.assign({}, this.getAccountData("userInfo"));
      console.log("cancelData");
    },
    submitUserInfo() {
      let entry = {
        email: this.accountdata.email,
        firstname: this.accountdata.firstname,
        lastname: this.accountdata.lastname,
        organization: this.accountdata.organization,
        phone: this.accountdata.phone,
      };
      console.log("submitUserInfo", entry);
      let getViewAction = [
        actionBuilder.newUpdateDataViewEntryAction(
          "account",
          "userInfo",
          entry
        ),
      ];
      this.$store.dispatch("actions/emitActionRequest", getViewAction);
    },
    submitChangePin() {
      console.log("submitChangePin");
      let getViewAction = [
        actionBuilder.newChangePinAction(
          "account",
          this.pin_password,
          this.pin
        ),
      ];
      this.$store.dispatch("actions/emitActionRequest", getViewAction);
    },
    submitChangePassword() {
      console.log("submitChangePin");
      let getViewAction = [
        actionBuilder.newChangePasswordAction(
          "account",
          this.oldpassword,
          this.password
        ),
      ];
      this.$store.dispatch("actions/emitActionRequest", getViewAction);
    },
  },
  computed: {
    ...mapState("views", ["viewDictionary"]),
    ...mapState("views", ["viewStates"]),
    passwordVerificationRule() {
      return () =>
        this.password === this.password_verification ||
        this.password_verification === "" ||
        "Passwords must match";
    },
    pinVerificationRule() {
      return () =>
        this.pin === this.pin_verification ||
        this.pin_verification === "" ||
        "Pins must match";
    },
  },
  watch: {
    viewStates(newValue, oldValue) {
      console.log("change on viewStates detected with", newValue, oldValue);
      if (this.viewStates["access/userInfo"] === "ready") {
        let data = viewParser.parseEntries(
          "access/userInfo",
          this.viewDictionary
        );
        console.log(data);
        this.accountdata = Object.assign({}, data);
        this.loading = false;
      } else {
        this.loading = true;
      }
    },
  },
  mounted() {
    let getViewAction = [actionBuilder.newGetViewAction("access", "userInfo")];
    this.$store.dispatch("actions/emitActionRequest", getViewAction);
  },
};
</script>

<style scoped>
.gray >>> .v-input__control input {
  color: rgba(0, 0, 0, 0.38) !important;
}
</style>
