;(function() {
	"use strict";

	angular.module("consultoria").controller("ClientePlanoController", ClientePlanoController);

	ClientePlanoController.$inject = ['$http', 'LoginService', 'Notification', '$window', '$state', '$uibModal'];

	function ClientePlanoController($http, LoginService, Notification, $window, $state, $uibModal) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.pagar = pagar;
		vm.confere = confere;
		vm.ajustaForm = ajustaForm;
		vm.classVenda = classVenda;
		vm.modalPlano = modalPlano;
		
		init();
		
		function init(){
			listar();
		}
		
		function listar(){
			$http.get('/planosCliente').then(function(response) {
				vm.vendas = response.data;
			})
		}
		
		function modalPlano(modelo) {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-app-escolhePlano/modal-app-escolhePlano.html'
						},
						size : 'lg',
//						backdrop : 'static',
						controller : "ModalEscolhaPlanoController",
						controllerAs : "ModalEscPlanoCtrl"
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}
		
		function pagar(venda){
			$window.open('https://pagseguro.uol.com.br/v2/checkout/payment.html?code='+venda.pagamento.codigo)
//			$window.open('https://sandbox.pagseguro.uol.com.br/v2/checkout/payment.html?code='+venda.pagamento.codigo)
		}
	
		function confere(venda){
			return venda.pagamento.status == 'Aguardando pagamento' || venda.pagamento.status == 'aguardando pagamento'
		} 

		function ajustaForm(form){
			if(form.status == 'pendente'){
				$state.go("app.formulario", {id:form.id})
			}
		}
		
		function classVenda(venda){
			if(venda.formulario.status == 'pendente'){
				return 'warning'
			}
		}
		
	}

})();