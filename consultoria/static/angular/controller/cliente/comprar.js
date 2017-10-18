(function() {
	"use strict";

	angular.module("consultoria").controller("ComprarController", ComprarController);

	ComprarController.$inject = [ "$http", "Notification", "$scope", "LoginService"];

	/* @ngInject */
	function ComprarController($http, Notification, $scope, LoginService) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.comprar = comprar;
		vm.submitPromise = { message : "Aguarde..."	};

		function comprar(param) {
			if(vm.usuario){
				vm.submitPromise.promise = $http.post('/comprarConsultoria/' + param, vm.formulario).then(httpSuccess, httpFail);
			} else {
				Notification.error('Entre em contato pelo email: jullianoVolpato@gmail.com, e resolveremos seu problema.');
			}
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
		
	}

})();