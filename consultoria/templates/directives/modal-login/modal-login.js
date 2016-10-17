(function() {
	"use strict";

	angular.module("consultoria").controller("ModalLoginController", ModalLoginController);

	ModalLoginController.$inject = ["$uibModalInstance", "LoginService"];

	function ModalLoginController($uibModalInstance, LoginService ) {
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
			LoginService.login(vm.usuario).then(function(response){
				if(response.auth){
					$uibModalInstance.close();
				}
			});
		}
		
	}
})();
