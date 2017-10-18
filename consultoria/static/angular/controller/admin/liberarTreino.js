(function() {
	"use strict";

	angular.module("consultoria").controller("LiberarTreinoAdminController", LiberarTreinoAdminController);

	LiberarTreinoAdminController.$inject = [ "$http", "LoginService", "Notification", "treino"];

	/* @ngInject */
	function LiberarTreinoAdminController($http, LoginService, Notification, treino) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.salvar = salvar;
		
		init();
		
		function init(){
			$http.get('/admin/modeloTreino/').then(function(response){
				vm.modelos = response.data
			})
		}
		
		function salvar(){
//			colocar modelo escolhido pra dentro do treino
		}
		
		
	}

})();