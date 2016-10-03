(function() {
	'use strict'
	angular.module('consultoria').controller('PresentationController', PresentationController)

	PresentationController.$inject = [ "LoginService"]

	function PresentationController(LoginService) {
		var vm = this;
		vm.slide = 1;
		vm.logar = logar;
		vm.usuario = { lembrar:true }
		vm.trendy = "OK";
		vm.agro = "Agrosatélite"
		
		vm.menu = function() {
			return $location.url()
		}
		
		function logar() {
			LoginService.login(vm.usuario)
		}
	}
})()