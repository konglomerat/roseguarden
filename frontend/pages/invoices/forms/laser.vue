<template>
  <v-app id="login" class="primary lighten-3">
    <v-main>
      <v-container fluid fill-height>
        <v-layout  justify-center>
          <v-flex xs12 sm10 md10 lg8>
            <v-card width="100%">
              <v-img
                cover
                height="250"
                src="/images/laser_logbook_header.jpg">
              </v-img>
            </v-card>
            <v-card class="pa-3">
              <v-card-text>
                <div class="layout column align-center">
                  <!---
                  <img src="../static/konglo_logo.png" alt="Roseguarden logo" width="120" height="120">
                  ---->
                  <h1 class="info--text">Laser Logbuch</h1>
                </div>
              </v-card-text>
            </v-card>
            <br>
            <div v-if="form_state==='enter_data'">
                <v-form v-model="valid_form" @submit.prevent ref="form">
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Mit welchem Laserschneider hast du gearbeitet?</h2>
                            <v-radio-group v-model="machine" :rules="[rules.required]">
                                <v-radio label="Zing Laser" value="Zing"></v-radio>
                                <v-radio label="DIT Lasersaur" value="Lasersaur"></v-radio>
                            </v-radio-group>
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Wann hast du gelasert? (Leistungsdatum)</h2>
                            <v-menu
                            :close-on-content-click="true"
                            max-width="290"
                            >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                :value="computedDate"
                                prepend-icon="mdi-calendar"                        
                                clearable
                                :rules="[rules.required]"
                                readonly
                                v-on="on"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                                v-model="date"
                                locale="de"                            
                            ></v-date-picker>
                            </v-menu>
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Zählerstand zum Beginn?</h2>

                            Bitte folgendes Format verwenden: HHHH:MM:SS
                            <v-text-field
                                v-model="counter_at_start"
                                :rules="[check_for_plausible_counter, rules.counter]"
                                prepend-icon="mdi-counter"                        
                                label="Zählerstand zum Beginn"
                            ></v-text-field>                        

                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Zählerstand zum Ende?</h2>
                        Bitte folgendes Format verwenden: HHHH:MM:SS
                        <v-text-field
                            v-model="counter_at_end"
                            :rules="[rules.counter, check_for_plausible_counter]"
                            prepend-icon="mdi-counter"                        
                            label="Zählerstand zum Ende"
                        ></v-text-field>                        
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Dein Projekt?</h2>
                        Eine kurze Beschreibung für dich, um die Rechnung leichter zuordnen zu können.
                        <v-text-field
                            v-model="project_description"
                            prepend-icon="mdi-lightbulb-on"                        
                            label="Deine Beschreibung"
                            :rules="[rules.required]"
                        ></v-text-field>                        
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Bist du Vereinsmitglied?</h2>
                            <v-radio-group v-model="membership" :rules="[rules.machine]">
                                <v-radio label="Ja, Vereinsmitglied" value="member"></v-radio>
                                <v-radio label="Nein, kein Vereinsmitglied" value="no_member"></v-radio>
                            </v-radio-group>
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Was ist der Verwendungszweck?</h2>
                            <v-radio-group v-model="purpose" :rules="[rules.machine]">
                                <v-radio label="Privat" value="1"></v-radio>
                                <v-radio label="Betrieblich" value="2"></v-radio>
                                <v-radio label="Vereinsintern" value="3"></v-radio>
                            </v-radio-group>
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                        <h2 class="info--text">Optional: Welches Material hast du gelasert?</h2>
                        Für die Statistik ;-)
                            <v-radio-group v-model="material">
                            <v-radio label="MDF/HDF" value="MDF/HDF"></v-radio>
                            <v-radio label="PMMA/Acrylglas/Plexiglas" value="PMMA"></v-radio>
                            <v-radio label="Papier/Pappe" value="Paper"></v-radio>
                            <v-radio label="Sonstiges" value="Others"></v-radio>
                            </v-radio-group>
                        </div>
                    </v-card-text>
                    </v-card>
                    <br>
                    <div class="layout column align-center">
                        <v-btn type="submit" color="info" @click="calculate_and_proceed">
                            Berechnen und weiter
                        </v-btn>
                    </div>
                    <br>
                </v-form>
            </div>
            <div v-else>
                <div class="layout column align-center">
                    <v-btn color="info" @click="update_data">
                        Angaben ändern
                    </v-btn>
                </div>
                <br>
                <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                            <h2 class="info--text">Laser-Kosten im Konglomerat</h2>
                            <div>
                                <br>
                                Im Konglomerat fallen folgende Kosten für das selbstständige lasern an.
                            </div>
                            <v-img
                                cover
                                src="/images/laser_pricing.svg">
                            </v-img>
                        </div>
                    </v-card-text>
                </v-card>                
                <br>
                <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                            <h2 class="info--text">Berechnetet Kosten</h2>
                        </div>
        
                        <br>

                        <div class="layout column align-center">
                            <h3 class="info--text">Laserzeit:</h3>
                        </div>

                        <br>

                        <div class="layout column align-center">
                            <h2> {{laser_usage}}</h2>
                        </div>

                        <br>                        

                        <div class="layout column align-center">
                            <h3 class="info--text">Durchschnittlicher Preis je Minute:</h3>
                        </div>

                        <br>

                        <div class="layout column align-center">
                            <h2> {{laser_average_costs_per_minute}}</h2>
                        </div>

                        <br>

                        <div class="layout column align-center">
                            <h3> ( Erste Minute: {{laser_costs_first_minute}} &nbsp; Letzte Minute: {{laser_costs_last_minute}} )</h3>
                        </div>

                        <br>

                        <div class="layout column align-center">
                            <h3 class="info--text">Gesamtkosten:</h3>
                        </div>

                        <br>

                        <div class="layout column align-center">
                            <h2> {{laser_costs_total}}</h2>
                        </div>

                        <br>

                        <div v-if="laser_costs_tax">

                            <div class="layout column align-center">
                                <h3 class="info--text">Enthaltene Steuer:</h3>
                            </div>

                            <br>

                            <div class="layout column align-center">
                                <h2> {{laser_costs_tax}}</h2>
                            </div>

                            <br>

                        </div>

                        <div class="layout column align-center">
                            <h3 class="red--text">* Achtung : Die berechneten Kosten können bei Rechnungsstellung abweichen !</h3>
                        </div>

                    </v-card-text>
                </v-card>            
                <br>    
                <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                            <h2 class="info--text">Anmelden</h2>
                        </div>

                        <br v-if="!guest_email_input">

                        <div v-if="!guest_email_input" class="layout column align-center">
                            <h3 class="info--text">Bitte melde dich an:</h3>
                        </div>

                        <v-row v-if="!guest_email_input">
                            <v-col
                                cols="12"
                                lg="10"
                                offset-lg="1"
                                sm="10"
                                offset-sm="1"
                                xs="12"
                                justify="center"
                                align="center"
                                dense
                            >
                                <v-form
                                v-model="valid_credentials"
                                @submit.prevent="login"
                                id="login-form"
                                >
                                <v-text-field
                                    append-icon="person"
                                    name="login"
                                    label="E-Mail"
                                    type="email"
                                    v-model="model.username"
                                    color="info"
                                    :rules="[rules.email, rules.required]"
                                ></v-text-field>
                                <v-text-field
                                    append-icon="lock"
                                    name="password"
                                    label="Passwort"
                                    id="password"
                                    type="password"
                                    color="info"
                                    v-model="model.password"
                                    :rules="[rules.required]"
                                ></v-text-field>
                                </v-form>
                            </v-col>
                            <v-col cols="9" lg="5" offset-lg="2" sm="5" offset-sm="2" xs="9">
                                <v-btn
                                dense
                                text
                                small
                                color="info"
                                href="/user/lostpassword"
                                target="_blank"
                                >Passwort vergessen?</v-btn
                                >
                            </v-col>
                            <v-col
                                cols="12"
                                offset="0"
                                lg="3"
                                offset-lg="0"
                                sm="3"
                                offset-sm="0"
                                xs="12"
                                align="center"
                                justify="center"
                            >
                                <v-btn
                                color="primary"
                                class="text-center"
                                form="login-form"
                                type="submit"
                                @click="login"
                                :disabled="!valid_credentials"
                                >Anmelden</v-btn
                                >
                            </v-col>

                        </v-row>

                        <br v-if="!guest_email_input">

                        <div v-if="!guest_email_input" class="layout column align-center">
                            <h3 class="info--text">Oder alternativ:</h3>
                        </div>
                        <br v-if="!guest_email_input">
                        <div v-if="!guest_email_input" class="layout column align-center">
                            <v-btn color="info" @click="procceed_as_guest">
                                Ohne Anmeldung fortfahren 
                            </v-btn>
                        </div>
                        <div v-else class="layout column">
                            <v-col
                                cols="12"
                                lg="10"
                                offset-lg="1"
                                sm="10"
                                offset-sm="1"
                                xs="12"
                                justify="center"
                                align="center"
                                dense
                            >
                                <v-text-field
                                    append-icon="person"
                                    name="login"
                                    label="E-Mail (Gast)"
                                    type="email"
                                    v-model="model.username"
                                    color="info"
                                    :rules="[rules.email, rules.required]"
                                ></v-text-field>
                            An diese Adresse wird die generierte Rechnung geschickt.

                            </v-col>                            
                        </div>

                        <br v-if="guest_email_input">
                        <div v-if="guest_email_input" class="layout column align-center">
                            <h3 class="info--text">Oder alternativ:</h3>
                        </div>

                        <br v-if="guest_email_input">

                        <div v-if="guest_email_input" class="layout column align-center">
                            <v-btn color="info" @click="procceed_as_user">
                                Als registrierter Nutzer Anmelden 
                            </v-btn>
                        </div>


                    </v-card-text>
                </v-card>                
                <br>
                <v-card class="pa-3">
                    <v-card-text>
                        <div class="layout column">
                            <h2 class="info--text">Angaben eintragen</h2>
                        </div>

                        <v-col
                            cols="12"
                            lg="10"
                            offset-lg="1"
                            sm="10"
                            offset-sm="1"
                            xs="12"
                            dense
                        >                                
                            <v-switch
                                dense
                                v-model="accept_conditions"
                                :rules="[rules.accept]"
                            >
                                <template v-slot:label>
                                <span>
                                    Ich habe die <a href="/termsofuse" target="_blank" @click.stop>Nutzungsvereinbarung</a> und die <a href="/privacy" target="_blank" @click.stop>Datenschutzerklärung</a> gelesen und erkläre mich damit einverstanden.
                                </span>
                                </template>
                            </v-switch>
                            <v-switch
                                dense
                                v-model="accept_submission"
                                :rules="[rules.accept]"
                            >
                                <template v-slot:label>
                                <span>
                                    Ich bin damit einverstanden, dass meine Angaben an den Konglomerat e.V. übermittelt werden.
                                </span>
                                </template>
                            </v-switch>

                        </v-col>

                        <div class="layout column align-center">
                            <v-btn color="info">
                                Absenden
                            </v-btn>

                        </div>
                    </v-card-text>
                </v-card>                


            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState } from "vuex";
