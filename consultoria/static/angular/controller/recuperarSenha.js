;(function() {
	"use strict";

	angular.module("consultoria").controller("RecuperarSenhaController", RecuperarSenhaController);

	RecuperarSenhaController.$inject = ['$http', 'LoginService', 'Notification'];

	function RecuperarSenhaController($http, LoginService, Notification) {
		var vm = this;
		vm.salvar = salvar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		function salvar() {
			vm.usuario.recuperar = window.location.href.split('=')[1];
			vm.submitPromise.promise = $http.put('/resetarSenha/', vm.usuario).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
			$state.go("index/start")
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
	}

})();