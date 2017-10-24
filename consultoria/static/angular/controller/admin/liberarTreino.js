(function() {
	"use strict";

	angular.module("consultoria").controller("LiberarTreinoAdminController", LiberarTreinoAdminController);

	LiberarTreinoAdminController.$inject = [ "$http", "LoginService", "Notification", "treino", "$state"];

	/* @ngInject */
	function LiberarTreinoAdminController($http, LoginService, Notification, treino, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.salvar = salvar;
		vm.gerarPdf = gerarPdf;
		
		init();
		
		function init(){
			$http.get('/admin/modeloTreino/').then(function(response){
				vm.modelos = response.data
			})
		}
		
		function salvar(){
			vm.treino.nome = vm.modelo.titulo
			vm.treino.explicacao = vm.modelo.explicacao
			$http.put('/admin/treinos/', vm.treino).then(httpSuccess, httpFail)
		}
		

		function httpSuccess(response) {
			Notification.success("Treino liberado com sucesso");
			$state.go("admin.treinos")
		}
	
		function httpFail(response) {
			Notification.error("Erro, favor contate o administrador do sistema.");
		}

		function gerarPdf(){
//			var texto = document.getElementById("explicacao")
//			var doc = new jsPDF('p', 'pt', 'a4')
//			doc.text(texto.innerText, 10, 10)
//			doc.save('a4.pdf')
//			
		}
		
		
	}

})();