(function() {
	"use strict";

	angular.module("consultoria").controller("DuvidaAdminController", DuvidaAdminController);

	DuvidaAdminController.$inject = [ "$http", "LoginService", "Notification", "DuvidaService", "$state"];

	/* @ngInject */
	function DuvidaAdminController($http, LoginService, Notification, DuvidaService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.verDuvida = verDuvida;
		
		init();
		
		function init(){
			listar();
		}
		
		function listar() {
			DuvidaService.listarAdmin().then(function(response) {
				vm.duvidas = response;
			})
		}
		
		function verDuvida(id){
			$state.go("admin.duvida", {
				id : id
			})
		}
		
	}

})();