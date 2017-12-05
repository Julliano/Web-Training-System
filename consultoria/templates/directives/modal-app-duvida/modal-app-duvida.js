;(function() {
	"use strict";
	angular.module("consultoria").controller("ModalDuvidaController", ModalDuvidaController);

	ModalDuvidaController.$inject = ["filterFilter", "$uibModalInstance", "$http", "Notification", "usuario"];

	/** @ngInject */
	function ModalDuvidaController(filterFilter, $uibModalInstance, $http, Notification, usuario) {
		var vm = this;
		vm.usuario = usuario;
		vm.salvar = salvar;
		vm.cancelar = cancelar;
		vm.submitPromise = {
			message : "Aguarde..."
		};

		init();

		function init() {
		}

		function salvar() {
			vm.duvida.usuario_id = usuario.id;
			vm.submitPromise.promise = $http.post('/duvidas/', vm.duvida).then(httpSuccess, httpFail);
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