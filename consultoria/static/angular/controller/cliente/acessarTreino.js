;(function() {
	"use strict";

	angular.module("consultoria").controller("AcessarTreinoController", AcessarTreinoController);

	AcessarTreinoController.$inject = ['$http', 'LoginService', 'Notification', 'treino', '$uibModal', '$state'];

	function AcessarTreinoController($http, LoginService, Notification, treino, $uibModal, $state) {
		var vm = this;
		vm.usuario = LoginService.getUsuario();
		vm.treino = treino;
		vm.gerarPdf = gerarPdf;
		vm.modal = modal;
		vm.go = go;
		
		init();
		
		function init(){
			vm.nome = vm.treino.venda.usuario.nome;
		}
		
		function go(){
			$state.go('app.'+vm.treino.ver)
		}
		
		function modal() {
			var modalInstance = $uibModal
					.open({
						animation : true,
						templateUrl : function() {
							return '/templates/directives/modal-app-duvida/modal-app-duvida.html'
						},
						controller : "ModalDuvidaController",
						controllerAs : "ModalDuvidaCtrl",
						resolve : {
							usuario : function() {
								return angular.copy(vm.usuario)
							}
						} 
					});

			modalInstance.result.then(function(selectedItem) {
			});
		}

		function gerarPdf(){
			var quotes = document.getElementById('treinoDescricao');
			quotes.style.width = '780px !important'
			html2canvas(quotes, {
	            onrendered: function (canvas) {
	            	var pdf = new jsPDF('p', 'pt', 'a4');
	                for (var i = 0; i <= quotes.clientHeight/980; i++) {
	                    var srcImg  = canvas;
	                    var sX      = -20;
	                    var sY      = 1100*i; // start 980 pixels down for every new page
	                    var sWidth  = 1150;
	                    var sHeight = 1120;
	                    var dX      = 30;
	                    var dY      = 20;
	                    var dWidth  = 830;
	                    var dHeight = 1120;
	                    window.onePageCanvas = document.createElement("canvas");
	                    onePageCanvas.setAttribute('width', 778);
	                    onePageCanvas.setAttribute('height', 1120);
	                    var ctx = onePageCanvas.getContext('2d');
	                    ctx.strokeStyle = '';  // some color/style
	                    ctx.lineWidth = 0;
	                    ctx.drawImage(srcImg,sX,sY,sWidth,sHeight,dX,dY,dWidth,dHeight);
	                    var canvasDataURL = onePageCanvas.toDataURL("image/png", 1.0);
	                    var width         = onePageCanvas.width;
	                    var height        = onePageCanvas.clientHeight;
	                    if (i > 0) {
	                        pdf.addPage(595, 842); //8.5" x 11" in pts (in*72)
	                    }
	                    pdf.setPage(i+1);
	                    pdf.addImage(canvasDataURL, 'PNG', 0, 0, (width*.72), (height*.71));
	                }
	                pdf.save('Treino'+vm.treino.id+'.pdf');
	            }
	        });
		}
		
	}

})();