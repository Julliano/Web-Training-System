(function() {
	"use strict";

	angular.module("consultoria").controller("AcessarTreinoController", AcessarTreinoController);

	AcessarTreinoController.$inject = [ "$http", "LoginService", "Notification", "treino", "$uibModal"];

	/* @ngInject */
	function AcessarTreinoController($http, LoginService, Notification, treino, $uibModal) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.gerarPdf = gerarPdf;
		vm.modal = modal;
		
		init();
		
		function init(){
			vm.nome = vm.treino.venda.usuario.nome;
		}
		

		function modal() {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-app-duvida/modal-app-duvida.html'
						},
						controller : "ModalDuvidaController",
						controllerAs : "ModalDuvidaCtrl",
						resolve : {
							usuario : function() {
								return angular.copy(vm.usuario)
							}
						} 
					});

			modalInstance.result.then(function(selectedItem) {
			});
		}

		function gerarPdf(){
			
		}
		
	}

})();