import moment from 'moment';
import * as actionBuilder from "@/api/actionBuilder";
import axios from 'axios';

export default {
  layout: "default",
  data: () => ({
    loading: false,
    query: "-",
    form_state: "enter_data",
    valid_form: false,
    valid_date: false,
    date: "",
    purpose: null,
    machine: null,
    membership : null,
    material : null,
    laser_usage:"",
    laser_costs_first_minute: "",
    laser_costs_last_minute: "",
    laser_average_costs_per_minute: "",
    laser_costs_total: "",
    laser_costs_tax: "",
    guest_email_input: false,
    valid_credentials: false,
    counter_at_start : "",
    counter_at_end : "",
    accept_conditions : false,
    accept_submission : false,
    project_description: "",
    rules: {
      required: (value) => !!value || "Diese Angabe wird benötigt.",
      machine: (value) => !!value || "Bitte den verwendeten Laser angeben.",
      counter: (v) => /([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b/.test(v) || "Bitte im folgenden Format eingeben : HHHH:MM:SS",
      email: (v) =>
        !v ||
        /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,5})+$/.test(v) ||
        "Bitte gebe eine gültige eMail-Adresse an.",
    },
    model: {
      username: "",
      password: "",
    },
  }),
  computed: {
    computedDate () {
      return this.date ? moment(this.date).locale("de").format('dddd, MMMM Do YYYY',"de") : ''
    },
  },
  methods: {
    async validate () {
        const { valid_machine } = await this.$refs.form_machine.validate()
    },
    check_for_plausible_counter () {
        let vals_start = this.counter_at_start.split(":").map(function(item) {
            return parseInt(item, 10);
        });
        let vals_end = this.counter_at_end.split(":").map(function(item) {
            return parseInt(item, 10);
        });
        let seconds = ((vals_end[0] * 60 + vals_end[1]) * 60 + vals_end[2]) - 
                    ((vals_start[0] * 60 + vals_start[1]) * 60 + vals_start[2]);
        return !this.counter_at_end || (seconds > 0) || "Der Zählerstand am Ende muss größer sein als der Zählerstand am Anfang.";
    },    
    get_calculated_costs() {
        let action = [
        actionBuilder.newAction(
            "invoices",
            "calculateLaserCosts",
            {
                "counter_at_start" : this.counter_at_start,
                "counter_at_end" : this.counter_at_end,
                "membership" : this.membership
            }
        ),
        ];
        this.$store.dispatch("actions/emitActionRequest", action).then(response => {
            this.laser_usage = response.usage;
            this.laser_costs_first_minute = response.costs_first_minute
            this.laser_costs_last_minute = response.costs_last_minute
            this.laser_average_costs_per_minute = response.average_costs_per_minute
            this.laser_costs_total = response.total_costs;
            this.laser_costs_tax = response.tax;
        });

    },
    update_data () {
        window.scrollTo(0,0);
        this.form_state = "enter_data";
    },
    calculate_and_proceed() {
        const { valid } = this.$refs.form.validate();
        if (this.valid_form == true) {
            window.scrollTo(0,0);
            this.get_calculated_costs();
            this.form_state = "submit";
        }
    },
    procceed_as_user() {
        this.guest_email_input = false;
    },
    procceed_as_guest() {
        this.guest_email_input = true;
    },
    login() {
      //this.loading = true;

      let redirect = "";
      if (this.$route.query.hasOwnProperty("redirect")) {
        redirect = this.$route.query.redirect;
      }
      let loginAction = [
        actionBuilder.newLoginUserAction(
          this.model.username,
          this.model.password,
          { redirect: redirect }
        ),
      ];
      this.$store.dispatch("actions/emitActionRequest", loginAction);
      this.$store.dispatch("user/login", null);
    },
    cancel() {
      this.$store.dispatch("user/logout", null);
      this.$router.push("/dashboard");
    },
  },
  mounted() {
    let redirect = "no";
    if (this.$route.query.hasOwnProperty("redirect")) {
      redirect = this.$route.query.redirect;
    }
  },
};
</script>
<style scoped lang="css">
#login {
  height: 100%;
  width: 100%;
  content: "";
  z-index: 0;
}
</style>
