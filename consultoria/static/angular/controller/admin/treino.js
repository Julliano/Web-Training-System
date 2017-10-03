(function() {
	"use strict";

	angular.module("consultoria").controller("TreinoAdminController", TreinoAdminController);

	TreinoAdminController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function TreinoAdminController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();