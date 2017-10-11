(function() {
	"use strict";

	angular.module("consultoria").controller("ModeloAdminController", ModeloAdminController);

	ModeloAdminController.$inject = [ "$http", "LoginService", "Notification", "$uibModal" ];

	/* @ngInject */
	function ModeloAdminController($http, LoginService, Notification, $uibModal) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.modal = modal;

		function init(){
//			listar();
		}
		
		function listar() {
//			ModeloService.listar().then(function(response) {
//				vm.duvidas = response;
//			})
			
		}
		
		function modal(modelo) {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-admin-modeloTreino/modal-admin-modeloTreino.html'
						},
						controller : "ModalModeloTreinoController",
						controllerAs : "ModalModTreinoCtrl",
						resolve : {
							modelo : function() {
								return angular.copy(vm.modelo)
							}
						} 
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}
		
	}

})();