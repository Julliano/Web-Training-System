;(function() {
	"use strict";

	angular.module("consultoria").service("TreinoService", TreinoService)

	TreinoService.$inject = [ "$rootScope", "$http", "$q", "$state", "Notification" ];

	function TreinoService($rootScope, $http, $q, $state , Notification) {
		var _observers = [];
		var service = {
			buscar : buscar,
			listar : listar,
			listarAdmin : listarAdmin
		};

		return service;

		function listar() {
			return $http.get("/treinos/").then(function(response) {
				return response.data;
			})
		}

		function listarAdmin(pagina) {
			return $http.get("/admin/treinos/", pagina).then(function(response) {
				return response.data;
			})
		}
				
		function buscar(id) {
			var deferred = $q.defer()
			$http.get('/treinos/' + id).then(function(response) {
				deferred.resolve(response.data);
			}, function() {
				Notification.error("Erro ao consultar o treino")
				deferred.reject();
			})
			return deferred.promise;
		}

	}

})();