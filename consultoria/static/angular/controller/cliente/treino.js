(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteTreinoController", ClienteTreinoController);

	ClienteTreinoController.$inject = [ "$http", "LoginService", "Notification", "TreinoService", "$state"];

	/* @ngInject */
	function ClienteTreinoController($http, LoginService, Notification, TreinoService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.formularios = []
		vm.acessarTreino = acessarTreino;
		
		init();
		
		function init(){
			listar();
		}
		
		function listar(){
			TreinoService.listar().then(function(response) {
				vm.treinos = response;
			})
		}

		function acessarTreino(treino){
			$state.go("app.treino", {id:treino.id })
		}		

		
	}

})();