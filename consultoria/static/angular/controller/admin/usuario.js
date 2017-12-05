;(function() {
	'use strict';

	angular.module('consultoria').controller("AdminUsuarioController", AdminUsuarioController);

	AdminUsuarioController.$inject = ['$http', '$uibModal', 'Notification'];

	function AdminUsuarioController($http, $uibModal, Notification) {
		var configModalConfirma = configModalConfirma();
		var vm = this;
		vm.listar = listar;
		vm.modal = modal;		
		vm.selecionarUsuario = selecionarUsuario;		
		vm.editar = modal;
		vm.deletar = deletar;

		init()

		function init() {
			listar()
		}
		
		function configModalConfirma() {			
			return {
				animation : true,
				templateUrl :'/templates/directives/modal-confirmacao/modal-confirmacao.html',						
				backdrop : 'static',
				controller : "ModalConfirmacaoController",
				controllerAs : "ModalConfCtrl",
				size: 'sm',
			}
		}

		function modal(usuario) {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-admin-usuario/modal-admin-usuario.html'
						},
						controller : "ModalAdminUsuarioController",
						controllerAs : "ModalAdmUsuarioCtrl",
						resolve : {
							usuario : function() {
								return angular.copy(usuario)
							},
							grupos : function(){
								return $http.get('/grupos/').then(function(response){
									return response.data
								})
							},
//							instituicoes : InstituicaoService.listar()
						}
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}

		function listar() {
			$http.get('/usuarios').then(function(response) {
				vm.usuarios = response.data;
			})
			
		}

		function deletar(usuario){
			var modalInstance = $uibModal.open(configModalConfirma);
			modalInstance.result.then(function(selectedItem) {
			if(selectedItem == 1){
				$http.delete('/usuarios/'+usuario.id).then(function(response){
					Notification.success("Usuário removido com sucesso!")
					listar();
				}, function(){
					Notification.error("Erro ao remover usuário, tente novamente")
					})
				}
			})
		}
		function selecionarUsuario(obj) {
			vm.usuarioSelecionado = obj;
		}
	}
})();
