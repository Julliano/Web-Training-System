(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteTreinoController", ClienteTreinoController);

	ClienteTreinoController.$inject = [ "$http", "LoginService", "Notification", "FormService", "TreinoService", "$state"];

	/* @ngInject */
	function ClienteTreinoController($http, LoginService, Notification, FormService, TreinoService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.formularioAntigo = formularioAntigo;
		
		init();
		
		function init(){
			buscarFormulario();
			listar();
		}

		function buscarFormulario(){
			FormService.buscarUltimo(vm.usuario.id).then(function(response) {
				vm.formularios = response;
			})
		}
		
		function listar(){
			TreinoService.listar().then(function(response) {
				vm.treinos = response;
			})
		}
		
		function formularioAntigo(param){
			if(param){
				vm.formulario = vm.formularios[1]
			}else{
				$state.go('app.formulario', {id : vm.formularios[0].id})
			}
		}

	}

})();