<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <h3>Deine Nutzer:innendaten</h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>E-Mail:</v-subheader>
          <v-text-field
            label="eMail"
            v-model="accountdata.email"
            :loading="loading"
            hide-details
            disabled
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Vorname:</v-subheader>
          <v-text-field
            label="Dein Vorname"
            value="Max"
            v-model="accountdata.firstname"
            :loading="loading"
            hide-details
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Nachname:</v-subheader>
          <v-text-field
            label="Dein Nachname"
            v-model="accountdata.lastname"
            :loading="loading"
            hide-details
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Gruppenzugehörigkeit (nur für Gruppenmitglieder relevant):</v-subheader>
          <v-text-field
            label="Deine Gruppe"
            v-model="accountdata.organization"
            :loading="loading"
            hide-details
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Telefonnummer (optional):</v-subheader>
          <v-text-field
            label="Telefonnummer"
            v-model="accountdata.phone"
            :loading="loading"
            hide-details
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
      <v-row justify="end">
        <v-col cols="2" class="text-right">
          <v-btn color="primary" @click="cancelData()">abbrechen</v-btn>
        </v-col>
        <v-col cols="2" class="text-right">
          <v-btn color="primary" @click="submitUserInfo()">Daten ändern</v-btn>
        </v-col>
        <v-col cols="1" />
      </v-row>
      <br />
    </v-card>
    <br />
    <v-card>
      <v-card-title>
        <h3>Passwort ändern</h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-form ref="form" v-model="valid_password">
        <v-row dense>
          <v-col cols="1" />
          <v-col cols="10">
            <v-text-field
              append-icon="lock_open"
              :type="showOld ? 'text' : 'password'"
              name="oldpassword"
              label="Altes Passwort"
              color="info"
              dense
              class="input-group--focused"
              :rules="[rules.required]"
              v-model="oldpassword"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="1" />
          <v-col cols="5">
            <v-text-field
              append-icon="lock"
              name="password"
              label="Neues Passwort"
              color="info"
              id="password"
              type="password"
              v-model="password"
              :rules="[
                rules.required,
                rules.password,
                passwordVerificationRule,
              ]"
            >
            </v-text-field>
          </v-col>
          <v-col cols="5">
            <v-text-field
              append-icon="lock_open"
              name="password_verification"
              label="Passwort wiederholen"
              color="info"
              id="password_verification"
              type="password"
              v-model="password_verification"
              :rules="[rules.required, passwordVerificationRule]"
            >
            </v-text-field>
          </v-col>
        </v-row>
      </v-form>
      <v-row justify="end">
        <v-col cols="4" class="text-right">
          <v-btn
            color="primary"
            :disabled="!valid_password"
            @click="submitChangePassword()"
            >Passwort ändern</v-btn
          >
        </v-col>
        <v-col cols="1" />
      </v-row>
      <br />
    </v-card>
    <br />
    <v-card>
      <v-card-title>
        <h3>Account Informationen</h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Registriert:</v-subheader>
          <v-text-field
            label="Registriert"
            v-model="accountdata.creationdate"
            :loading="loading"
            hide-details
            disabled
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Verifiziert:</v-subheader>
          <v-text-field
            label="Verifiziert"
            v-model="accountdata.verified"
            :loading="loading"
            hide-details
            disabled
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="1" />
        <v-col cols="10">
          <v-subheader>Letzte Anmeldung:</v-subheader>
          <v-text-field
            label="Letzte Anmeldung"
            v-model="accountdata.lastlogindate"
            :loading="loading"
            hide-details
            disabled
            solo
            dense
          ></v-text-field>
        </v-col>
      </v-row>
      <br />
    </v-card>
    <br />

    <v-card>
      <v-card-title>
        <h3>Authentifizierer (Karte, Telefon, Gerät):</h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-form ref="form" v-model="valid_requestKey">
        <v-row dense>
          <v-col cols="1" />
          <v-col cols="10">
            <v-subheader>Status:</v-subheader>
            <v-chip
              smalle
              :color="authenticator_status_color"
              style="width: 100%; justify-content: center"
            >
              <span style="color: white">
                {{ authenticator_status_message }}</span
              >
            </v-chip>
          </v-col>
        </v-row>
        <v-row v-if="accountdata.authenticator_status == 'Unset'" dense>
          <v-col cols="1" />
          <v-col cols="10">
            <v-subheader>Authentifizierer freischalten:</v-subheader>
            <v-text-field
              label="Hier deinen Freigabe-Code eingeben"
              v-model="authenticatorCode"
              :rules="[
                rules.required,
                rules.requestKey_digits,
                rules.requestKey_length,
              ]"
              name="authenticatorCode"
              id="authenticatorCode"
              :loading="loading"
              @keyup="uppercase"
              solo
              dense
            ></v-text-field>
          </v-col>
        </v-row>
        <br />
        <v-row justify="end">
          <v-col
            v-if="accountdata.authenticator_status === 'Unset'"
            cols="4"
            class="text-right"
          >
            <v-btn
              color="primary"
              :disabled="!valid_requestKey"
              @click="submitAssignCard()"
              >Karten-ID zuweisen</v-btn
            >
          </v-col>
          <v-col cols="1" />
        </v-row>
        <v-row
          v-if="accountdata.authenticator_status !== 'Unset'"
          justify="end"
        >
          <v-col cols="1" />
          <v-col cols="3" class="text-right">
            <v-btn color="warning" @click="submitUnassignCard()">Remove</v-btn>
            <v-btn
              v-if="accountdata.authenticator_status !== 'Locked'"
              color="error"
              @click="submitUnassignCard()"
              >Lost it</v-btn
            >
          </v-col>
          <v-col cols="1" />
        </v-row>
        <br />
      </v-form>
    </v-card>
    <br />
    <!--
    <v-card>
      <v-card-title>
        <h3>Pin</h3>
        <v-spacer></v-spacer>
      </v-card-title>
      <v-form ref="form" v-model="valid_pin">
        <v-row dense>
          <v-col cols="1" />
          <v-col cols="10">
            <v-alert v-if="accountdata.pinIsLocked" type="error" dense>
              Your pin is locked due to invalid inputs. Please submit a new pin.
            </v-alert>
            <v-subheader>Your Password</v-subheader>
            <v-text-field
              append-icon="lock_open"
              :type="showOld ? 'text' : 'password'"
              name="password"
              label="Your password"
              v-model="pin_password"
              dense
              solo
              class="input-group--focused"
              :rules="[rules.required]"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="1" />
          <v-col cols="5">
            <v-subheader>New pin</v-subheader>
            <v-text-field
              append-icon="lock"
              name="pin"
              label="Your new pin"
              id="pin"
              type="password"
              v-model="pin"
              :rules="[
                rules.required,
                rules.pin_digits,
                rules.pin_length,
                pinVerificationRule,
              ]"
            >
            </v-text-field>
          </v-col>
          <v-col cols="5">
            <v-subheader>Repeat pin</v-subheader>
            <v-text-field
              append-icon="lock_open"
              name="pin_verification"
              label="Repeat your new pin"
              id="pin_verification"
              type="password"
              v-model="pin_verification"
              :rules="[rules.required, pinVerificationRule]"
            >
            </v-text-field>
          </v-col>
        </v-row>
        <v-row justify="end">
          <v-col cols="4" class="text-right">
            <v-btn
              color="primary"
              :disabled="!valid_pin"
              @click="submitChangePin()"
              >Submit</v-btn
            >
          </v-col>
          <v-col cols="1" />
        </v-row>
        <br />
      </v-form>
    </v-card>
    -->
  </v-container>
