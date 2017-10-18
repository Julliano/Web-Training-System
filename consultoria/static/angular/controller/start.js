(function() {
	"use strict";

	angular.module("consultoria").controller("StartController", StartController);

	StartController.$inject = [ "$http", "Notification", "$scope", "LoginService", "$state"];

	/* @ngInject */
	function StartController($http, Notification, $scope, LoginService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.enviar = enviar;
		vm.comprar = comprar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		function enviar() {
			vm.submitPromise.promise = $http.post('/emailContato/', vm.formulario).then(httpSuccess, httpFail);
		}

		function comprar(param) {
			if(vm.usuario){
//				vm.submitPromise.promise = $http.post('/comprarConsultoria/' + param, vm.formulario).then(httpSuccess, httpFail);
				$state.go('app.compra'+parseInt(param))
			}else{
				$scope.PresentCtrl.modalLogin(param);
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