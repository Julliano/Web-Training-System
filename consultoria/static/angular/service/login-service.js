(function() {
	"use strict";

	angular.module("consultoria").service("LoginService", LoginService);

	LoginService.$inject = [ "$q", "$rootScope", "$state", "$http", "Notification" ];

	function LoginService($q, $rootScope, $state, $http, Notification) {
		var _usuario;
		var _compra;
		var _observers = {total_change : []}
		var service = {
			login : login,
			logout : logout,
			getSession : getSession,
			getUsuario : getUsuario,
			logged : logged,
			addObserver : addObserver,
			removeNotificacao : removeNotificacao
		}

		return service;

		function addObserver(event,callback){
			_observers[event].push(callback)
		}
		
		function removeNotificacao(id){
			$http.post('/remove_notificacao/'+id).then(function(response){
				_usuario = response.data
				total_change();
			})
		}
		
		function total_change(){
			angular.forEach(_observers.total_change,function(callback){
				callback(_usuario.total_notificacoes)
			})
		}
		
		function logged() {
			var deferred = $q.defer()
			$http.get("/loged").then(function(response) {
				if (!angular.equals({}, response.data.usuario)) {
					_usuario = response.data.usuario
					deferred.resolve(true);
				}
				deferred.reject(false);
			}, function() {
				deferred.reject(false);
			})
			return deferred.promise;
		}
		
		function getUsuario() {			
			return _usuario;
		}

		function getSession() {
			var deferred = $q.defer();
			/*
			 * if ($rootScope.session === true) { deferred.resolve(true); } else {
			 * deferred.reject(); $state.go("index.signin"); }
			 */
			$http.get("/check_session/").then(function(response) {
				if (response.lembrar && response.session) {
					deferred.resolve(true)
				}
				deferred.reject(false)
			}, function(response) {
				deferred.reject(false)
			})			
			return deferred.promise;
		}

		function login(usuario, param) {
			_compra = param;
			return $http.post("/login", usuario).then(loginSuccess, loginFailed)
		}

		function logout() {
			$rootScope.session = false;
			return $http.get("/logout").then(logoutSuccess, logoutFailed)
		}

		function loginSuccess(response) {
			if (response.data.auth) {
				$rootScope.session = true;
				logged().then(function(){
					Notification.success('Login bem sucessido. Bem Vindo!')
					if(_usuario.grupos[0]['nome'] == "admin"){
						$state.go("admin.treinos");
					} else {
						if(_compra.valor){
							$state.go("app.compra"+_compra.valor)
						}else{
							$state.go("app.treinos");
						}
					}					
				})
				return response.data;
			}
			return loginFailed(response)
		}

		function loginFailed(response) {
			Notification.error({
				message : response.data.message
			})
			return response.data
		}

		function logoutSuccess(response) {
			$state.go("index.start")
			_usuario = null;
		}

		function logoutFailed(response) {
			console.log(response.data)
		}

	}
})()