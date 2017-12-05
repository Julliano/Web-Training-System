;(function() {
	"use strict";
	angular.module("consultoria").controller("ModalAdminPlanoController", ModalAdminPlanoController);

	ModalAdminPlanoController.$inject = ['filterFilter', '$uibModalInstance', '$http', 'plano', 'Notification'];

	function ModalAdminPlanoController(filterFilter, $uibModalInstance, $http, plano, Notification) {
		var vm = this;	
		vm.salvar = salvar;
		vm.cancelar = cancelar;
		vm.submitPromise = {
			message : "Aguarde..."
		};

		init();

		function init() {
			if (plano) {
				vm.plano = plano;			
			}
		}

		function salvar() {
			if (vm.plano.id) {
				vm.submitPromise.promise = $http.put('/admin/planos/', vm.plano).then(httpSuccess, httpFail);
				return;
			}
			vm.submitPromise.promise = $http.post('/admin/planos/', vm.plano).then(httpSuccess, httpFail);
		}

		function httpSuccess(response) {
			Notification.success(response.data);
			$uibModalInstance.close();
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}

		function cancelar() {
			$uibModalInstance.dismiss();
		}
	}
})();