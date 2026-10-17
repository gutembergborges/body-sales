<template>
  <div class="q-pa-md">
    <div class="q-gutter-md">
      <q-select filled clearable v-model="group" :options="groupsFiltered"
        color="red" label="Grupo" option-value="Codigo_Grupo" option-label="Descricao"
        input-debounce="0" @input="getProductsByFilter" use-input="" @filter="getGroupsByFilter">
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              Grupo não encontrado
            </q-item-section>
          </q-item>
        </template>
      </q-select>

      <q-input filled color="red" v-model="description" label="Descrição" placeholder="Busca na Body"
        use-input input-debounce="0" @input="getProductsByFilter" />

      <q-input filled color="red" v-model="code" label="Código" placeholder="Código do produto"
        debounce="400" @input="getProductsByFilter" />

      <q-infinite-scroll @load="onLoadProducts" class="q-mt-md row">
        <div v-for="(product, index) in products" :key="index" class="q-gutter-xs-xs col-12">
          <q-card class="my-card">
            <q-card-actions align="right">
              <q-btn flat round color="teal" icon="add_shopping_cart" @click="addToCart(product)" />
            </q-card-actions>
            <router-link :to="{ name: 'Produto', params: { product: product} }">
              <q-img class="card-img" :src="product.urlProduto"></q-img>
            </router-link>
            <q-card-section>
              <div class="text-h7">{{ product.Produto_Descricao }}</div>
              <div class="text-subtitle2">R$ {{ product.preco_venda }},00</div>
            </q-card-section>
            <q-card-section>
              <div class="text-caption">Disponível no estoque: {{ product.Saldo_Disponivel_Dominio }}</div>
            </q-card-section>
          </q-card>
        </div>

        <template v-slot:loading>
          <div v-if="productsCount > 0" class="fixed-center">
            <q-spinner color="grey" size="6em"></q-spinner>
          </div>
        </template>
      </q-infinite-scroll>
      <q-page-scroller position="bottom-right" :scroll-offset="150" :offset="[18, 18]">
        <q-btn fab icon="keyboard_arrow_up" color="accent" />
      </q-page-scroller>
    </div>
  </div>
</template>

<script>
import {
  QSelect, QCard, QCardSection, QCardActions, QImg,
  QInfiniteScroll, QSpinner, QTooltip, QPageScroller,
  Notify
  } from 'quasar'

export default {
  components: {
    QSelect, QCard, QCardSection, QCardActions, QImg,
    QInfiniteScroll, QSpinner, QTooltip, QPageScroller
  },
  data () {
    return {
      group: { Codigo_Grupo: 13, Descricao: "ALBUMINA", urlGrupo: null },
      description: "",
      code: "",
      page: 1,
    }
  },
  mounted () {
    // this.getProductsByFilter()
    this.$store.dispatch('produtos/obterGrupos', {})
  },
  computed: {
    groupsFiltered() {
      return this.$store.getters['produtos/getGroupsFiltered']
    },
    products() {
      return this.$store.getters['produtos/getProducts']
    },
    productsCount() {
      return this.$store.getters['produtos/getProductsCount']
    }
  },
  methods: {
    getGroupsByFilter(val, update) {
      if (val === '') {
        update(() => {
          this.$store.commit('produtos/setGroupsFiltered', null)
        })
        return
      }

      update(() => {
        const needle = val.toUpperCase()
        this.$store.commit('produtos/setGroupsFiltered', needle)
      })
    },
    getProductsByFilter() {
      this.page = 1
      this.$store.dispatch('produtos/filtrar', {
        group: this.group.Codigo_Grupo,
        description: this.description,
        code: this.code,
        page: this.page
      })
    },
    getProductsByPagination(pagination) {
      this.$store.dispatch('produtos/paginar', {
        group: this.group.Codigo_Grupo,
        description: this.description,
        code: this.code,
        page: pagination
      })
    },
    onLoadProducts (index, done) {
      // if(this.productsCount > 0) {
        setTimeout(() => {
          this.getProductsByPagination(this.page)
          this.page += 1
          done()
        }, 3000)
      // }
    },
    addToCart (product) {
      this.$store.dispatch('produtos/verificarEstoque', { product: product, quantityAdded: 1 })
      if(this.$store.getters['produtos/getProductDisponibility'])
        this.$store.dispatch('produtos/adicionarNoCarrinho', product)
    }
  }
}
</script>
<style>
.my-card {
  width: 95%;
  margin-left: 0.55rem;
  margin-bottom: 1rem;
  height: auto;
}
.card-img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 80%;
  /* min-height: 181.44px; */
}
</style>
