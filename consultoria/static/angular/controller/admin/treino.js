(function() {
	"use strict";

	angular.module("consultoria").controller("TreinoAdminController", TreinoAdminController);

	TreinoAdminController.$inject = [ "$http", "LoginService", "Notification", "TreinoService", "$state"];

	/* @ngInject */
	function TreinoAdminController($http, LoginService, Notification, TreinoService, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.filtrar = filtrar;
		vm.filtroTreino = 'pendente'
		vm.liberarTreino = liberarTreino;
		vm.classTreino = classTreino;
		var hoje = new Date()

		init();
		
		function init(){
			listar();
		}
		
		function listar(){
			TreinoService.listarAdmin().then(function(response) {
				vm.treinos = response;
			})
		}
		
		function liberarTreino(treino){
			$state.go("admin.treino", {	id:treino.id })
		}
		
		function classTreino(treino){
			if(treino.status == 'pendente'){
				var date = new Date(treino.data_entrega)
				var timeDiff = Math.abs(date.getTime() - hoje.getTime());
				var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
				if(diffDays-1 < 0){
					return 'info'
				} else if (diffDays-1 == 0){
					return 'danger'
				} else if (diffDays-1 == 1){
					return 'warning'
				} else if (diffDays-1 > 1){
					return 'success'
				}
			} else {
				return 'info'
			}
		}
		
		function filtrar(param){
			vm.filtroTreino = param;
		}
		
	}

})();