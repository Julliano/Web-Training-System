(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteDuvidaController", ClienteDuvidaController);

	ClienteDuvidaController.$inject = [ "$http", "LoginService", "Notification", "$uibModal", "DuvidaService", "$state"];

	/* @ngInject */
	function ClienteDuvidaController($http, LoginService, Notification, $uibModal, DuvidaService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.modal = modal;
		vm.show = false;
		vm.verDuvida = verDuvida;
		
		init();
		
		function init(){
			if(!vm.duvida){
				listar();
			}
		}
		
		function listar() {
			DuvidaService.listar().then(function(response) {
				vm.duvidas = response;
			})
		}
		
		function verDuvida(id){
			$state.go("app.duvida", {
				id : id
			})
		}
		
		function modal(duvida) {
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
				init();
				vm.show = true;
			});
		}
		
	}

})();