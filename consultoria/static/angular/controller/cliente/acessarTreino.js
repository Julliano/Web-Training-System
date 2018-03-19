;(function() {
	"use strict";

	angular.module("consultoria").controller("AcessarTreinoController", AcessarTreinoController);

	AcessarTreinoController.$inject = ['$http', 'LoginService', 'Notification', 'treino', '$uibModal', '$state'];

	function AcessarTreinoController($http, LoginService, Notification, treino, $uibModal, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.gerarPdf = gerarPdf;
		vm.modal = modal;
		vm.go = go;
		
		init();
		
		function init(){
			vm.nome = vm.treino.venda.usuario.nome;
		}
		
		function go(){
			$state.go('app.'+vm.treino.ver)
		}
		
		function modal() {
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
			});
		}

		function gerarPdf(){
			$http.get('/treinoPdf/'+ vm.treino.id,{
				responseType: 'arraybuffer'
			}).then(function(response) {
				var file = new Blob([response.data], {type : 'application/pdf'});
				saveAs(file, 'treino'+vm.treino.id+'.pdf')
			})
		}
		
	}

})();