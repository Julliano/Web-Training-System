(function() {
	"use strict";

	angular.module("consultoria").controller("ClientePlanoController", ClientePlanoController);

	ClientePlanoController.$inject = [ "$http", "LoginService", "Notification", "$window"];

	/* @ngInject */
	function ClientePlanoController($http, LoginService, Notification, $window) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.pagar = pagar;
		vm.confere = confere;
		
		init();
		
		function init(){
			listar();
		}
		
		
		function listar(){
			$http.get('/planosCliente').then(function(response) {
				vm.vendas = response.data;
			})
		}
		
		function pagar(venda){
			$window.open('https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code='+venda.pagamento.codigo)
		}
	
		function confere(venda){
			return venda.pagamento.status == 'aguardando pagamento'
		} 
		
	}

})();