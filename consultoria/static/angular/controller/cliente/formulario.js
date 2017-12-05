;(function() {
	"use strict";

	angular.module("consultoria").controller("ClienteFormularioController", ClienteFormularioController);

	ClienteFormularioController.$inject = ['$http', 'LoginService', 'Notification', 'form', '$state'];

	function ClienteFormularioController($http, LoginService, Notification, form, $state) {
		var vm = this;
		vm.formulario = form;
		vm.usuario = LoginService.getUsuario();
		vm.salvar = salvar;
		vm.disponibilidade = disponibilidade;

		
		function salvar() {			
			$http.put('/formularios/', vm.formulario).then(function(response) {
				Notification.success(response.data);
				$state.go("app.treinos")
			}, function(response) {
				Notification.error(response.data);
			})
		}
		
		function disponibilidade(param){
			vm.formulario.disponibilidade.push(param)
		}
	}

})();