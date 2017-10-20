(function() {
	"use strict";

	angular.module("consultoria").controller("ComprarController", ComprarController);

	ComprarController.$inject = [ "$http", "Notification", "$scope", "LoginService", "FormService", "$state"];

	/* @ngInject */
	function ComprarController($http, Notification, $scope, LoginService, FormService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.comprar = comprar;
		vm.quest = false;
		vm.submitPromise = { message : "Aguarde..."	};
		vm.formularioAntigo = formularioAntigo;

		init();
		
		function init(){
			buscarFormulario();
		}
		
		function comprar(param) {
			if(vm.usuario){
				var fd = new FormData();
				fd.append('formulario', JSON.stringify(vm.formulario));
				vm.submitPromise.promise = $http.post('/comprarConsultoria/' + param, fd, {
					timeout : 50400000,
					transformRequest : angular.identity,
					headers : {
						'Content-Type' : undefined
					}
				}).then(httpSuccess, httpFail);
			} else {
				Notification.error('Entre em contato pelo email: jullianoVolpato@gmail.com, e resolveremos seu problema.');
			}
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
			$state.go('app.treinos')
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		

		function buscarFormulario(){
			FormService.buscarUltimo(vm.usuario.id).then(function(response) {
				vm.ultimoForm = response;
			})
		}
		
		function formularioAntigo(param){
			if(param){
				vm.ultimoForm.id = undefined;
				vm.formulario = vm.ultimoForm
				vm.quest = true;
			}else{
				vm.quest = true;
			}
		}
	}

})();