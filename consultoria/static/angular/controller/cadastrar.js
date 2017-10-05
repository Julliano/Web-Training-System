(function() {
	"use strict";

	angular.module("consultoria").controller("CadastrarController", CadastrarController);

	CadastrarController.$inject = [ "$http", "LoginService", "Notification" ];

	/* @ngInject */
	function CadastrarController($http, LoginService, Notification) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.estados = ["Outro","Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins"];

	}

})();