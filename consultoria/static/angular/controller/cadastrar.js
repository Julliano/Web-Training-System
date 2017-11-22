(function() {
	"use strict";

	angular.module("consultoria").controller("CadastrarController", CadastrarController);

	CadastrarController.$inject = [ "$http", "LoginService", "Notification", "$state" ];

	/* @ngInject */
	function CadastrarController($http, LoginService, Notification, $state) {
		var vm = this;
		vm.estados = ["Outro","Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins"];
		vm.brasil = true;
		vm.salvar = salvar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		function salvar() {
			vm.submitPromise.promise = $http.post('/cadastroNovoUsuario/', vm.usuario).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
			$state.go("index.start")
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
		
	}

})();