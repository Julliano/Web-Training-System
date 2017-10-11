(function() {
	"use strict";
	angular.module("consultoria").controller("ModalModeloTreinoController", ModalModeloTreinoController);

	ModalModeloTreinoController.$inject = ["filterFilter", "$uibModalInstance", "$http", "modelo", "Notification"];

	function ModalModeloTreinoController(filterFilter, $uibModalInstance, $http, modelo, Notification) {
		var vm = this;	
		vm.salvar = salvar;
		vm.cancelar = cancelar;
		vm.submitPromise = {
			message : "Aguarde..."
		};

		init();

		function init() {
		}

		function salvar() {
			if (vm.modelo.id) {
				vm.submitPromise.promise = $http.put('/admin/modeloTreino/', vm.modelo).then(httpSuccess, httpFail);
				return;
			}
			vm.submitPromise.promise = $http.post('/admin/modeloTreino/', vm.modelo).then(httpSuccess, httpFail);
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