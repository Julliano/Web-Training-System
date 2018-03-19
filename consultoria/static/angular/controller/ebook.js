;(function() {
	"use strict";

	angular.module("consultoria").controller("EbookController", EbookController);

	EbookController.$inject = ['$http', 'LoginService', 'Notification'];

	function EbookController($http, LoginService, Notification) {
		var vm = this;
		vm.baixar = baixar;
		vm.submitPromise = { message : "Aguarde..."	};
		
		init();
		
		function init(){
			vm.ebook = window.location.href.split('=')[1];
			if (vm.ebook){
				vm.submitPromise.promise = $http.post('/enviarEbook/', {ebook : vm.ebook}).then(httpSuccess, httpFail);
			}
		}
		
		function baixar() {
			vm.submitPromise.promise = $http.post('/emailEbook/', {email : vm.email}).then(httpSuccess, httpFail);
		}
		
		function httpSuccess(response) {
			Notification.success(response.data);
		}
	
		function httpFail(response) {
			Notification.error(response.data);
		}
		
	}

})();