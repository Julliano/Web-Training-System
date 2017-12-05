;(function() {
	"use strict";

	angular.module("consultoria").controller("NavbarController", NavbarController);

	NavbarController.$inject = ['$state', 'LoginService', '$http', '$scope'];

	function NavbarController($state, LoginService, $http, $scope) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();

		vm.login = function(passwd) {
			LoginService.login(vm.email, passwd)
		};

		vm.logout = function() {
			LoginService.logout()
			$state.reload();
		}
		
//		vm.usuario_observer = usuario_observer;
		vm.atualizaTotalPendencias = getTotalPendencias;
		
		init();

		function init() {			
//			LoginService.addObserver('total_change',usuario_observer);
//			if($state.includes('admin')){
//				getTotalDuvidas();
//				OperacaoService.addObserver(getTotalDuvidas)
//			}
		}
		
		function getTotalPendencias(){			
			$http.get('/contar_duvidas/').then(function(response){					
				vm.adminTotalDuvidas = response.data
			})
		}
		
//		function usuario_observer(total){
//			vm.usuario.total_notificacoes = total; 
//		}
	}
})();