(function() {
	"use sctrict";

	angular.module("consultoria").factory("Locale", Locale);

	Locale.$inject = [];

	/* @ngInject */

	function Locale() {
		ptbr = {
			"decimal" : ",",
			"thousands" : ".",
			"grouping" : [ 3 ],
			"currency" : [ "R$", "" ],
			"dateTime" : "%A, %e de %b de %Y - %X",
			"date" : "%d/%m/%Y",
			"time" : "%H:%M:%S",
			"periods" : [ "AM", "PM" ],
			"days" : [ "domingo", "sengunda-feira", "terça-feira",
					"quarta-feira", "quinta-feira", "sexta-feira", "sábado" ],
			"shortDays" : [ "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab" ],
			"months" : [ "Janeiro", "Fevereiro", "Março", "Abril", "Maio",
					"Junho", "Julho", "Agosto", "Setembro", "Outubro",
					"Novembro", "Dezembro" ],
			"shortMonths" : [ "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul",
					"Ago", "Set", "Out", "Nov", "Dez" ]
		}
		return d3.locale(ptbr)
	}

})();