<template>

  <div class="home top">
      <h1>WishBuilder</h1>
    <div class="row justify-content-center width-100">
      <div class="col-8">
        <h1>Search for a dataset</h1>

        <div class="row" style="margin-bottom:1rem;">
            <input class="form-control" type="text" v-model="searchText" placeholder="Search">
        </div>

      </div>
    </div>
    <b-table striped hover outlined bordered :items="items" :fields="fields" 
      :sort-by.sync="sortBy" :sort-desc.sync="sortDesc" :filter="searchText" @row-clicked="info">
    </b-table>

    <b-modal id="modalInfo" @hide="resetModal" :title="modalInfo.title" cancel-only>
      <div v-for="test in this.modalInfo.tests">
          <pre>Pull Request #{{test.pr}} {{test.date}} sha = {{test.sha}}
            Status: {{test.status}} <button class="btn-small btn-danger" @click="viewReport(test.sha)">View Report</button>

          </pre>
      </div>
    </b-modal>
    
  </div>
</template>

<script>
import DatasetDetail from '../shared/DatasetDetail';
import selectize from '../shared/Selectize';
import router from '../../router';
// import prismjs from 'prismjs';

export default {
  name: 'datasets',
  components: { DatasetDetail, selectize },
  data () {
    return {
      sortBy: 'e_date',
      sortDesc: true,
      searchText: '',
      fields: [
        {
          key: 'branch',
          sortable: true,
        },
        {
          key: 'date',
          sortable: true,
        },
        {
          key: 'user',
          sortable: true,
        },
        {
          key: 'status',
          sortable: true,
        },
        {
          key: 'time_elapsed',
          sortable: false,
        },
        {
          key: 'feature_variables',
          sortable: true,
        },
        {
          key: 'meta_variables',
          sortable: true,
        },
        {
          key: 'samples',
          sortable: true,
        },
      ],
      modalInfo: { title: '', tests: [] },
    };
  },
  updated () {
  },
  computed: {
    items () {
      return this.$store.state.wbData;
    },
    wbData () {
      return this.$store.state.wbData;
    },
  },
  methods: {
    info (item, button) {
      this.modalInfo.title = item.branch;
      let tests = [];
      for (var test in this.wbData) {
        if (this.wbData[test].branch === item.branch) {
          tests.push(this.wbData[test]);
        }
      }
      this.modalInfo.tests = tests;
      this.$root.$emit('bv::show::modal', 'modalInfo', button);
    },
    resetModal () {
      this.modalInfo.title = '';
      this.modalInfo.tests = [];
    },
    viewReport (sha) {
    //   this.$store.dispatch('getReport', sha);
      router.push('/wishbuilder/report/' + sha);
    },
  },
  created () {
    this.$store.dispatch('getWishBuilder');
  },
};
</script>

<style lang="scss" scoped>
.dataset-item {
  padding: 15px;
}
.padding-right-0 {
  padding-right: 0px;
}
.width-100 {
  max-width: 100%;
}

pre {
  text-align: left;
}
</style>