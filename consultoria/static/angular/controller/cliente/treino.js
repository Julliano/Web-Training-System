(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteTreinoController", ClienteTreinoController);

	ClienteTreinoController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function ClienteTreinoController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		
		init();
		
		function init(){
			listar();
		}
		
		function listar(){
			TreinoService.listar().then(function(response) {
				vm.treinos = response;
			})
		}

	}

})();