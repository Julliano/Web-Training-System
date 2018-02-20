;(function() {
	"use strict";

	angular.module("consultoria").controller("ComprarController", ComprarController);

	ComprarController.$inject = ['$http', 'Notification', '$scope', 'LoginService', 'FormService', '$state', '$window'];

	function ComprarController($http, Notification, $scope, LoginService, FormService, $state, $window) {
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
				if(vm.formulario.cardapio1){
					vm.formulario.cardapio = 'Manha: ' + vm.formulario.cardapio1
				}
				if(vm.formulario.cardapio2){
					vm.formulario.cardapio += '. Almoço: ' + vm.formulario.cardapio2
				}
				if(vm.formulario.cardapio3){
					vm.formulario.cardapio = '. Tarde: ' + vm.formulario.cardapio3
				}
				if(vm.formulario.cardapio4){
					vm.formulario.cardapio += '. Jantar: ' + vm.formulario.cardapio4
				}
				if(vm.formulario.cardapio5){
					vm.formulario.cardapio += '. Extra: ' + vm.formulario.cardapio5
				}
//				var popup = $window.open('', '_blank')
//				popup.document.write('Carregando tela de pagamento...');
				var fd = new FormData();
				fd.append('formulario', JSON.stringify(vm.formulario));
				vm.submitPromise.promise = $http.post('/comprarConsultoria/' + param, fd, {
					timeout : 50400000,
					transformRequest : angular.identity,
					headers : {
						'Content-Type' : undefined
					}
				}).then(function httpSuccess(response, param) {
					var popup = $window.open(response.data)
//					popup.location.href = response.data;
//					$window.open(response.data, '_blank')
					Notification.success("Compra realizada, assim que o pagamento for confirmado começarei a trabalhar no seu treino.");
					$state.go('app.treinos')
				}, httpFail);
			} else {
				Notification.error('Entre em contato pelo email: jullianoVolpato@gmail.com, e resolveremos seu problema.');
			}
		}
		
		function httpSuccess(response, param) {
			param.location.href = response.data;
//			$window.open(response.data, '_blank')
			Notification.success("Compra realizada, assim que o pagamento for confirmado começarei a trabalhar no seu treino.");
			$state.go('app.treinos')
		}
	
		function httpFail(response) {
			Notification.error("Erro na conexão com o servidor do PagSeguros, favor tentar realizar o pagamento mais tarde.");
		}
		

		function buscarFormulario(){
			FormService.buscarUltimo(vm.usuario.id).then(function(response) {
				vm.ultimoForm = response;
				if(vm.ultimoForm){
					vm.ultimoForm.cupom = null;
				}
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