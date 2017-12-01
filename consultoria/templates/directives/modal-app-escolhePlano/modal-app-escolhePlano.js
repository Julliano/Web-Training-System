(function() {
	"use strict";

	angular.module("consultoria").controller("ModalEscolhaPlanoController", ModalEscolhaPlanoController);

	ModalEscolhaPlanoController.$inject = ["$uibModalInstance", "LoginService", "$state"];

	/* @ngInject */
	function ModalEscolhaPlanoController($uibModalInstance, LoginService, $state) {
		var vm = this;
		vm.cancelar = cancelar;
		vm.usuario = LoginService.getUsuario();
		vm.comprar = comprar;
		
		init();

		function init() {
		}
		
		function cancelar() {
			$uibModalInstance.dismiss();
		}
		
		function comprar(param) {
			if(vm.usuario){
				$state.go('app.compra'+parseInt(param))
				$uibModalInstance.dismiss();
			}else{
				$state.go('index.start')
			}
		}
		
		
	}
})();
