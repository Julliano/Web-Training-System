(function() {
	"use strict";

	angular.module("consultoria").controller("PlanoController", PlanoController);

	PlanoController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function PlanoController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();