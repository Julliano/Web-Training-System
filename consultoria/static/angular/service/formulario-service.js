;(function() {
	"use strict";

	angular.module("consultoria").service("FormService", FormService)

	FormService.$inject = [ "$rootScope", "$http", "$q", "$state", "Notification" ];

	/** @ngInject */
	function FormService($rootScope, $http, $q, $state , Notification) {
		var _observers = [];
		var service = {
			buscar : buscar,
			buscarUltimo : buscarUltimo,
			listar : listar,
			listarAdmin : listarAdmin
		};

		return service;

		function listar() {
			return $http.get("/formularios/").then(function(response) {
				return response.data;
			})
		}

		function listarAdmin() {
			return $http.get("/admin/formularios/").then(function(response) {
				return response.data;
			})
		}
				
		function buscar(id) {
			var deferred = $q.defer()
			$http.get('/formularios/' + id).then(function(response) {
				deferred.resolve(response.data);
			}, function() {
				Notification.error("Erro ao consultar o formulário, favor notificar pelo email de contato.")
				deferred.reject();
			})
			return deferred.promise;
		}

		function buscarUltimo(id) {
			var deferred = $q.defer()
			$http.get('/formulariosUltimo/' + id).then(function(response) {
				deferred.resolve(response.data);
			}, function() {
				Notification.error("Erro ao consultar o formulário, favor notificar pelo email de contato.")
				deferred.reject();
			})
			return deferred.promise;
		}

	}

})();