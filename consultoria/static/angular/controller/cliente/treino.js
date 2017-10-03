(function() {
	"use strict";

	angular.module("consultoria").controller("TreinoController", TreinoController);

	TreinoController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function TreinoController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();