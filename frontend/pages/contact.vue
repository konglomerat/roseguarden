<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <h3>Kontakt</h3>
      </v-card-title>
      <v-card-text dense>
        <v-alert type="info">
          <p>
            Für Fehler und Optimierungsideen kannst du gern auf
            <a
              href="https://github.com/konglomerat/roseguarden/issues/new/choose"
              target="_blank"
            >
              github
            </a>
            (Account benötigt) ein Ticket erstellen oder uns eine E-Mail an:
            <a href="mailto:rosenritter@listen.konglomerat.org"
              >rosenritter@listen.konglomerat.org</a
            >
            senden.
            <br />
            Für Support-Anfragen schreib uns einfach eine E-Mail an:
            <a href="mailto:zugang@konglomerat.org">zugang@konglomerat.org</a>
            .
          </p>
        </v-alert>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Vue from "vue";
import { codemirror } from "vue-codemirror";
import { mapState } from "vuex";
import moment from "moment";

// import { GenericNode } from '@/nodes/generic'

import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(VueAxios, axios);

export default {
  layout: "dashboard",
  components: {},
  data: () => ({
    info: "",
  }),
  methods: {
    ok() {},
  },
  watch: {
    info: function (val) {},
  },
  computed: {
    test: function () {},
  },
  created() {},
  mounted() {},
};
</script>

<style scoped></style>
