(function() {
	"use strict";

	angular.module("consultoria").controller("NavbarController", NavbarController);

	NavbarController.$inject = ["filterFilter", "$state", "LoginService", "$http", "$scope", "OperacaoService"];

	/* @ngInject */
	function NavbarController(filterFilter, $state, LoginService, $http, $scope, OperacaoService) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.collapse = true;
		vm.isAvaliar = isAvaliar;
		vm.count = 1;
		vm.pesquisa = pesquisa;
		vm.pesquisaApp = pesquisaApp;

		vm.login = function(passwd) {
			LoginService.login(vm.email, passwd)
		};

		vm.logout = function() {
			LoginService.logout()
		}
		
		vm.usuario_observer = usuario_observer;
		vm.atualizaTotalPendencias = getTotalPendencias;
		
		init();

		function init() {			
			LoginService.addObserver('total_change',usuario_observer);
			if($state.includes('admin')){
				getTotalPendencias();
				OperacaoService.addObserver(getTotalPendencias)
			}
		}
		
		function getTotalPendencias(){			
			$http.get('/contar_pendencias/').then(function(response){					
				vm.adminTotalPendencias = response.data
			})
		}
		function usuario_observer(total){
			vm.usuario.total_notificacoes = total; 
		}

		function isAvaliar() {
			return $state.current.name == "admin.relatorios";
		}
		
		function pesquisa() { 
			return $state.current.name == "admin.consultar"
		}

		function pesquisaApp() { 
			return $state.current.name == "app.consultar"
		}
		
	}
})();