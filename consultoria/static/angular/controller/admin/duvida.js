(function() {
	"use strict";

	angular.module("consultoria").controller("DuvidaAdminController", DuvidaAdminController);

	DuvidaAdminController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function DuvidaAdminController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();