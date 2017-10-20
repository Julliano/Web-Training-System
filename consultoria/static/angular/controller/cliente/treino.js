(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteTreinoController", ClienteTreinoController);

	ClienteTreinoController.$inject = [ "$http", "LoginService", "Notification", "TreinoService"];

	/* @ngInject */
	function ClienteTreinoController($http, LoginService, Notification, TreinoService) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.formularios = []
		
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