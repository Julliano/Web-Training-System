(function() {
	'use strict';

	angular.module('consultoria', [ 'ngResource','ngRoute', 'ui.bootstrap', 'ui.router', 'ui-notification', 'angular-loading-bar', 'cgBusy', 'ui.mask', 'uiSwitch' ])

	.config([ '$stateProvider', '$urlRouterProvider' , '$provide', '$uibTooltipProvider', 'cfpLoadingBarProvider', config ])

	.run(function($http, $rootScope) {
		init();

		function init() {
			$rootScope.submitPromise = { message:"Aguarde..." };
		}
	});

	function config($stateProvider, $urlRouterProvider, tagsInputConfigProvider, $provide, $uibTooltipProvider, cfpLoadingBarProvider) {
		var operacoes = function (LoginService, $http) {
			return LoginService.logged().then(function(response){				
				var instituicaoId = LoginService.getUsuario().instituicao.id;
				return $http.get('/instituicoes/' + instituicaoId).then(function(response) {
					return response.data.operacoes;
				})			
			})
		}
		var proprietarios = function(Proprietario){
			try{
				return Proprietario.query().$promise
			}catch(err){
				return false;
			}
		};
		
		var session = function(LoginService, $stateParams, $state) {
			return LoginService.logged().then(function(response) {				
				return response;
			}, function(response) {
				$state.go("index.signin");
				return false;
			});
		};
		
		cfpLoadingBarProvider.includeSpinner = false;
		
		$uibTooltipProvider.options({popupDelay:500});
		
		$provide.decorator('$state', function($delegate, $rootScope) {
		    $rootScope.$on('$stateChangeStart', function(event, state, params, from, fromParams) {
		    	$delegate.next = state;
		    	$delegate.toParams = params;
		    	$delegate.from = from;
		    	$delegate.fromParams = fromParams;
		    });
		    
		    return $delegate;
		 });
		
		// For unmatched routes
		$urlRouterProvider.otherwise('/index/start');
		//$urlRouterProvider.when('/app/operacoes', '/app/consultar');

		// Application routes
		$stateProvider.state('index', {
			url : '/index',
			controller : 'PresentationController',
			controllerAs : 'PresentCtrl',
			templateUrl : '/templates/presentation/base.html',
		}).state('index.start', {
			url : '/start',
			templateUrl : '/templates/presentation/start.html'
		}).state('index.signin', {
			url : '/signin',
			templateUrl : '/templates/presentation/signin.html',
			resolve : {
				automatic_login : function(LoginService, $state) {
					LoginService.logged().then(function(response) {
						if (response) {
							$state.go("app.consultar")
						}
					})
				}
			}
		}).state('app', {
			url : '/app',
			templateUrl : '/app/cliente/base.html',
			resolve : {
				session : session
			}
		}).state('app.operacoes', {
			url : '/operacoes/:id',
			templateUrl : '/app/cliente/operacoes.html',
			controller : "ClienteOperacaoController",
			controllerAs : "CliOperacaoCtrl",
			resolve : {
				operacao : operacao
			}
		}).state('app.operacoes.relatorios', {
			url : '/relatorios/:relatorio',
			templateProvider : function($http, $templateCache, relatorio){
				return $templateCache.get('cliente_'+relatorio.tipo_relatorio+'.html') ||
				 $http.get('/app/cliente/relatorios/'+relatorio.tipo_relatorio+'.html').then(function(response){
					return $templateCache.put('cliente_'+relatorio.tipo_relatorio+'.html', response.data);							
				});
			},
			//controller : 'RelatorioController',
			controllerProvider: function($stateParams, relatorio) {
				return relatorio.tipo_relatorio.charAt(0).toUpperCase() + relatorio.tipo_relatorio.slice(1) + "Controller";				
			},
			controllerAs : 'RelCtrl',
			resolve : {
				relatorio : relatorio
			}
		}).state('app.sant', {
			url : '/pdf/:relatorio'
		}).state('app.editar', {
			url : '/reports',
			templateUrl : '/app/map.html',
			controller : 'MapController',
			controllerAs : 'MapCtrl'
		}).state('app.consultar', {
			url : '/consultar',
			templateUrl : '/app/cliente/consultar.html',
			controller : 'ClienteConsultaController',
			controllerAs : 'CliConCtrl'
			/*resolve : {
				operacoes : operacoes
			}*/
		}).state('app.conta', {
			url : '/conta',
			templateUrl : '/app/cliente/conta.html',
			controller : 'ClienteContaController',
			controllerAs : 'CliContaCtrl'
		}).state('app.cadastrarOpBase', {
			url : '/cadastroOperacaoBase',
			templateUrl : '/app/cliente/cadastro_operacoes_base.html',
			controller : 'CadastroOperacaoBaseController',
			controllerAs : 'CadOpBaseCtrl',
			resolve : {
				culturas : culturas
			}
		}).state('app.cadastrarOpMonitoramento', {
			url : '/cadastroOperacaoMonitoramento',
			templateUrl : '/app/cliente/cadastro_operacoes_monitoramento.html',
			controller : 'CadastroOperacaoMonitoramentoController',
			controllerAs : 'CadOpMoniCtrl',
			resolve : {
				culturas : culturas
			}
		}).state('app.embargos', {
			url : '/embargos',
			templateUrl : '/app/cliente/verificar_embargos.html',
			controller : 'EmbargosController',
			controllerAs : 'EmbargosCtrl'
		}).state('admin', {
			url : '/admin',
			templateUrl : '/app/admin/base.html',
			resolve : {
				session : session
			}
		}).state('admin.consultar', {
			url : '/consultar',
			templateUrl : '/app/admin/consultar.html',
			controller : 'ConsultarController',
			controllerAs : 'ConsultaCtrl'
		}).state('admin.cadastrarOpBase', {
			url : '/cadastroOperacaoBase',
			templateUrl : '/app/admin/cadastro_operacoes_base.html',
			controller : 'CadastroOperacaoAdminBaseController',
			controllerAs : 'CadOpAdmBaseCtrl',
			resolve : {
				culturas : culturas				
			}
		}).state('admin.cadastrarOpMonitoramento', {
			url : '/cadastroOperacaoMonitoramento',
			templateUrl : '/app/admin/cadastro_operacoes_monitoramento.html',
			controller : 'CadastroOperacaoAdminMonitoramentoController',
			controllerAs : 'CadOpAdmMoniCtrl',
			resolve : {
				culturas : culturas
			}
		}).state('admin.instituicoes', {
			url : '/instituicoes',
			templateUrl : '/app/admin/instituicoes.html',
			controller : 'InstituicaoController',
			controllerAs : 'InstituicaoCtrl'
		}).state('admin.usuarios', {
			url : '/usuarios',
			templateUrl : '/app/admin/usuarios.html',
			controller : 'AdminUsuarioController',
			controllerAs : 'UsuarioCtrl'
		}).state('admin.operacoes', {
			url : '/operacoes/:id',
			templateUrl : '/app/admin/operacoes.html',
			controller : 'AdminOperacaoController',
			controllerAs : 'AdmOpCtrl',
			resolve : {
				operacao : operacao			
			}
		}).state('admin.operacoes.relatorios', {
			url : '/relatorios/:relatorio',
			templateProvider : function($http, $templateCache, relatorio){				
						return $templateCache.get(relatorio.tipo_relatorio+'.html') ||
						 $http.get('/app/admin/'+relatorio.tipo_relatorio+'.html').then(function(response){
							return $templateCache.put(relatorio.tipo_relatorio+'.html', response.data);							
						});
			},
			controllerProvider: function($stateParams, relatorio) {
				return 'Admin'+relatorio.tipo_relatorio.charAt(0).toUpperCase() + relatorio.tipo_relatorio.slice(1) + "Controller";				
			},
			controllerAs : 'AdmRelCtrl',
			resolve : {
				relatorio : relatorio
				}
		});
	}

})();
