(function() {
	"use strict";

	angular.module("consultoria").controller("ModeloAdminController", ModeloAdminController);

	ModeloAdminController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function ModeloAdminController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

	}

})();