</template>

<script>
import Vue from "vue";
import * as actionBuilder from "@/api/actionBuilder";
import { createHelpers } from "vuex-map-fields";

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
      authenticatorCode: "",
      rules: {
        required: (v) => !!v || "Is required",
        pin_digits: (v) => /([0-9]{6})/.test(v) || "Pin have to have 6 digits",
        pin_length: (v) => v.length == 6 || "Pin have to have 6 digits",
        requestKey_digits: (v) =>
          /([0-9A-Fa-f:]{17})/.test(v) ||
          "The request key have to have 17 characters",
        requestKey_length: (v) =>
          v.length == 17 || "The request key have to have 17 characters",
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
      this.authenticatorCode = this.authenticatorCode.toUpperCase();
    },
    getAccountData(view) {
      if (this.viewDictionary.hasOwnProperty(view)) {
        return this.viewDictionary[view].entries[0];
      } else {
        return {};
      }
    },
    submitUnassignCard() {
      let action = [
        actionBuilder.newUnassignUserAuthenticatorAction(
          "users",
          this.accountdata.email
        ),
        actionBuilder.newGetViewAction("account", "userInfo"),
      ];
      this.$store.dispatch("actions/emitActionRequest", action);
      this.authenticatorCode = "";
    },
    submitAssignCard() {
      let action = [
        actionBuilder.newAssignUserAuthenticatorAction(
          "users",
          this.accountdata.email,
          this.authenticatorCode
        ),
        actionBuilder.newGetViewAction("account", "userInfo"),
      ];
      this.$store.dispatch("actions/emitActionRequest", action);
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
        actionBuilder.newGetViewAction("account", "userInfo"),
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
    authenticator_status_color() {
      if (this.accountdata.authenticator_status) {
        if (this.accountdata.authenticator_status.toUpperCase() === "VALID") {
          return "success";
        }
        if (this.accountdata.authenticator_status.toUpperCase() === "UNSET") {
          return "blue";
        }
        if (this.accountdata.authenticator_status.toUpperCase() === "LOCKED") {
          return "error";
        }
      }
      return "error";
    },
    authenticator_status_message() {
      if (this.accountdata.authenticator_status) {
        if (this.accountdata.authenticator_status.toUpperCase() === "VALID") {
          return "Valid";
        }
        if (this.accountdata.authenticator_status.toUpperCase() === "UNSET") {
          return "Please assign.";
        }
        if (this.accountdata.authenticator_status.toUpperCase() === "LOCKED") {
          return "Got locked, please assign a new one.";
        }
      }
      return "";
    },
  },
  watch: {
    viewStates(newValue, oldValue) {
      console.log("change on viewStates detected with", newValue, oldValue);
      if (this.viewStates["account/userInfo"] === "ready") {
        this.accountdata = Object.assign(
          {},
          this.getAccountData("account/userInfo")
        );
        console.log("AccountData: ", this.accountdata);
        this.loading = false;
      } else {
        this.loading = true;
      }
    },
  },
  mounted() {
    let getViewAction = [actionBuilder.newGetViewAction("account", "userInfo")];
    this.$store.dispatch("actions/emitActionRequest", getViewAction);
  },
};
</script>

<style scoped>
</style>
