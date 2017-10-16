(function() {
	"use strict";

	angular.module("consultoria").controller("StartController", StartController);

	StartController.$inject = [ "$http", "Notification" ];

	/* @ngInject */
	function StartController($http, Notification) {
		var vm = this;
		vm.enviar = enviar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		function enviar() {
			vm.submitPromise.promise = $http.post('/emailContato/', vm.formulario).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
		
	}

})();