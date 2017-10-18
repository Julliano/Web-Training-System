;(function() {
	"use strict";

	angular.module("consultoria").service("ModeloService", ModeloService)

	ModeloService.$inject = [ "$rootScope", "$http", "$q", "$state", "Notification" ];

	function ModeloService($rootScope, $http, $q, $state , Notification) {
		var _observers = [];
		var service = {
//			buscar : buscar,
			listarAdmin : listarAdmin
		};

		return service;

		function listarAdmin() {
			return $http.get("/admin/modeloTreino/").then(function(response) {
				return response.data;
			})
		}
				
//		function buscar(id) {
//			var deferred = $q.defer()
//			$http.get('/duvidas/' + id).then(function(response) {
//				deferred.resolve(response.data);
//			}, function() {
//				Notification.error("Erro ao consultar dúvida")
//				deferred.reject();
//			})
//			return deferred.promise;
//		}

	}

})();