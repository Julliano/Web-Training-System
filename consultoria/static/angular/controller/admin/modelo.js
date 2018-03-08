;(function() {
	"use strict";

	angular.module("consultoria").controller("ModeloAdminController", ModeloAdminController);

	ModeloAdminController.$inject = ['$http', 'LoginService', 'Notification', '$uibModal', 'ModeloService'];

	function ModeloAdminController($http, LoginService, Notification, $uibModal, ModeloService) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.modal = modal;
		vm.gerarPdf = gerarPdf;
		
		init();
		
		function init(){
			listar();
		}
		
		function listar() {
			ModeloService.listarAdmin().then(function(response) {
				vm.modelos = response;
			})
			
		}

		function gerarPdf(modelo){
			$http.get('/modeloPdf/'+ modelo.id,{
				responseType: 'arraybuffer'
			}).then(function(response) {
				var file = new Blob([response.data], {type : 'application/pdf'});
				saveAs(file, modelo.titulo+'.pdf')
			})
		}
		
		function modal(modelo) {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-admin-modeloTreino/modal-admin-modeloTreino.html'
						},
						size : 'lg',
						backdrop : 'static',
						controller : "ModalModeloTreinoController",
						controllerAs : "ModalModTreinoCtrl",
						resolve : {
							modelo : function() {
								return angular.copy(modelo)
							}
						} 
					});

			modalInstance.result.then(function(selectedItem) {
				init();
			});
		}
		
	}

})();