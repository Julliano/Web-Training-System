(function() {
	"use strict";

	angular.module("consultoria").controller("PlanoAdminController", PlanoAdminController);

	PlanoAdminController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function PlanoAdminController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();