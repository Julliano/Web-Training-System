(function() {
	"use strict";

	angular.module("consultoria").controller("ClientePlanoController", ClientePlanoController);

	ClientePlanoController.$inject = [ "$http", "LoginService", "Notification"];

	/* @ngInject */
	function ClientePlanoController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		
		init();
		
		function init(){
			listar();
		}
		
		
		function listar(){
			$http.get('/planosCliente').then(function(response) {
				vm.vendas = response.data;
			})
		}
		
	}

})();