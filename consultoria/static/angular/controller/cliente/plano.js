(function() {
	"use strict";

	angular.module("consultoria").controller("ClientePlanoController", ClientePlanoController);

	ClientePlanoController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function ClientePlanoController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();