(function() {
	"use strict";

	angular.module("consultoria").controller("RecuperarEmailController", RecuperarEmailController);

	RecuperarEmailController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function RecuperarEmailController($http, LoginService, Notification) {
		var vm = this;
		vm.salvar = salvar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		function salvar() {
			vm.submitPromise.promise = $http.post('/emailRecuperacao/', vm.usuario).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
		
	}

})();