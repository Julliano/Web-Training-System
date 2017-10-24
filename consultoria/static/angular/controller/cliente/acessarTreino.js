(function() {
	"use strict";

	angular.module("consultoria").controller("AcessarTreinoController", AcessarTreinoController);

	AcessarTreinoController.$inject = [ "$http", "LoginService", "Notification", "treino"];

	/* @ngInject */
	function AcessarTreinoController($http, LoginService, Notification, treino) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.gerarPdf = gerarPdf;
		
		init();
		
		function init(){
			vm.nome = vm.treino.venda.usuario.nome;
		}
		

		function gerarPdf(){
			
		}
		
	}

})();