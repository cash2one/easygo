efft1 = Vue.extend({
	template: '<canvas v-el:mycanvas :width="width" :height="height">4</canvas>',
	data: function(){
		return {
			width: 0,
			height: 0,
		}
	},
	ready:function(){
		effects_one(this.$els.mycanvas)
	},
})
//Vue.component('my-effect', efft1)
/*new efft1({
    el: '#cbb'
})*/

ad = new Vue({
    el: '#test',
    data:{
        ds: [],
        selected: '',
    },
    methods:{
        ma: function(){
            $.post(
                '/info/',
                {'st': 1},
                function(data){
                    ad.ds = data
                },
                'json'
        )
        },
        mb: function(sl){
            console.log(sl)
            console.log(typeof(sl))
            this.selected = (parseInt(sl)) % 3 + 1
            console.log(typeof(this.selected))
            console.log(this.selected)

        },
        ch: function(){
            console.log(this.selected)
        },
    },

    ready: function(){
        this.ma()
        this.selected = 1
    },
})
/*$().ready(function(){
    alert('aa')
    ad.ma()
})*/
Mycomp = Vue.extend({
    template:"<div>comp</div>",
})
Vue.component('my-comp', Mycomp)

aa = new Vue({
    el:'#mysel',
    data: {
        selected: '',
    },
    mthods: {
        ch: function(ev){
            alert(this.selected)
        },
   },
})
