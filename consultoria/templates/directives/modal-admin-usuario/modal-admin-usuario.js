;(function() {
	"use strict";
	angular.module("consultoria").controller("ModalAdminUsuarioController", ModalInstanceController);

	ModalInstanceController.$inject = ["filterFilter", "$uibModalInstance", "$http", "usuario", "grupos", "Notification", "instituicoes" ];

	/** @ngInject */
	function ModalInstanceController(filterFilter, $uibModalInstance, $http, usuario, grupos, Notification, instituicoes) {
		var vm = this;	
		vm.instituicoes = instituicoes;
		vm.salvar = salvar;
		vm.cancelar = cancelar;
		vm.grupos = grupos;
		vm.addGrupo = addGrupo;
		vm.removeGrupo = removeGrupo;
		vm.submitPromise = {
			message : "Aguarde..."
		};

		init();

		function init() {
			if (usuario) {
				vm.usuario = usuario;			
				angular.forEach(vm.usuario.grupos,function(grupo){
					vm.usuario.grupoSelecionado = grupo.id;										
				});
			}
		}

		function salvar() {
			if (vm.usuario.id) {
				vm.submitPromise.promise = $http.put('/admin/usuarios/', vm.usuario).then(httpSuccess, httpFail);
				return;
			}
			vm.submitPromise.promise = $http.post('/admin/usuarios/', vm.usuario).then(httpSuccess, httpFail);
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
		
		function addGrupo(grupo){
			vm.usuario.grupos.push(grupo)
		}
		
		function removeGrupo(key){
			vm.usuario.grupos.splice(key,1)
		}
	}
})();