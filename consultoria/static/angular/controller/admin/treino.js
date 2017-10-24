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
		vm.filtrarPagina = filtrarPagina;
		vm.pagination = {
			paginas : 0, 
			paginaAtual : 0, 
			totalItems : 0,
			porPagina : 0				
		}
		var hoje = new Date()

		init();
		
		function init(){
			listar();
		}
		
		function listar(){
			TreinoService.listarAdmin().then(function(response) {
				vm.treinos = response.items[0];					
				vm.pagination.paginas = response.total_paginas;
				vm.pagination.paginaAtual = response.pagina_atual;
				vm.pagination.totalItems = response.total_items;
				vm.pagination.porPagina = response.por_pagina;
			})
		}

		function filtrarPagina(){
			TreinoService.listarAdmin(vm.pagination.paginaAtual).then(function(response) {
				vm.treinos = response.items[0];					
				vm.pagination.paginas = response.total_paginas;
				vm.pagination.paginaAtual = response.pagina_atual;
				vm.pagination.totalItems = response.total_items;
				vm.pagination.porPagina = response.por_pagina;
			})
		}
		
		function liberarTreino(treino){
			$state.go("admin.treino", {	id:treino.id })
		}
		
		function classTreino(treino){
			if(treino.status == 'pendente'){
				var date = new Date(treino.data_entrega)
				var timeDiff = Math.abs(hoje.getTime() - date.getTime());
//				var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
				var diffDays = Math.ceil((date - hoje) / 86400000);
				if (diffDays < 1){
					return 'danger'
				} else if (diffDays >= 1 && diffDays <2){
					return 'warning'
				} else if (diffDays >= 2){
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