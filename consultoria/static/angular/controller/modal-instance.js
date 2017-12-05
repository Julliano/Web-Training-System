;(function() {
	"use strict";
	angular.module("consultoria").controller("ModalInstanceController", ModalInstanceController);

	ModalInstanceController.$inject = ['$uibModalInstance', '$http', 'model', 'obj'];

	function ModalInstanceController($uibModalInstance, $http, model, obj) {
		var vm = this;
		vm.objeto = {};
		vm.salvar = salvar;
		vm.cancelar = cancelar;		
		
		init();

		function init() {
			vm.objeto = obj || {};
		}

		function salvar() {
			if(vm.objeto.id){
				$http.put('/' + model+'/', vm.objeto).then(httpSuccess, httpFail)
				return;
			}
			$http.post('/' + model+'/', vm.objeto).then(httpSuccess, httpFail)
		}

		function httpSuccess(response){
			console.log("success");
			$uibModalInstance.close();
		}
		
		function httpFail(response){
			console.log("error");
		}		
		
		function cancelar() {
			$uibModalInstance.dismiss();
		}
	}
})();