(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteFormularioController", ClienteFormularioController);

	ClienteFormularioController.$inject = [ "$http", "LoginService", "Notification", "form" ];

	/* @ngInject */
	function ClienteFormularioController($http, LoginService, Notification, form) {
		var vm = this;
		vm.formulario = form;
		vm.usuario = LoginService.getUsuario();
		vm.salvar = salvar;

		function salvar() {			
			$http.put('/formulario/', vm.formulario).then(function(response) {
				Notification.success(response.data);
			}, function(response) {
				Notification.error(response.data);
			})
		}
	}

})();