;(function() {
	"use strict";

	angular.module("consultoria").controller("PlanoAdminController", PlanoAdminController);

	PlanoAdminController.$inject = [ "$http", "LoginService", "Notification", "$uibModal" ];

	/** @ngInject */
	function PlanoAdminController($http, LoginService, Notification, $uibModal) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.modal = modal;

		
		init();
		
		function init(){
			listar()
		}
		
		function listar() {
			$http.get('/planos').then(function(response) {
				vm.planos = response.data;
			})
		}
		
		function modal(plano) {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-admin-plano/modal-admin-plano.html'
						},
						controller : "ModalAdminPlanoController",
						controllerAs : "ModalAdmPlanoCtrl",
						resolve : {
							plano : function() {
								return angular.copy(plano)
							}
						}
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}
		
	}

})();