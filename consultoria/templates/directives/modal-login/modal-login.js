(function() {
	"use strict";

	angular.module("consultoria").controller("ModalLoginController", ModalLoginController);

	ModalLoginController.$inject = ["$uibModalInstance", "LoginService", "$window", "$state", "compra"];

	/* @ngInject */
	function ModalLoginController($uibModalInstance, LoginService, $window, $state, compra) {
		var vm = this;
		vm.trendy = "OK";
		vm.agro = "Agrosatélite"
		vm.logar = logar;
		vm.cancelar = cancelar;
		vm.usuario = { lembrar:true }
		
		init();

		function init() {
		}
		
		function cancelar() {
			$uibModalInstance.dismiss();
		}
		
		function logar() {
			LoginService.login(vm.usuario, compra).then(function(response){
				if(response.auth){
					$uibModalInstance.dismiss();
				}
			});
		}
		
	}
})();
