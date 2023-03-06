<template>
  <v-container fluid>
    <v-card height="600px">
      <v-card-title>
        <h3>Consumptions</h3>
      </v-card-title>
      <v-card-text dense>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Vue from "vue";
import { codemirror } from "vue-codemirror";
import { mapState } from "vuex";
import moment from "moment";

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
