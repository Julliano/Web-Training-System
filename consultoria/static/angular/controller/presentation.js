(function() {
	'use strict'
	angular.module('consultoria').controller('PresentationController', PresentationController)

	PresentationController.$inject = [ "LoginService", "$uibModal" ]

	function PresentationController(LoginService, $uibModal) {
		var vm = this;
		vm.slide = 1;
		vm.logar = logar;
		vm.usuario = { lembrar:true }
		vm.trendy = "OK";
		vm.agro = "Agrosatélite"
		vm.modalLogin = modalLogin;
		
		vm.menu = function() {
			return $location.url()
		}
		
		function logar() {
			LoginService.login(vm.usuario)
		}
		
		function modalLogin() {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-login/modal-login.html'
						},
						controller : "ModalLoginController",
						controllerAs : "ModalLogCtrl"
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}
		
		
	}
})()