<template>
    <vue-markdown class="report" :source="report.markdown" :linkify="false"></vue-markdown>
</template>

<script>
import VueMarkdown from 'vue-markdown';
import { mapGetters } from 'vuex';

export default {
  name: 'report',
  components: { VueMarkdown },
  data () {
    return {
    };
  },
  computed: {
    ...mapGetters([
      'wbReport',
    ]),
    report () {
      if (this.$store.state.wbReport) {
        return this.$store.state.wbReport;
      } else {
        return null;
      }
    },
  },
  created () {
    this.$store.dispatch('getReport', this.$route.params.sha);
  },
};
</script>

<style lang="scss" scoped>
.report {
  margin: 20px;
  text-align: left;

}
</style>