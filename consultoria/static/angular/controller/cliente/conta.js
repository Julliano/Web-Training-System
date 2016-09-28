(function() {
	"use strict";

	angular.module("simfaz").controller("ClienteContaController", ClienteContaController);

	ClienteContaController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function ClienteContaController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.salvar = salvar;

		function salvar() {			
			$http.put('/usuarios/', vm.usuario).then(function(response) {
				Notification.success(response.data);
			}, function(response) {
				Notification.error(response.data);
			})
		}
	}

})();