(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteDuvidaUnitariaController", ClienteDuvidaUnitariaController);

	ClienteDuvidaUnitariaController.$inject = [ "$http", "LoginService", "Notification", "$uibModal", "DuvidaService", "$state", "duvida"];

	/* @ngInject */
	function ClienteDuvidaUnitariaController($http, LoginService, Notification, $uibModal, DuvidaService, $state, duvida) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.duvida = duvida;
		vm.salvarResposta = salvarResposta;
		
		init();
		
		function init(){
			
		}
		
		function salvarResposta(){
			vm.resposta.usuario_id = vm.usuario.id;
			vm.resposta.duvida_id = vm.duvida.id;
			vm.duvida.respostas.push(vm.resposta)
			$http.put('/duvidas/', vm.duvida).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success("Dúvida enviada com sucesso");
			vm.duvida = response.data;
			vm.resposta = null;
		}
	
		function httpFail(response) {
			Notification.error("Erro, favor contate o administrador do sistema.");
		}
		
	}

})();