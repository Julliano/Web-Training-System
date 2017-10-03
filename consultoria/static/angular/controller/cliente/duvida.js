(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteDuvidaController", ClienteDuvidaController);

	ClienteDuvidaController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function ClienteDuvidaController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();